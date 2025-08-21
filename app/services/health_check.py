import asyncio
from collections.abc import Callable

from pydantic import NonNegativeFloat

from app.contracts.services import IHealthCheckService
from app.core.config import Settings
from app.core.enums import Status
from app.schemas.health import ComponentHealth, HealthResponse


class HealthCheckService(IHealthCheckService):
    """
    Service for checking the health of the application.
    """

    async def gather_health_checks(
        self, checks: dict[str, Callable], timeout: float | None = 5.0
    ) -> dict[str, ComponentHealth]:
        """
        Execute health checks concurrently while preserving service names.
        Individual failures don't stop other checks.
        """

        async def safe_health_check(
            name: str, check_func: Callable
        ) -> tuple[str, ComponentHealth]:
            try:
                if timeout:
                    result = await asyncio.wait_for(check_func(), timeout=timeout)
                else:
                    result = await check_func()

                self.logger.debug(f"Health check '{name}' completed successfully")
                return name, result

            except TimeoutError:
                self.logger.warning(f"Health check '{name}' timed out after {timeout}s")
                return name, ComponentHealth(
                    status=Status.DOWN,
                    details={"error": f"Timeout after {timeout}s"},
                    responseTime=timeout,
                )

            except Exception as e:
                self.logger.error(f"Health check '{name}' failed: {e}")
                return name, ComponentHealth(
                    status=Status.DOWN,
                    details={"error": str(e)},
                    responseTime=0.0,
                )

        # Create tasks for all health checks
        tasks = [
            safe_health_check(name, check_func) for name, check_func in checks.items()
        ]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

        return dict(results)

    async def check_health(
        self, settings: Settings, uptime: NonNegativeFloat
    ) -> HealthResponse:
        services_checks: dict[str, Callable] = {  # type: ignore
            # TODO: Add health checks for services. Each entry should be:
            # ServiceNames.service_name: service.check_health (method returning ComponentHealth)
            # ComponentHealth requires: status, details dict, responseTime
            # Services should implement ServiceWithHealthCheck protocol
        }

        health_results: dict[str, ComponentHealth] = await self.gather_health_checks(
            services_checks, timeout=5.0
        )

        # Determine overall status based on individual check results
        overall_status = Status.UP
        for _service_name, result in health_results.items():
            if isinstance(result, ComponentHealth) and result.status == Status.DOWN:
                overall_status = Status.DOWN
                break

        return HealthResponse(
            status=overall_status,
            uptime=uptime,
            checks=health_results,
            version=settings.version,
            environment=settings.environment,
        )

from pydantic import BaseModel, ConfigDict


class Constants(BaseModel):
    # Right now we dont have any constants, so we dont need to define any constants. This is just a placeholder.

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class ServiceNames(BaseModel):
    # Right now we dont have any services, so we dont need to define any constants. This is just a placeholder.

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

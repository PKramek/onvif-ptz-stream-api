# ONVIF PTZ Stream API - Dev Container

This directory contains the development container configuration for the ONVIF PTZ Stream API project.

## Required Files

The project requires the ONVIF Device Management WSDL file for proper functionality.

### Download the Device Management WSDL

To download the required `devicemgmt.wsdl` file, run the following command:

```bash
wget -O devicemgmt.wsdl https://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl
```

This file contains the ONVIF Device Management service definitions needed for the API to communicate with ONVIF-compliant devices.

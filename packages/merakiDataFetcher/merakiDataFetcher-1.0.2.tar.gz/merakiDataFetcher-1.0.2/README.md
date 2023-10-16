# Meraki Data Fetcher

This module pulls the data using the Meraki sdk.   
For better processing of the data dataclasses was created.   
These are then used to create objects that have the data from the Meraki API.  


## meraki_data_fetcher

The MerakiDataFetcher expects an apikey when instantiating.  
The object has the following methods.  
- apikey_validation() -> boolean
- get_organizations() -> [MerakiOrganization]
- get_networks(organizationId: str) -> [MerakiNetwork]
- get_device(deviceSerial: str) -> MerakiDevice
- get_network(networkId: str) -> MerakiNetwork
- get_network_devices(networkId: str, types='all': str) -> [MerakiDevice]


### apikey_validation

With the method "apikey_validation" a boolean is returned.  
True, if the apikey is valid. Otherwise, it returns False.


### get_organizations

The method "get_organizations" returns all organizations available with the apikey  
as an instance of the MerakiOrganizations dataclass.


### get_networks

The get_networks method takes an organizationId.  
Then all networks which are contained in the organization are returned as a list of MerakiNetwork instances.  


### get_device

The get_device method takes a deviceSerial and returns the device data as MerakiDevice instance.


### get_network

The get_network method takes a networkId and returns the network data as MerakiNetwork instance.


### get_network_devices

The get_network_devices method takes the networkId as a required parameter.  
Optionally, the type of the devices can also be passed as parameter.
The default parameter is all.
The following types are available to pass
- 'all'
- 'Firewall'
- 'Switch'
- 'Access Point'
- 'Sensor'
- 'Camera'

The type must be passed as a string.

## Dataclasses

There are eight dataclasses.


### meraki_organization

The dataclass meraki_organization stores organizations with the values
- id
- name
- url
- api
- networks

The networks are optional.
On the one hand, so that organizations can be created without networks.  
On the other hand, because the networks get the OrganizationId.  
The value to attach the networks as a list is a feature that can be used, but does not have to be used.  
All other values must be set when instantiating.  


### meraki_network

The dataclass meraki_network stores networks with the values
- id
- organizationId
- name
- productTypes
- timeZone
- tags
- url
- notes
- configTemplateId
- isBoundToConfigTemplate

All these values must be set.


### meraki_device

The dataclass meraki_device is a parent class for all types of Meraki devices.  
This contains the values  
- name
- lat
- lng
- serial
- mac
- model
- address
- notes
- tags
- networkId
- firmware
- floorPlanId
- url
- productType


#### meraki_device_appliance

The dataclass meraki_device_appliance is a child class for Meraki Firewalls.  
This contains the values from the meraki_device dataclass and
- wan1Ip
- wan2Ip


#### meraki_device_camera

The dataclass meraki_device_camera is a child class for Meraki Cameras.  
This contains the values from the meraki_device dataclass and
- lanIp
- wirelessMac


#### meraki_device_sensor

The dataclass meraki_device_sensor is a child class for Meraki Sensors.  
This contains the values from the meraki_device dataclass and
- lanIp


#### meraki_device_switch

The dataclass meraki_device_switch is a child class for Meraki Switches.  
This contains the values from the meraki_device dataclass and
- lanIp
- switchProfileId

#### meraki_device_wireless

The dataclass meraki_device_wireless is a child class for Meraki Access Points.  
This contains the values from the meraki_device dataclass and
- lanIp
- beaconIdParams


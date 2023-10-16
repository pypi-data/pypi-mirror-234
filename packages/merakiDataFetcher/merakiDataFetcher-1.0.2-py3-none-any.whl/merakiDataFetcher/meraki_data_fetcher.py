import meraki
from meraki import APIError

from meraki_dataclasses.meraki_device import MerakiDevice
from meraki_dataclasses.meraki_device_appliance import MerakiAppliance
from meraki_dataclasses.meraki_device_camera import MerakiCamera
from meraki_dataclasses.meraki_device_sensor import MerakiSensor
from meraki_dataclasses.meraki_device_switch import MerakiSwitch
from meraki_dataclasses.meraki_device_wireless import MerakiWireless
from meraki_dataclasses.meraki_network import MerakiNetwork
from meraki_dataclasses.meraki_organization import MerakiOrganization


class MerakiDataFetcher:

    def __init__(self, apikey: str):
        """
        :param apikey:
        """
        api_key = apikey
        self.dashboard = meraki.DashboardAPI(api_key=api_key, suppress_logging=True)

    def apikey_validation(self) -> bool:
        """
        :return:
        """
        return bool(self._get_organizations())

    def _get_organizations(self):
        """
        :return:
        """
        try:
            organizations = self.dashboard.organizations.getOrganizations()
            return organizations
        except APIError:
            return None

    def _get_networks(self, organizationId: str):
        """
        :param organizationId:
        :return:
        """
        try:
            networks = self.dashboard.organizations.getOrganizationNetworks(organizationId=organizationId)
            return networks
        except APIError:
            return None

    def _get_device(self, deviceSerial: str):
        """
        :param deviceSerial:
        :return:
        """
        try:
            device = self.dashboard.devices.getDevice(serial=deviceSerial)
            return device
        except APIError:
            return None

    def _get_network(self, networkId: str):
        """
        :param networkId:
        :return:
        """
        try:
            network = self.dashboard.networks.getNetwork(networkId=networkId)
            return network
        except APIError:
            return None

    def _get_network_devices(self, networkId: str):
        """
        :param networkId:
        :return:
        """
        try:
            devices = self.dashboard.networks.getNetworkDevices(networkId=networkId)
            return devices
        except APIError:
            return None

    def _device_factory(self, device: dict) -> MerakiDevice:
        """
        :param device:
        :return:
        """
        device_data: MerakiDevice = None
        device_values = (device.get('name', ""),
                         device.get('lat', ""),
                         device.get('lng', ""),
                         device.get('serial', ""),
                         device.get('mac', ""),
                         device.get('model', ""),
                         device.get('address', ""),
                         device.get('notes', ""),
                         device.get('tags', ""),
                         device.get('networkId', ""),
                         device.get('firmware', ""),
                         device.get('floorPlanId', ""),
                         device.get('url', ""))

        if "MX" in device.get('model'):
            mr_values = ('Firewall', device.get('wan1Ip'), device.get('wan2Ip'))
            device_data = MerakiAppliance(*device_values, *mr_values)
        elif "MS" in device.get('model'):
            mr_values = ('Switch', device.get('lanIp'), device.get('switchProfileId'))
            device_data = MerakiSwitch(*device_values, *mr_values)
        elif "MR" in device.get('model'):
            mr_values = ('Access Point', device.get('lanIp'), device.get('beaconIdParams'))
            device_data = MerakiWireless(*device_values, *mr_values)
        elif "MT" in device.get('model'):
            mr_values = ('Sensor', device.get('lanIp'))
            device_data = MerakiSensor(*device_values, *mr_values)
        elif "MV" in device.get('model'):
            mr_values = ('Camera', device.get('lanIp'), device.get('wirelessMac'))
            device_data = MerakiCamera(*device_values, *mr_values)

        return device_data

    def get_organizations(self) -> [MerakiOrganization]:
        """
        :return:
        """
        organizations_data: [MerakiOrganization] = []
        for organization in self._get_organizations():
            organizations_data.append(
                MerakiOrganization(id=organization.get('id', ""), name=organization.get('name', ""),
                                   url=organization.get('url', ""), api=organization.get('api', ""))
            )
        return organizations_data

    def get_networks(self, organizationId: str) -> [MerakiNetwork]:
        """
        :param organizationId:
        :return:
        """
        networks_data: [MerakiNetwork] = []
        for network in self._get_networks(organizationId=organizationId):
            networks_data.append(MerakiNetwork(id=network.get('id', ""),
                                               organizationId=network.get('organizationId', ""),
                                               name=network.get('name', ""),
                                               productTypes=network.get('productTypes', ""),
                                               timeZone=network.get('timeZone', ""),
                                               tags=network.get('tags', ""),
                                               url=network.get('url', ""),
                                               notes=network.get('notes', ""),
                                               configTemplateId=network.get('configTemplateId', ""),
                                               isBoundToConfigTemplate=network.get('isBoundToConfigTemplate', ""),
                                               )
                                 )
        return networks_data

    def get_device(self, deviceSerial: str) -> MerakiDevice:
        """
        :param deviceSerial:
        :return:
        """
        device = self._get_device(deviceSerial=deviceSerial)
        device_data: MerakiDevice = self._device_factory(device)
        return device_data

    def get_network(self, networkId: str) -> MerakiNetwork:
        """
        :param networkId:
        :return:
        """
        network = self._get_network(networkId=networkId)
        network_data = MerakiNetwork(id=network.get('id', ""),
                                     organizationId=network.get('organizationId', ""),
                                     name=network.get('name', ""),
                                     productTypes=network.get('productTypes', ""),
                                     timeZone=network.get('timeZone', ""),
                                     tags=network.get('tags', ""),
                                     url=network.get('url', ""),
                                     notes=network.get('notes', ""),
                                     configTemplateId=network.get('configTemplateId', ""),
                                     isBoundToConfigTemplate=network.get('isBoundToConfigTemplate', ""))
        return network_data

    def get_network_devices(self, networkId: str, type='all') -> [MerakiDevice]:
        """
        :param networkId:
        :param type:
        :return:
        """
        devices = self._get_network_devices(networkId=networkId)
        device_data: [MerakiDevice] = []
        specific_devices: [MerakiDevice] = []

        for device in devices:
            device_data.append(self._device_factory(device))

        if type == 'all':
            return device_data

        for device in device_data:
            if device.productType == type:
                specific_devices.append(device)

        return specific_devices

from model.device import Device
from model.harddisk import Harddisk
from model.network import Network
from model.port import Port
from model.service import Service
from model.device_service import DeviceService
from model.device_network import DeviceNetwork
from model.network_port import NetworkPort


class DeviceRegisterHandler:

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.device = Device(self.db_conn)
        self.harddisk = Harddisk(self.db_conn)
        self.network = Network(self.db_conn)
        self.port = Port(self.db_conn)
        self.service = Service(self.db_conn)
        self.network_port = NetworkPort(self.db_conn)
        self.device_service = DeviceService(self.db_conn)
        self.device_network = DeviceNetwork(self.db_conn)

    def _add_device(self, device_data: dict) -> None:

        self.device.insert_device(device_data)

    def _add_network(self, network_data) -> None:

        self.network.add_network(network_data)
    
    def _add_harddisk(self, host_name, harddisk_data: list) -> None:

        for harddisk_item in harddisk_data:

            self.harddisk.add_hardisk(host_name, harddisk_item)

    def _add_port(self, port_data) -> None:
        
        self.port.add_port(port_data)
    
    def _add_network_port(self, network_ip, port_list):

        for port_data in port_list:

            self._add_port(port_data)
            self.network_port.add_network_port(
                self.network.get_network_id(network_ip),
                self.port.get_port_id(port_data["port"])
            )

    def _add_device_network(self, host_name, network_data_list):

        for network_data in network_data_list:
            
            self._add_network(network_data)
            self.device_network.add_device_network(
                self.device.get_device_id(host_name),
                self.network.get_network_id(network_data["ip_address"])
            )

    def _add_service(self, port_num, service_data: dict) -> None:

        self.service.add_service(port_num, service_data)

    def _add_device_service(self, host_name, service_data_list):

        for service_data in service_data_list:

            self._add_service(service_data["port"], service_data)
            self._add_device_service(
                self.device.get_device_id(host_name),
                self.service.get_service_id(service_data["service_name"])
            )

    def add_device(self, device_data_from_client: dict) -> None:

        host_name = device_data_from_client["host_name"]
        self._add_device(
            {
                key: device_data_from_client[key]
                for key in ["host_name", "cpu", "memory", "os_install"]
            }
        )
        
        self._add_harddisk(
            host_name, device_data_from_client["harddisk"]
        )

    def get_device(self, host_name):

        return self.device.get_device_id(host_name)
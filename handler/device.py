from model.device import Device
from model.harddisk import Harddisk
from model.network import Network
from model.port import Port
from model.service import Service
from model.device_service import DeviceService
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

    def _add_device(self, device_data: dict) -> None:

        self.device.insert_device(device_data)

    def _add_network(self, host_name, network_data: list) -> None:

        for network_item in network_data:

            self.network.add_network(host_name, network_item)
    
    def _add_harddisk(self, host_name, harddisk_data: list) -> None:

        for harddisk_item in harddisk_data:

            self.harddisk.add_hardisk(host_name, harddisk_item)

    def _add_port(self, port_data) -> None:
        #How do we deal with 1 IP with multiple ports?
        self.port.add_port(port_data)
    
    def _add_network_port(self, network_ip, port_list):

        for port_data in port_list:

            self._add_port(port_data)
            self.network_port.add_network_port(
                self.network.get_network_id(network_ip),
                self.port.get_port_id(port_data["port"])
            )

    def _add_service(self, port_num, service_data: dict) -> None:

        self.service.add_service(port_num, service_data)

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

        self._add_network(
            host_name, device_data_from_client["network"]
        )

        for service_data in device_data_from_client["service"]:
            self._add_service(service_data["port"], service_data)

    def get_device(self, host_name):

        return self.device.get_device_id(host_name)
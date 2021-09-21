from model.device import Device
from model.harddisk import Harddisk
from model.network import Network
from model.port import Port
from model.service import Service
from model.device_service import DeviceService
<<<<<<< HEAD
=======
from model.device_network import DeviceNetwork
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
from model.network_port import NetworkPort
from model.interface import Interface
from model.network_interface import NetworkInterface
from model.device_network import DeviceNetwork


class DeviceRegisterHandler:

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.device = Device(self.db_conn)
        self.harddisk = Harddisk(self.db_conn)
        self.network = Network(self.db_conn)
        self.port = Port(self.db_conn)
        self.service = Service(self.db_conn)
<<<<<<< HEAD
        self.interface = Interface(self.db_conn)
        self.network_interface = NetworkInterface(self.db_conn)
=======
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
        self.network_port = NetworkPort(self.db_conn)
        self.device_service = DeviceService(self.db_conn)
        self.device_network = DeviceNetwork(self.db_conn)

    def _add_device(self, device_data: dict) -> None:

        self.device.insert_device(device_data)

<<<<<<< HEAD
    def _add_network(self, network_data: list) -> None:

        for network_item in network_data:

            self.network.add_network(network_item)
=======
    def _add_network(self, network_data) -> None:

        self.network.add_network(network_data)
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
    
    def _add_harddisk(self, host_name, harddisk_data: list) -> None:

        for harddisk_item in harddisk_data:

            self.harddisk.add_hardisk(host_name, harddisk_item)

<<<<<<< HEAD
    def _add_port(self, port_data: list) -> None:
        #How do we deal with 1 IP with multiple ports?
=======
    def _add_port(self, port_data) -> None:
        
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
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

<<<<<<< HEAD
    def _add_interface(self, interface_data: dict) -> None:
=======
    def _add_device_service(self, host_name, service_data_list):

        for service_data in service_data_list:

            self._add_service(service_data["port"], service_data)
            self._add_device_service(
                self.device.get_device_id(host_name),
                self.service.get_service_id(service_data["service_name"])
            )

    def add_device(self, device_data_from_client: dict) -> None:
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de

        self.interface.add_interface(interface_data)

    def add_register(self, client_device_data: dict) -> None:

        host_name = client_device_data["host_name"]
        self._add_device(
            {
                key: client_device_data[key]
                for key in ["host_name", "cpu", "memory", "os_install"]
            }
        )
        
        self._add_harddisk(
            host_name, client_device_data["harddisk"]
        )

<<<<<<< HEAD
        mac_address_temp = None

        for interface, interface_data in client_device_data["network"].items():

            if interface_data["mac_address"]:

                mac_address_temp = interface["mac_address"]
                self._add_interface(
                    {
                        "interface_name": interface,
                        "mac_address": interface_data["mac_address"]
                    }
                )

            else:
                self._add_network(
                    {
                        "ip_address": interface_data["ip_address"],
                        "ip_version": interface_data["ip_type"][-1]
                    }
                )

                self.network_interface.add_network_interface(
                    interface_data["ip_address"], mac_address_temp
                )

                self.device_network.add_device_network(
                    interface_data["ip_address"], host_name
                )

        for port_data in client_device_data["ports"]:

            self._add_port(port_data)
            self.network_port.add_network_port(
                port_data["ip_address"], port_data["port"]
            )

        for service_data in client_device_data["services"]:
            self._add_service(service_data["port"], service_data)
            self.device_service.add_device_service(host_name, service_data["service_name"])

=======
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
    def get_device(self, host_name):

        return self.device.get_device_id(host_name)
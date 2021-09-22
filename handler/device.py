from model.device import Device
from model.harddisk import Harddisk
from model.network import Network
from model.port import Port
from model.service import Service
from model.device_service import DeviceService
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
        self.interface = Interface(self.db_conn)
        self.network_interface = NetworkInterface(self.db_conn)
        self.network_port = NetworkPort(self.db_conn)
        self.device_service = DeviceService(self.db_conn)
        self.device_network = DeviceNetwork(self.db_conn)

    def _add_device(self, device_data: dict) -> None:

        self.device.insert_device(device_data)

    def _add_network(self, network_data: dict) -> None:

        self.network.add_network(network_data)
    
    def _add_harddisk(self, host_name, harddisk_data: list) -> None:

        for harddisk_item in harddisk_data:

            self.harddisk.add_hardisk(host_name, harddisk_item)

    def _add_ports(self, ports_data: list) -> None:
        #How do we deal with 1 IP with multiple ports?
        for port_data in ports_data:
            self._add_port(port_data)
            self.network_port.add_network_port(
                self.network.get_network_id(port_data["ip_address"])["id"], 
                self.port.get_port_id(port_data["port"])["id"]
            )
    
    def _add_services(self, host_name, services_data: dict) -> None:

        for service_data in services_data:
            self._add_service(service_data["port"], service_data)
            self.device_service.add_device_service(
                self.device.get_device_id(host_name)["id"], 
                self.service.get_service_id(service_data["service_name"])["id"]
            )
        

    def _add_interface(self, interface_data: dict) -> None:

        self.interface.add_interface(interface_data)

    def add_register(self, client_device_data: dict) -> None:

        host_name = client_device_data["host_name"]

        self._add_device(
            {
                key: client_device_data[key]
                for key in ["host_name", "cpu", "memory", "os_install"]
            }
        )

        self._add_harddisk(host_name, client_device_data["harddisc"])

        mac_address_temp = None

        for interface, interface_data in client_device_data["network"].items():

            for interface_d in interface_data:
                
                if interface_d["mac_address"]:
                    mac_address_temp = interface_d["mac_address"]
                    
                    self._add_interface(
                        {
                            "interface_name": interface,
                            "mac_address": interface_d["mac_address"]
                        }
                    )

                else:

                    if interface_d["ip_address"] == "127.0.0.1" and (not interface_d["mac_address"]):

                        mac_address_temp = "00:00:00:00:00:00"

                        self._add_interface(
                            {
                                "interface_name": interface,
                                "mac_address": mac_address_temp
                            }
                        )

                    self._add_network(
                        {
                            "ip_address": interface_d["ip_address"],
                            "ip_version": interface_d["ip_type"][-1]
                        }
                    )

                    self.network_interface.add_network_interface(
                        self.network.get_network_id(interface_d["ip_address"])["id"], 
                        self.interface.get_interface_id(mac_address_temp)["id"]
                    )

                    self.device_network.add_device_network(
                        self.device.get_device_id(host_name)["id"],
                        self.network.get_network_id(interface_d["ip_address"])["id"], 
                    )

        self._add_ports(client_device_data["ports"])
        self._add_services(host_name, client_device_data["services"])

    def get_device(self, host_name):

        return self.device.get_device_id(host_name)
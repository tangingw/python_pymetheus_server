

class Device:

    def __init__(self):

        self.device_dict = {
            "host_name": None,
            "cpu": None,
            "memory": None,
            "os_install": None,
            "harddisk": None,
            "service": None,
            "ports": None,
            "network": None
        }
    
    def add_attribute(self, attribute_name, attribute_value):

        self.device_dict[attribute_name] = attribute_value
    
    def get_attributes(self):

        return self.device_dict


"""
device_data_struct = {
    "host_name":
    "cpu":
    "memory":
    "os_install":
    "harddisk": [
        {
            "name":
            "mount_point":
            "fs_type":
            "size":
        }

    ]
    "network: [
        {
            "ip_address":
            "ip_version":
        }
    ],
    "port: [
        {
            "host_name":
            "ip_address":
            "port":
            "port_desc"
        }
    ],
    "service: [
        {
            "name":
            "url":
            "service_desc":
            "service_type":
            "network_ip":
            "port":
            "host_name":
        }
    ]
}
event_data_struct = {
    "monitoring_type": 
    "event_status":
    "event_message":
    "event_value":
    "item_monitored": {
        "item_type":
        "item_name":
    }
}
"""


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
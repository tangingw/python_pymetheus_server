from model.heartbeat import HeartBeat


class HeartBeatHandler:

    def __init__(self, db_conn):

        self.db_conn = db_conn
        self.heart_beat = HeartBeat(self.db_conn)

    def add_heartbeat(self, device_name):

        device_in_heartbeat = self.heart_beat.get_heartbeat_device(device_name)

        if not device_in_heartbeat:

            self.heart_beat.add_heartbeat(device_name)
        
    def update_heartbeat(self, device_name):

        self.heart_beat.update_heartbeat(device_name)

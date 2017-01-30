from arbalet.config import ConfigReader
from arbalet.core import Rate
from arbalet.dbus import DBusClient
from arbalet.events import CapacitiveTouchEvents, SystemEvents


class EventServer(object):
    """
    Arbalet Events Server
    Initializes the available sensors and publishes them on D-Bus
    """
    def __init__(self, parser):
        self.args = parser.parse_args()
        config_reader = ConfigReader()
        self.config = config_reader.hardware
        self.joystick = config_reader.joystick
        self.sensors = [CapacitiveTouchEvents(),
                        SystemEvents()]
        self.rate = Rate(100)
        self.running = False
        self.bus = DBusClient(event_publisher=True)

    def work(self):
        for sensor in self.sensors:
            for event in sensor.get():
                self.bus.events.publish(event)

    def run(self):
        self.running = True
        while self.running:
            try:
                self.work()
                self.rate.sleep()
            except KeyboardInterrupt:
                print("[Arbalet Event server] Shutdown initiated via SIGINT, closing...")
                self.running = False
                self.bus.close()


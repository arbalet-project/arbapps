import argparse
from .server import EventServer
from arbalet.core.config import get_config_parser

parser = argparse.ArgumentParser(description='Arbalet Event Manager. '
                                             'Gathers all events from sensors, i.e. keyboards, joysticks, touch sensors, '
                                             'web interfaces and publishes them on the Arbalet D-BUS.'
                                             'Interactive applications will not properly work without running Event Manager.')
parser = get_config_parser(parser)
EventServer(parser).run()
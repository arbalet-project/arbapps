from .proxy import Proxy
import argparse

parser = argparse.ArgumentParser(description='Arbalet D-Bus proxy. '
                                             'Bind and listen to an ingoing port and replicate messages on an outgoing connection'
                                             'Exchanged messages are part of the Arbalet Data Bus')
Proxy(argparse).run()
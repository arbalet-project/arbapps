import argparse
from .tester import SimpleTester

parser = argparse.ArgumentParser(description='Light every pixel one by one for hardware address debuging purposes. Columns are filled in first progressively, then rows. All pixels in a column share the same color.')
SimpleTester(parser).start()
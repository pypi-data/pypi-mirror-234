import sys
import time
from lager import gdb

def main():
    halt = sys.argv[1] == 'True'
    resp = gdb.reset(halt)
    for item in resp:
        if item['message'] is None and item['payload'] is not None and item['stream'] == 'stdout':
            print(item['payload'], end='')


if __name__ == '__main__':
    main()

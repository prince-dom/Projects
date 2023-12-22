from argparse import ArgumentParser
import socket
from threading import Thread
from time import time

open_ports = []

def scan_port():
    while True:
        try:
            s = socket.socket()
            s.settimeout(1)
            port = next(ports)
            s.connect((arguments.ip, port))
            open_ports.append(port)
            if arguments.verbose:
                print(f'\r{open_ports}', end='')
        except (ConnectionRefusedError, socket.timeout):
            continue
        except StopIteration:
            break



def prepare_args():
    parser = ArgumentParser(description='Python Based Fast  Port Scanner', usage='%(prog)s 127.0.0.1', epilog='Example - %(prog)s <ip>')
    parser.add_argument(metavar='ip', dest='ip', help='host to scan')
    parser.add_argument('-s', '--start', metavar='', dest='start', type=int, help='starting port', default=1)
    parser.add_argument('-e', '--end', metavar='', dest='end', type=int, help='ending port', default=65535)
    parser.add_argument('-t', '--threads', metavar='', dest='threads', type=int, help='threads', default=500)
    parser.add_argument('-V', '--verbose', dest='verbose', action='store_true', help='verbose mode')
    parser.add_argument('-v', '--version', action='version' , version='%(prog)s 1.0,', help='show version')
    args = parser.parse_args()
    return args

def prepare_ports(start:int, end:int):
    for port in range(start, end+1):
        yield port

def prepare_threads(threads:int):
    thread_list= []
    for _ in range(threads+1):
        thread_list.append(Thread(target=scan_port))
    
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()    

if __name__=='__main__':
    arguments = prepare_args()
    ports = prepare_ports(arguments.start, arguments.end)
    start_time = time()
    prepare_threads(arguments.threads)
    end_time = time()
    if arguments.verbose:
        print()
    print(f'open ports founds - {open_ports}')
    print(f'Time taken: {end_time - start_time:.2f} seconds')


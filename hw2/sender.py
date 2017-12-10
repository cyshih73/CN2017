import socket
import argparse
import time


def main(args):
    address = (args.ip, int(args.port))
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(args.input, 'rb') as file:
        while True:
            msg = file.read(1024)
            if not msg:
                break
            receiver.sendto(msg, address)
            print("sent 1024")
            time.sleep(0.1)

        receiver.close()

def parse_args():
    parser = argparse.ArgumentParser(description='CN2017 HW2 sender')
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--input')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

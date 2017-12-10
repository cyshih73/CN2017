import socket
import argparse
#ip = int("10.0.0.1")
port = int("3001")

def main(args):
    address = ("127.0.0.2", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    while True:
        data, addr = s.recvfrom(2048)
        if not data:
            print("client has exist")
            break
        print("received:", data, "from", addr)

    s.close()



def parse_args():
    parser = argparse.ArgumentParser(description='Twitter text sentiment data preprocess.')
    """
    parser.add_argument('--sender_ip')
    parser.add_argument('--sender_port')

    parser.add_argument('--receiver_ip')
    parser.add_argument('--receiver_port')
    parser.add_argument('--loss_rate')
    """
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

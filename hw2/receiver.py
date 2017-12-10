import socket

def main(args):
    address = ('127.0.0.1', 31500)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)

    while True:

        data, addr = s.recvfrom(2048)
        if not data:
            print "client has exist"
            break
        print "received:", data, "from", addr
        #send ack

    s.close()

def parse_args():
    parser = argparse.ArgumentParser(description='CN2017 HW2 receiver')
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--output')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

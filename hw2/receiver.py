import socket
import argparse
import time
import pickle

self_ip = "127.0.0.4"
self_port = 3004

def main(args):
    buffer_size = 32

    address = (self_ip, args.port)
    agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    agent.settimeout(0)
    agent.bind((self_ip, self_port))
    acking = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    while True:
        try:
            pickle_msg, _ = agent.recvfrom(2048)
            msg = pickle.loads(pickle_msg)
            print("recv", msg['type'], '#'+str(msg['seq']+1), sep="\t")

            if msg['type'] == 'fin':
                ack = {'type': 'finack', 'seq': msg['seq']}
            else:
                ack = {'type': 'ack', 'seq': msg['seq']}

            pickle_ack = pickle.dumps(ack, -1)
            acking.sendto(pickle_ack, (args.ip, int(args.port)))
            print("send", ack['type'], '#'+str(ack['seq']+1), sep="\t")

            #final data
            if ack['type'] == 'finack':
                break

        except socket.error:
            pass

    agent.close()
    acking.close()

#python receiver.py --ip 127.0.0.3 --port 3002 --output result.txt
def parse_args():
    parser = argparse.ArgumentParser(description='CN2017 HW2 receiver')
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--output')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

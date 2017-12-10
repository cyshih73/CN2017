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

    data = []
    acked, written = -1, -1

    with open(args.output, 'wb') as f:
        resending = -1
        while True:
            try:
                pickle_msg, _ = agent.recvfrom(2048)
                msg = pickle.loads(pickle_msg)
                if msg['seq'] == acked + 1 and (acked - written) < buffer_size:
                    print("recv", msg['type'], '#'+str(msg['seq']+1), sep="\t")
                    data.append(msg['data'])
                    acked = msg['seq']
                else:
                    print("drop", msg['type'], '#'+str(msg['seq']+1), sep="\t")

                #ack processing
                if msg['type'] == 'fin' and resending+1 - acked == 0:
                    ack = {'type': 'finack', 'seq': acked}
                else:
                    resending = msg['seq']
                    ack = {'type': 'ack', 'seq': acked}

                pickle_ack = pickle.dumps(ack, -1)
                acking.sendto(pickle_ack, (args.ip, int(args.port)))
                if ack['type'] == 'finack':
                    print("send", ack['type'], sep="\t")
                    break
                else:
                    print("send", ack['type'], '#'+str(ack['seq']+1), sep="\t")

            except socket.error:
                pass

            #flush
            if acked - written >= buffer_size:
                print("flush")
                for i in range(32):
                    if data[i]:
                        f.write(data[i])
                data = []
                written = acked

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

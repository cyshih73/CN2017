import socket
import argparse
import time
import pickle

self_ip = "127.0.0.2"
self_port = 3003

def main(args):
    threshold = 16
    timeout = 2 #timeout setting <1s

    agent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    acking = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    acking.settimeout(0)
    acking.bind((self_ip, self_port))

    #data preprocessing
    data = []
    with open(args.input, 'rb') as file:
        while 1:
            msg = file.read(1024)
            if not msg:
                break
            data.append(msg)


    acked = -1
    sent = -1
    now_timeout = time.time()
    while True and acked < len(data):
        #sending data
        if sent - acked < threshold and sent < len(data) - 1:
            sent = sent + 1
            if sent == len(data) - 1:
                msg = {'type': 'fin', 'seq': sent, 'data': data[sent]}
            else:
                msg = {'type': 'data', 'seq': sent, 'data': data[sent]}

            pickle_msg = pickle.dumps(msg, -1)
            agent.sendto(pickle_msg, (args.ip, int(args.port)))
            print("send", msg['type'], '#'+str(msg['seq']+1), sep="\t")

            #time.sleep(0.1)

        #receiving acks
        try:
            pickle_ack, _ = acking.recvfrom(2048)
            ack =  pickle.loads(pickle_ack)
            print("recv", ack['type'], '#'+str(ack['seq']+1), sep="\t")
            #final data
            if ack['type'] == 'finack':
                break
            if acked != ack['seq']:
                acked = ack['seq']
                now_timeout = time.time()
        except socket.error:
            pass

        #timeout resend
        if time.time() - now_timeout >= timeout:
            sent = acked
            now_timeout = time.time()

    agent.close()
    acking.close()

#python sender.py --ip 127.0.0.3 --port 3001 --input
def parse_args():
    parser = argparse.ArgumentParser(description='CN2017 HW2 sender')
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--input')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

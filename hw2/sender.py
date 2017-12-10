import socket
import argparse
import time
import pickle

self_ip = "127.0.0.2"
self_port = 3003

def main(args):
    threshold = 16
    windows = 1
    timeout = 0.7 #timeout setting <1s

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

    acked, resend, sent = -1, -1, -1
    breakpoint = 0

    now_timeout = time.time()
    print(len(data))

    while acked < len(data):
        #sending data
        if sent < len(data) - 1:
            if sent == acked:
                for i in range(windows):
                    sent = sent + 1
                    #final data
                    if sent == len(data) - 1:
                        print("FINAL DATA")
                        msg = {'type': 'fin', 'seq': sent, 'data': data[sent]}
                        breakpoint = 1
                    else:
                        msg = {'type': 'data', 'seq': sent, 'data': data[sent]}

                    pickle_msg = pickle.dumps(msg, -1)
                    agent.sendto(pickle_msg, (args.ip, int(args.port)))
                    if sent < resend:
                        print("resnd", msg['type'], '#'+str(msg['seq']+1)+',', 'winSize = '+str(windows), sep="\t")
                    else:
                        print("send", msg['type'], '#'+str(msg['seq']+1)+',', 'winSize = '+str(windows), sep="\t")
                        resend = sent
                    if breakpoint == 1:
                        break

                    #time.sleep(0.1)
                #slow start
                if windows < threshold:
                    windows = windows * 2
                else:
                    windows = windows + 1

        #receiving acks
        out_of_ack, get_out = 0, 0
        while out_of_ack == 0:
            try:
                pickle_ack, _ = acking.recvfrom(2048)
                ack =  pickle.loads(pickle_ack)
                print("recv", ack['type'], '#'+str(ack['seq']+1), sep="\t")
                #final data
                if ack['type'] == 'finack':
                    get_out = 1
                    break
                if acked != ack['seq']:
                    acked = ack['seq']
                    now_timeout = time.time()

            except socket.error:
                out_of_ack = 1

        if get_out != 0:
            break
        #timeout resend
        if time.time() - now_timeout >= timeout:
            threshold = max(windows/2, 1)
            windows = 1
            print("time", "out,", "", "threshold = "+str(threshold), sep='\t')
            sent = acked
            breakpoint = 0
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

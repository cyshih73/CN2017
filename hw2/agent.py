import socket
import argparse
import pickle
import random

#config
self_ip = "127.0.0.3"
self_port_s = 3001
self_port_r = 3002

#python agent.py --sender_ip 127.0.0.2 --sender_port 3003 --receiver_ip 127.0.0.4 --receiver_port 3004 --loss_rate 0.1
def main(args):
    sender_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_receive.bind((self_ip, self_port_s))
    sender_receive.settimeout(0)

    receiver_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_receive.bind((self_ip, self_port_r))
    receiver_receive.settimeout(0)

    num_packets = 0
    lost_packets = 0
    while True:
        out_of_data, out_of_ack, get_out = 0, 0, 0
        #data
        while out_of_data == 0:
            try:
                pickle_msg, _ = sender_receive.recvfrom(2048)
                msg =  pickle.loads(pickle_msg)
                print("get",msg['type'], '#'+str(msg['seq']+1), sep="\t")
                num_packets = num_packets + 1
                if msg['type'] == 'fin':
                    print("get",msg['type'], sep="\t")
                    receiver_send.sendto(pickle_msg, (args.receiver_ip, int(args.receiver_port)))
                    print("fwd",msg['type'], sep="\t")
                    break

                #random drop
                YN = 1
                if args.loss_rate != 0: YN = (random.randint(1,2147483646) % (1/float(args.loss_rate)))
                if  YN != 0:
                    receiver_send.sendto(pickle_msg, (args.receiver_ip, int(args.receiver_port)))
                    loss_rate = "{0:.4f}".format(lost_packets/num_packets)
                    print("fwd",msg['type'], '#'+str(msg['seq']+1)+',', 'loss rate = '+loss_rate, sep="\t")
                else:
                    lost_packets = lost_packets + 1
                    loss_rate = "{0:.4f}".format(lost_packets/num_packets)
                    print("drop",msg['type'], '#'+str(msg['seq']+1)+',', 'loss rate = '+loss_rate, sep="\t")

            except socket.error: out_of_data = 1

        #ack
        while out_of_ack == 0:
            try:
                pickle_ack, _ = receiver_receive.recvfrom(2048)
                ack =  pickle.loads(pickle_ack)
                if ack['type'] == 'finack':
                    print("get",ack['type'], sep="\t")
                    sender_send.sendto(pickle_ack, (args.sender_ip, int(args.sender_port)))
                    print("fwd",ack['type'], sep="\t")
                    get_out = 1
                print("get",ack['type'], '#'+str(ack['seq']+1), sep="\t")

                sender_send.sendto(pickle_ack, (args.sender_ip, int(args.sender_port)))
                print("fwd",ack['type'], '#'+str(ack['seq']+1), sep="\t")
            except socket.error: out_of_ack = 1
        if get_out != 0: break #end

    sender_send.close()
    sender_receive.close()
    receiver_send.close()
    receiver_receive.close()

def parse_args():
    parser = argparse.ArgumentParser(description='CN2017 HW2 agent')
    parser.add_argument('--sender_ip')
    parser.add_argument('--sender_port')
    parser.add_argument('--receiver_ip')
    parser.add_argument('--receiver_port')
    parser.add_argument('--loss_rate')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

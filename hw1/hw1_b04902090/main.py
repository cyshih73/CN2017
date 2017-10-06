import sys
import time
import socket 
server="irc.freenode.net" 
botnick="ROBOTb04902090" 
channel="#CN2017_b04902090" 

def feipei(ip):
	iplist = []
	if len(ip)>12 or len(ip) < 4:
		return iplist
	a,b,c,d=0,0,0,0
	for i in range(0,3):
		for j in range(i+1,i+4):
			for k in range(j+1,j+4):
				a, b, c, d= ip[0:i+1], ip[i+1:j+1], ip[j+1:k+1], ip[k+1:]
				result = "%s.%s.%s.%s"%(a,b,c,d)
				try:
					tempa = socket.inet_aton(result)
					if socket.inet_ntoa(tempa) == result :
						iplist.append(result)
				except socket.error:
					a,b,c,d=0,0,0,0
	return iplist

def main():
	fp = open("./config",'r')
	line = fp.read()
	channel = line[line.find('\'')+1:-1]
	print("channel = "+channel+"")
	#Establish connection 
	irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	irc.connect((server, 6667))
	time.sleep(1) 
	irc.send("USER "+botnick+" "+botnick+" "+botnick+" :Hello!\r\n")
	print("send USER")
	time.sleep(1) 
	irc.send("NICK "+botnick+"\n")
	print("send NICK")
	time.sleep(1) 
	irc.send("JOIN "+channel+" \r\n") 
	print("send JOIN")
	time.sleep(1)
	irc.send("PRIVMSG "+channel+" :Hello! I am robot.\r\n")

	while True :
		time.sleep(0.1) 
		try: 
			Msg = irc.recv(2040)
			print(Msg) 
		except Exception: 
			pass 
		# Pingpong
		if Msg.find("PING")!=-1:
			print("PINGED")
			irc.send("PONG "+Msg.split()[1]+"\r\n") 
		# @repeat
		if Msg.lower().find(":@repeat ")!=-1:
			reply = Msg[Msg.find("@repeat")+len("@repeat ") :]
			irc.send("PRIVMSG "+channel+" :"+reply+"\r\n")
		# @convert
		if Msg.lower().find(":@convert ")!=-1:
			reply = Msg[Msg.find("@convert")+len("@convert ") :]
			if reply.find("0x")!=-1:
				reply = int(reply, 16)
			else:
				reply = hex(int(reply))
			irc.send("PRIVMSG "+channel+" :"+str(reply)+"\r\n")
		# @ip
		if Msg.lower().find(":@ip ")!=-1:
			reply = Msg[Msg.find("@ip")+len("@ip ") :]
			iplist = feipei(str(int(reply)))
			irc.send("PRIVMSG "+channel+" :"+str(len(iplist))+"\r\n")
			for i in range(0,len(iplist)):
				irc.send("PRIVMSG "+channel+" :"+iplist[i]+"\r\n")
				time.sleep(0.7)
		# @help
		if Msg.lower().find(":@help")!=-1:
			irc.send("PRIVMSG "+channel+" : @repeat <Message>\r\n")
			irc.send("PRIVMSG "+channel+" : @convert <Number>\r\n")
			irc.send("PRIVMSG "+channel+" : @ip <String>\r\n")
		Msg, reply="", ""
	input()

if __name__ == '__main__':
    main()
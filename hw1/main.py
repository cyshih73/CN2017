import sys
import time
import socket 
server="irc.freenode.net" 
botnick="ROBOT" 
channel="#CN2017Shihehe" 

#Establish connection 
IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IRCSocket.connect( ( server, 6667 ) )
time.sleep(1) 
Msg = "JOIN "+channel+" \r\n"
IRCSocket.send(bytes( Msg ,'utf8')) 
"""
IRCSocket.sendall("USER "+botnick+" "+botnick+" "+botnick+" :Hello! I am a test bot!\r\n") 
time.sleep(1) 
IRCSocket.send("NICK "+botnick+"\n") 
time.sleep(1) 
Msg = "JOIN "+channel+" \r\n"
IRCSocket.send(bytes( Msg ,'utf8')) 
"""
IRCSocket.setblocking(1) 
while True :
	time.sleep(0.1) 
	try: 
		IRCMsg = IRCSocket.recv( 2040 )
		print(IRCMsg) 
	except Exception: 
		pass 
	if IRCMsg.find(b"PING")!=-1:
		IRCSocket.send(byte("PONG "+text.split()[1]+"\r\n")) 
	if IRCMsg.lower().find(b":@hi")!=-1: 
		IRCSocket.send(byte("PRIVMSG "+channel+" :Hello!\r\n")) 
	text=""
input()
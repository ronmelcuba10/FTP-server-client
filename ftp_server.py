from socket import *
import threading 
import sys 
import traceback  
import errno
import os
import pdb
import configparser
import ftp_server_commands as c
import ftp_server_messages as msgs

## global variables
tList = []
thread_info = {} 
NEW_LINE = "\r\n"
CONFIG_PATH = 'ftpserver/conf/fsys.cfg'
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)
RECV_BUFFER = 0
USER_DATA_FILE = ""
log_file = ""
FTP_ROOT = ""
STOPPED = False
serverPort = 0
dp_min = 0
dp_max = 0
maximum_connected = 20


#
def clientThread(connectionSocket, addr):
    global thread_info
    global dp_min
    global dp_max
    try:
        print ("Thread Client Entering Now...")
        print (addr)
        print ("TID = ",threading.current_thread())
        connectionSocket.send(FTP_ROOT.encode())
        th_id = threading.current_thread().ident
        dp_min = int(defaultconfig("DATA_PORT_RANGE_MIN"))
        dp_max = int(defaultconfig("DATA_PORT_RANGE_MAX"))
        mode = defaultconfig("ftp_mode")
        root = os.getcwd()

        server_session = c.Session(th_id,connectionSocket,FTP_ROOT,USER_DATA_FILE,log_file,dp_min,dp_max,root,mode)
        thread_info [th_id] = server_session
        i = 0
        while not STOPPED:
            msg = connectionSocket.recv(RECV_BUFFER).decode().strip()
            tokens = msg.split()
            if(not tokens):
            	continue

            command = tokens[0]
            if(server_session.hascommand(command)):
                server_session.run_command(tokens)
            else:
                strm = "You said what? " + msg
                print_console(strm)
                server_session.send(strm)

            if (STOPPED):
        	    connectionSocket.recv(RECV_BUFFER)
        	    strm = "Server stopped working. Sorry for the inconvenience"
        	    connectionSocket.send(strm.encode())



    except OSError as e:
        # A socket error
        print_console("Socket error:",e) 
        

#
def defaultconfig(name):
    return CONFIG["DEFAULT"][name]

#
def joinAll():
    global tList
    for t in tList:
        t.join() 

#
def setglobals():
    global RECV_BUFFER
    global USER_DATA_FILE
    global FTP_ROOT
    global FTP_SERVER
    global log_file
    FTP_SERVER = os.getcwd()
    FTP_ROOT = os.path.join(FTP_SERVER,defaultconfig('ftp_root'))
    USER_DATA_FILE = os.path.join(FTP_SERVER,defaultconfig('user_data_file'))
    RECV_BUFFER = int(defaultconfig('RECV_BUFFER'))
    log_file = os.path.join(FTP_SERVER,defaultconfig('FTP_LOG'))

#
def check_stop_command():
	global thread_info
	global tList

	return any ( thread_info[tl.ident].ADMIN_STOP  for tl in tList )

#
def quitted():
	global tList
	global thread_info
	for t in tList:
		session_info = thread_info.get(t.ident,None)
		if(session_info == None):
			continue
		if(session_info.ADMIN_QUIT):
			return False
	return True

#
def is_int(num):
    try: 
        int(num)
        return True
    except ValueError:
        return False

#
def runmax(tokens):
    global maximum_connected
    maxc = tokens[1]
    if(is_int(maxc)):
        maximum_connected = maxc
        print_console("Maximum of connected users is: ", maxc)
        return
    print_console("not a valid number")

#
def rundpr(tokens):
    global dp_min
    global dp_max
    ports = tokens[1].split("-")
    if(len(ports) != 2):
        print_console("Invalid port range")
        return
    if(is_int(ports[0]) and is_int(ports[1])):
        pmin = int(ports[0])
        pmax = int(ports[1])
        if(pmin > pmax):
            print_console("Invalid port range")
            return
        dp_min = pmin
        dp_max = pmax
        print_console("new ports ranges is " + str(dp_min) + " - " + str(dp_max))
        return
    print_console("Not valid port numbers")

#
def runport(tokens):
    global serverPort
    port = tokens[1]
    if(not is_int(port)):
        print("Invalid port number")
        return
    serverPort = int(port)
    print("Server port changed to: ", serverPort)

#
def runconfiguratio(tokens=None):
	global CONFIG_PATH
	path = os.getcwd()
	conf_path = os.path.join(path,CONFIG_PATH)
	print_console(conf_path)
	return

#
def runuserdb(tokens=None):
	global USER_DATA_FILE
	path = os.getcwd()
	user_path = os.path.join(path,USER_DATA_FILE)
	print_console(user_path)
	return

#
def validate(tokens):
	if(tokens == []):
		return False

	if(len(tokens)==1 and tokens[0] in ["-configuration","-userdb"]):
		return True
	if(len(tokens)>1 and tokens[0] in ["-port","-max","-dpr","-configuration","-userdb"]):
		return True
	return False


#	
def admin_console():
    while True:
        line = input("ADMIN>")
        if(line == ""):
        	continue
        tokens = line.split()
        if(not validate(tokens)):
            print("not a valid command")
            continue
        cmd = tokens[0]
        if(cmd == "-port"):
            runport(tokens)
        elif (cmd == "-max"):
            runmax(tokens)
        elif(cmd == "-dpr"):
            rundpr(tokens)
        elif (cmd == "-configuration"):
            runconfiguratio()
        elif(cmd == "-userdb"):
            runuserdb()
        else:
            print("not a valid command")

#
def admin_thread():
    global STOPPED
    serviceSocket = socket(AF_INET,SOCK_STREAM)
    serviceSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serviceSocket.bind(('',int(defaultconfig('SERVICE_PORT'))))
    serviceSocket.listen(1)
    while True:
    	connectionSocket, addr = serviceSocket.accept()
    	cmd = connectionSocket.recv(RECV_BUFFER)
    	STOPPED = cmd.decode() == "STOP"
    	if(STOPPED):
    		print_console("Server service paused")
    	else:
    		print_console("Server service resumed")

#
def print_console(msg=None): 
	if (msg):
		print(msg)
	sys.stdout.write("ADMIN>")
	sys.stdout.flush()

#
def main():
    try:
        global tList
        global thread_info
        global STOPPED
        global maximum_connected
        setglobals()
        serverPort = int(defaultconfig('DATA_PORT_FTP_SERVER'))
        maximum_connected = int(defaultconfig("MAX_USER_SUPPORT"))
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(15)
        print(defaultconfig("WELCOME_MSG"))
        at = threading.Thread(target=admin_console,args=())
        at.start()
        tList.append(at)
        at = threading.Thread(target=admin_thread,args=())
        at.start()
        tList.append(at)
        while True:
            if(len(tList)<maximum_connected and not STOPPED):
                connectionSocket, addr = serverSocket.accept()
                t = threading.Thread(target=clientThread,args=(connectionSocket,addr))
                t.start()
                tList.append(t)
                print("Thread started")
                print_console("Waiting for another connection")
            
    except KeyboardInterrupt:
        print_console ("Keyboard Interrupt. Time to say goodbye!!!")
    finally:
        joinAll()
    print("The end")
    sys.exit(0) 


if __name__ == "__main__":
    # execute only if run as a script
    main()

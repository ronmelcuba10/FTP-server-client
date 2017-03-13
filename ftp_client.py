import sys
import configparser
import os
import time
import ftp_commands as cmds
import ftp_client_commands as c
from socket import *

CONFIG_FILE = 'ftp_client.cfg'
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_FILE)

#Global constants
USAGE = "usage: Python ftp hostname [username] [password]"

MSG_EMPTY = ""
RECV_BUFFER = 1024
FTP_PORT = 21
NEW_LINE = "\r\n"
DIVIDER = "#"
next_data_port = 1



#global 
username = ""
password = "" 
hostname = "cnt4713.cs.fiu.edu"

def defaultconfig(name):
    return CONFIG['DEFAULT'][name]    

def print_initial_greeting(hostname):
    print("********************************************************************")
    print("**                      ACTIVE/PASSIVE MODE                       **")
    print("********************************************************************")
    print("********************************************************************")
    print("***   This is an FTP application that includes the client and    ***")
    print("***   the server. In both, server and client, the session is     ***")
    print("***   an object. The server is mutltithreaded         			***")
    print("***   															***")
    print("***  															***")
    print("********************************************************************")
    print("********************************************************************")
    print("*****    for help type Help|?   									***")
    print("********************************************************************")
    print("********************************************************************")
    print("********************************************************************")
    print("********************************************************************")
    print("****                                                             ***")
    print("****  For test purpose there is an extra command                 ***")
    print("****                                                             ***")
    print("****  test + [start|dist]    starts creating directories         ***")
    print("****                         and moving/copying files            ***")
    print("****                         on the remote directory             ***")
    print("****                                                             ***")
    print("****  test + [clean|clear]   returns to the starting point       ***")
    print("****                                                             ***")
    print("****  test + [*]             will carry a list of command        ***")
    print("****                                                             ***")
    print("****                                                             ***")
    print("********************************************************************")
    print("********************************************************************")

    print(("You will be connected to host:" + hostname))
    print("Type HELP for more information")
    print("Commands are NOT case sensitive\n")  

    
def ftp_connecthost(hostname,default_ftp_port):
    global CONFIG
    ftp_socket = socket(AF_INET, SOCK_STREAM)
    #to reuse socket faster. It has very little consequence for ftp client.
    ftp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ftp_socket.connect((hostname, default_ftp_port)) 
    working_directory = ftp_socket.recv(RECV_BUFFER).decode()
    print ("Working directory : ", working_directory)
    return ftp_socket


def run_session_commands(session,command,tokens):   
    if(session.hascommand(command)):
        session.run_command(tokens)
    else:
        print("Unknown command")

def test_session_commands(session,command,tokens):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    option = tokens[1].upper()
    if(option in ["DIST","START"]):
        test_file_path = defaultconfig("test_file_distribute")
    elif(option in ["CLEAN","CLEAR"]): 
        test_file_path = defaultconfig("test_file_clean_up")
    else:
        test_file_path = defaultconfig("test_general")

    test_file_path = os.path.join(os.getcwd(),test_file_path)

    with open(test_file_path,'r') as test_file:
        print("Testing..........................")
        for line in test_file:
            line = line.strip()
            if(line == ""):
                continue
            tokens = line.split()

            if(tokens[0] == "#"):
                continue
            cmd = tokens[0].upper()
            print("\nExecuting command ---> :   "," ".join(tokens))
            run_session_commands(session,cmd,tokens)
            time.sleep(0.2) 

        print("...................finish testing") 

        # end of tests section 


#entry point main()
def main():
    global username
    global password
    global hostname 
    
    logged_on = False
    logon_ready = False
    print("FTP Client v1.0")
    if (len(sys.argv) < 2):
         print(USAGE)
    if (len(sys.argv) == 2):
        hostname = sys.argv[1]
    if (len(sys.argv) == 4):
        username = sys.argv[2]
        password = sys.argv[3]
        logon_ready = True


    if (logon_ready):
        logged_on = login(username,password,ftp_socket)

    print_initial_greeting(hostname)

    dp_min = int(defaultconfig("DATA_PORT_MIN"))
    dp_max = int(defaultconfig("DATA_PORT_MAX"))
    verbose = defaultconfig("DEFAULT_VERBOSE_MODE") == "ON"
    f_FTP = int(defaultconfig("DEFAULT_FTP_PORT"))
    ftp_socket = ftp_connecthost(hostname,f_FTP)
    log_file = defaultconfig("DEFAULT_LOG_FILE")
    app_path = os.getcwd()
    
    client_session = c.Session(ftp_socket,dp_min,dp_max,logged_on,f_FTP,log_file,app_path)
    if (logon_ready):
        client_session.login(username,password)

    keep_running = True
    while keep_running:
        try:
            rinput = input("FTP>")

            if (rinput is None or rinput.strip() == ''):
                continue
            tokens = rinput.split()
            command = tokens[0].upper()

            if(command == "TEST" and len(tokens)>1):
                test_session_commands(client_session,command,tokens)
            else:
                run_session_commands(client_session,command,tokens)

        except OSError as e:
        # A socket error
            print("Socket error:",e)
            strError = str(e)
            #this exits but it is better to recover
            if (strError.find("[Errno 32]") >= 0): 
                sys.exit()
    #print ftp_recv
    try:
        ftp_socket.close()
        print("Thank you for using FTP 1.0")
    except OSError as e:
        print("Socket error:",e)
    sys.exit()

main()

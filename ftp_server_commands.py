
import os
import shutil
import sys
import datetime
import subprocess
import errno
import time
import ftp_commands as cmds
import ftp_server_messages as msgs
from socket import *


NEW_LINE = "\r\n"
ADMINISTRATOR = "admin"
DIVIDER = "#"
USER = "user"
ANONYMOUS_USER = "ANONYMOUS"
START_TOKEN = "START"
STOP_TOKEN = "STOP"
QUIT_TOKEN = "QUIT"
RECV_BUFFER = 1024

class Session:

    #
    def __init__(self, th_id,ftp_socket,directory,users_file_path,log_file,dp_min,dp_max,root,mode):
        self.th_id = th_id
        self.ftp_socket = ftp_socket
        self.directory = directory
        self.user = ANONYMOUS_USER
        self.user_level = ""
        self.data_port = ""
        self.data_socket = None
        self.FTP_ROOT = directory
        self.USER_DATA_FILE = users_file_path
        self.ADMIN_STOP = False
        self.ADMIN_QUIT = False
        self.type_text = False
        self.PASSIVE_MODE = False
        self.DATA_PORT_MIN = dp_min 
        self.DATA_PORT_MAX = dp_max
        self.DATA_PORT_BACKLOG = 1
        self.next_data_port = 1
        self.first_login_attempt_time = 0
        self.last_login_attempt = 0
        self.user = ""
        self.log_file = log_file
        self.root = root
        self.ftp_mode = mode



    #
    def __del__(self):
        self.ftp_socket.close()
    
    #all the covered commands by the server
    def commands(self):
        COMMANDS = {   
                    cmds.CMD_APPE   : self.appe,                                      
                    cmds.CMD_BYE    : self.bye,   
                    cmds.CMD_CWD    : self.cwdir,        
                    cmds.CMD_DELETE : self.remove,       
                    cmds.CMD_LS     : self.ls,   
                    cmds.CMD_MDELETE: self.mdelete,
                    cmds.CMD_MGET   : self.mget,        
                    cmds.CMD_MKD    : self.mkdir,  
                    cmds.CMD_MV     : self.move,   
                    cmds.CMD_NOOP   : self.noop,  
                    cmds.CMD_PASSIVE: self.passive,       
                    cmds.CMD_PORT   : self.port, 
                    cmds.CMD_PASV   : self.pasv,  
                    cmds.CMD_PWD    : self.pwdir,        
                    cmds.CMD_QUIT   : self.quit,         
                    cmds.CMD_RENAME : self.rename,       
                    cmds.CMD_RETR   : self.get,          
                    cmds.CMD_RMD    : self.rmdir,        
                    cmds.CMD_RNFR   : self.rnfr,         
                    cmds.CMD_SERVICE: self.service,      
                    cmds.CMD_SIZE   : self.size,         
                    cmds.CMD_STOR   : self.put,
                    cmds.CMD_TYPE   : self.type,          
                    cmds.CMD_USER   : self.login         
                    }
        return COMMANDS        

    #
    def hascommand(self,command):
        return command in self.commands()   
    
    #
    def run_command(self,tokens):
        command = tokens[0]
        if(self.user != ANONYMOUS_USER):
            msg = self.commands()[command](tokens)
        elif(command in cmds.NOT_AUTH_NEEDED):
            msg = self.commands()[command](tokens)
        else:
            msg = " User needs authentication. " + DIVIDER + msgs.MSG_421

        self.send(msg)
        self.log_entry(tokens,msg)

    #
    def send(self,message):
        self.ftp_socket.send(message.encode())

    #
    def passive(self,tokens):
        self.PASSIVE_MODE = not self.PASSIVE_MODE
        mode_msg = msgs.MSG_227 if (self.PASSIVE_MODE) else "Leaving passive mode."
        return mode_msg

    #
    def mkdir(self,tokens):
        basepath = self.directory
        msg = msgs.MSG_257
        newpath = os.path.join(basepath,tokens[1])
        if(not os.path.exists(newpath)):
            os.mkdir(newpath)
            msg = msgs.MSG_257 
        else :
            msg = msgs.MSG_257 + " Already existing."
        return msg

    #
    def rmdir(self,tokens):
        basepath = self.directory
        dir_to_remove = os.path.join(basepath,tokens[1])
        if (os.path.exists(dir_to_remove)):
        	os.rmdir(tokens[1])
        	msg = msgs.MSG_250
        else :
        	msg = msgs.MSG_450
        return msg

    #
    def port (self,tokens):
        port_arguments,port = self.divide_port(tokens)
        cmd_port = cmds.CMD_PORT + " " + port_arguments + " " + str(port) + NEW_LINE
        self.data_port = cmd_port
        return msgs.MSG_125

    #
    def divide_port(self,tokens):
        client_address = tokens[1].split(',')
        high_dport = int(client_address[4]) * 256 
        low_dport = int(client_address[5]) 
        port = high_dport + low_dport
        port_arguments = '.'.join(client_address[0:4])
        return port_arguments,port


    def pasv (self,tokens):
        data_port_min = self.DATA_PORT_MIN
        data_port_max = self.DATA_PORT_MAX
        dport = self.next_data_port

        host = gethostname()
        host_address = gethostbyname(host)

        self.next_data_port = self.next_data_port + 1 #for next next
        dport = (data_port_min + dport) % data_port_max

        self.data_socket = socket(AF_INET, SOCK_STREAM)
        # reuse port
        self.data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.data_socket.bind((host_address, dport))
        self.data_socket.listen(self.DATA_PORT_BACKLOG)
        
        host_address_split = host_address.split('.')
        high_dport = str(dport // 256) #get high part
        low_dport = str(dport % 256) #similar to dport << 8 (left shift)
        port_argument_list = host_address_split + [high_dport,low_dport]
        server_port = ','.join(port_argument_list)
        msg = server_port + DIVIDER + msgs.MSG_200 
        try:
            self.ftp_socket.send(msg.encode())
            return msg
        except socket.timeout:
            return "Socket timeout. Port may have been used recently. wait and try again!"
        except socket.error:
            return "Socket error. Try again"

    #
    def prepare_data_socket(self):
        if(self.PASSIVE_MODE):
            self.data_socket, data_host = self.data_socket.accept()
        else:
            self.connect_data_socket()

    #
    def cwdir(self,tokens):
        msg = msgs.MSG_421 + " Your account is not accessible, please contact the administrator."
        if(self.user_level in [ADMINISTRATOR,USER]):
            basepath = self.directory
            newdir = os.path.join(basepath,tokens[1])
            user = self.user
            if (os.path.isdir(newdir)):
            	os.chdir(newdir)
            	new_path = os.getcwd()
            	if(self.validpath(new_path)):
            		self.directory = new_path
            		msg = msgs.MSG_250
            	else:
            		msg = msgs.MSG_550 + " : not accessible path " + tokens[1]
            else:
            	msg = msgs.MSG_550 + " : not existing file " + tokens[1]
        return msg

    #
    def validpath(self,new_path):
    	user_level = self.user_level
    	if(user_level == USER):
    		return self.user in new_path
    	elif (user_level == ADMINISTRATOR):
    		return "ftproot" in new_path

    #
    def pwdir(self,tokens):
        basepath = self.directory
        path = str(basepath.split("ftpserver/",1)[1])
        msg = path + DIVIDER + msgs.MSG_200
        return msg

    #
    def rename(self,tokens):
        return self.make_new_file(tokens,False)

    #
    def move(self,tokens):
        return self.make_new_file(tokens,True)

    #
    def make_new_file(self,tokens,remove_source):
        basepath = self.directory
        msg = msgs.MSG_550
        file_path = os.path.join(basepath,tokens[1])
        if (os.path.exists(file_path)) :
            new_file_path = os.path.join(basepath,tokens[2])
            msg = self.rnto(file_path, os.path.join(basepath,new_file_path),remove_source)
        return msg

    #
    def rnfr(self,tokens):
        basepath = self.directory
        msg = msgs.MSG_550
        file_path = os.path.join(basepath,tokens[1])
        if (os.path.exists(file_path)) :
            new_tokens = self.ftp_socket.recv(RECV_BUFFER).decode().split()
            new_file_path = os.path.join(basepath,new_tokens[1])
            msg = self.rnto(file_path,new_file_path,False)
        return msg

    #
    def rnto(self,oldfilename, newfilename,remove_source):
        try:
            if(remove_source):
                shutil.move(oldfilename, newfilename)
            else:
                shutil.copyfile(oldfilename, newfilename)
            msg = msgs.MSG_250
        except:
            msg = msgs.MSG_550
        return msg

    #
    def size(self,tokens):
        basepath = self.directory
        size_message = msgs.MSG_550
        file_path = os.path.join(basepath,tokens[1])
        if (os.path.exists(file_path)):
            file_size = str(os.path.getsize(file_path)) + " bytes"
            size_message = file_size + DIVIDER + msgs.MSG_200
        return size_message

    #
    def remove(self,tokens):
        basepath = self.directory
        msg = msgs.MSG_550
        file_path = os.path.join(basepath,tokens[1])
        if (os.path.isfile(file_path)) :
            os.remove(tokens[1])
            msg = msgs.MSG_200
        else: 
            msg = msg + " Not a valid file name"
        return msg

    #
    def ls(self,tokens):
        basepath = self.directory 
        dir_path = basepath
        os.chdir(dir_path)

        self.prepare_data_socket()

        if (len(tokens) == 2):
            dir_path = os.path.join(dir_path,tokens[1])
            if(os.path.exists(dir_path)):
                os.chdir(dir_path)

        dirs = subprocess.Popen(['ls','-l'], stdout=subprocess.PIPE)


        while True:
            line = dirs.stdout.readline()
            if (not line):
                self.data_socket.send(msgs.MSG_EMPTY.strip().encode())
                break
            self.data_socket.send(line)

        self.data_socket.close()
        return msgs.MSG_226
        

    #
    def connect_data_socket(self):
        datatokens = self.data_port.split( )
        clientaddress = gethostbyaddr(datatokens[1])
        self.data_socket = socket(AF_INET, SOCK_STREAM)
        self.data_socket.connect((datatokens[1], int(datatokens[2])))
        

    #
    def login(self,tokens):
        new_user = tokens[1].strip()
        user_stored_data = self.find_user_data(new_user)
        if(user_stored_data == []):
            return msgs.MSG_430

        self.user = new_user
        user_msg = msgs.MSG_331 + ". Verifying password for " + new_user
        self.send(user_msg)
        passmsg = self.ftp_socket.recv(RECV_BUFFER).decode().split()
        passw = passmsg[1]

        user_restricted = any ([ user_stored_data == [],               \
                                 user_stored_data[2] == "blocked",     \
                                 user_stored_data[2] == "notallowed" ])
        msg = msgs.MSG_530
        if( not user_restricted ):
            new_user_path = self.getpath(user_stored_data)
            if(passw == user_stored_data[1]):
                msg = msgs.MSG_230
                self.directory = new_user_path
                self.user_level = user_stored_data[2]
                self.last_login_attempt = 0
                self.last_login_attempt_time = 0
            else: 
                if (not self.check_user_login_attempts(user_stored_data)):
                    msg = msgs.MSG_421 + " Your account was locked for security reasons, please contact the administrator"
                    self.last_login_attempt = 0
                    self.last_login_attempt_time = 0
        else:
            msg = msgs.MSG_421 + " Your account is not accessible, please contact the administrator"
        
        return msg

    #
    def getpath(self,user_stored_data):
        switcher = {
            USER            : os.path.join(self.FTP_ROOT,user_stored_data[0]),
            ADMINISTRATOR   : self.FTP_ROOT,
        }
        return switcher.get(user_stored_data[2], "")

    #
    def find_user_data(self,new_user):
        with open(self.USER_DATA_FILE, 'r') as f:
            data = f.readlines()
        for line in data:
            words = line.split()
            if(new_user in words):
                return words
        return [] # not registered

    #
    def check_user_login_attempts(self,user_data):
        if(not self.last_login_attempt):
            self.first_login_attempt_time = time.time()

        self.last_login_attempt = self.last_login_attempt + 1

        user_attempts_allowed = int(user_data[3])
        user_time_frame = int(user_data[4])

        if (self.last_login_attempt > user_attempts_allowed):
            timespan = time.time() - self.first_login_attempt_time
            if (timespan < user_time_frame):
                self.lock_user()
                return False
        return True

    #
    def lock_user(self):
        with open(self.USER_DATA_FILE, 'r') as fr:
            data = fr.readlines()

        for i in range(len(data)):
            if (self.user in data[i]):
                user_data = data[i].split()
                data[i] = user_data[0] + " "    \
                          + user_data[1] + " "  \
                          + "blocked\n"  + " "  \
                          + user_data[3] + " "  \
                          + user_data[4]
                break

        with open(self.USER_DATA_FILE, 'w') as fw:
            fw.writelines(data)

    #
    def quit(self,tokens):
        self.user = ANONYMOUS_USER
        self.user_level = ""
        return msgs.MSG_231  

    #
    def appe(self,tokens):
        return self.upload(tokens,True)

    #
    def put(self,tokens):
        return self.upload(tokens,False)

    #
    def upload(self,tokens,append):
        basepath = self.directory
        
        self.send(msgs.MSG_125)
        self.prepare_data_socket()
        
        filename = os.path.join(basepath,tokens[2])

        mode = self.get_write_mode(append)
        
        file_to = open(filename, mode)
        data = self.data_socket.recv(RECV_BUFFER)
        try:
            sys.stdout.write("|")
            while (len(data) > 0):
                sys.stdout.write("*")
                file_to.write(data)
                data = self.data_socket.recv(RECV_BUFFER)
            sys.stdout.write("|")
            msg = msgs.MSG_200
        except Exception as e:
            print (e)
            msg = str(e)
        except:
            msg = msgs.MSG_426 + ". Error transferring file"
        finally:
            file_to.close()
        return msg

    #
    def get_read_mode(self):
        return "r" if self.type_text else "rb"

    #
    def get_write_mode(self,append):
        if(self.type_text):
            return "a+" if append else "w"
        else:
        	return "ab+" if append else "wb"

    
    #
    def mdelete(self,tokens)            :
        files_ok,files_msg,files = self.are_files_ok(tokens)
        if(not files_ok):
            return msg

        self.send(files_msg)
        for i_file in files:
            cmd = self.ftp_socket.recv(RECV_BUFFER).decode()
            if (cmd == "SKIP"):
                continue

            # DELETE
            the_file = cmd.split()[1]
            msg = self.remove([cmds.CMD_DELETE,the_file])
            self.send(msg)
            self.log_entry([cmds.CMD_DELETE,the_file],msg)
        return msgs.MSG_200

    #
    def mget(self,tokens):
        files_ok,files_msg,files = self.are_files_ok(tokens)
        if(not files_ok):
            return msgs.MSG_550 + " There is no file in the path"
        
        self.send(files_msg)
        for i_file in files:
            # Receive PORT PASV or SKIP
            cmd = self.ftp_socket.recv(RECV_BUFFER).decode()
            if (cmd == "SKIP"):
                continue

            # Process PORT or PASV
            commands = cmd.split()
            msg = self.commands()[commands[0]](commands)
            if(not self.PASSIVE_MODE):
                self.send(msg)
            self.log_entry(commands,msg)

            # GET
            cmd = self.ftp_socket.recv(RECV_BUFFER).decode()
            ds = str(self.data_socket)
            dp = str(self.data_port)
            the_file = cmd.split()[1]
            msg = self.get([cmds.CMD_GET,the_file,the_file])
            self.send(msg)
            self.log_entry([cmds.CMD_GET,the_file],msg)

        return msgs.MSG_200

    #
    def are_files_ok(self,tokens):
        files = self.get_files(tokens)
        if(not files):
            return False, msgs.MSG_550 + " Files unavailable",files
        files_msg = msgs.MSG_150 + DIVIDER + " ".join(files)
        return True,files_msg,files

    # 
    def get_files(self,tokens):
        basepath = self.directory
        file_list = []
        if(tokens[1] == "*"):
            for i_file in os.listdir(basepath):
                file_list.append(i_file)
        else:
            file_list = tokens[1:]
        return file_list

    #
    def get(self,tokens):
        basepath = self.directory

        file_path = os.path.join(basepath,tokens[1])
        if(not os.path.isfile(file_path)):
            return msgs.MSG_550

        self.send(msgs.MSG_150)
        self.prepare_data_socket()
        mode = self.get_read_mode()

        the_file = open(file_path,mode) #read and binary modes
        msg = msgs.MSG_200

        size_sent = 0
        try:
            sys.stdout.write("|")
            while True:
                sys.stdout.write("*")
                data = the_file.read(RECV_BUFFER)
                if (not data or data == '' or len(data) <= 0):
                    self.data_socket.send(msgs.MSG_EMPTY.encode())
                    the_file.close()
                    break
                else:
                    data_to_send = str(data).encode() if(self.type_text) else data
                    self.data_socket.send(data_to_send)
                    size_sent += len(data)
            sys.stdout.write("|")
            sys.stdout.write("\n")
            
        except IOError as e:
            if e.errno == errno.EPIPE:
                msg = msgs.MSG_426
        except Exception as e:
            print(e)
            msg = msgs.MSG_502 + str(e)
        finally:
            the_file.close()
        
        self.data_socket.close()
        return msg

    #
    def noop(self,tokens):
        return msgs.MSG_200

    #
    def type(self,tokens):
        self.type_text = tokens[1] == "A"
        add_msg = " Transfers will be in binary mode. " 
        if (self.type_text):
            add_msg = " Transfers will be in text mode. "
        msg =  "Type " + tokens[1] + " set." + add_msg + DIVIDER + msgs.MSG_200
        return msg

    #
    def bye(self,tokens):
        msg = msgs.MSG_221
        self.ftp_socket.close()
        return msg

    #
    def service(self,tokens):
        user_level = self.user_level
        msg = msgs.MSG_550 + " : Requires administrator privileges"
        if(user_level == ADMINISTRATOR):
            if(tokens[1] == STOP_TOKEN):
                self.ADMIN_STOP = True
                msg = msgs.MSG_250
            elif (tokens[1] == START_TOKEN):
                self.ADMIN_STOP = False
                msg = msgs.MSG_200
            elif (tokens[1] == QUIT_TOKEN):
                self.ADMIN_QUIT = True
                msg = msgs.MSG_221
            else:
                msg = cmds.msgs_504
        return msg

    #
    def log_entry(self,tokens,msg):
        sep = "\t"
        now = datetime.datetime.now()
        log_line = now.isoformat() + sep 
        log_line += "USER: " + self.user + sep
        mode = "Passive " if (self.PASSIVE_MODE) else "Active"
        log_line += "MODE: " + mode + sep
        log_line += ' '.join(tokens) + sep
        log_line += "Server msg: " + msg + "\r\n"
        log_file = os.path.join(self.root,self.log_file)

        try:
            with open(log_file, 'a') as fa:
                fa.write(log_line)
        except Exception as e:
            print(e)



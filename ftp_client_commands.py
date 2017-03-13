import os
import sys
import shutil
import subprocess
import errno
import threading
import time
import datetime
import ftp_commands as cmds
import ftp_server_messages as msgs
import ftp_help as h
from socket import *


NEW_LINE = "\r\n"
DIVIDER = "#"
RECV_BUFFER = 1024
MSG_EMPTY = ""

#
def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class Session:

	def __init__(self,ftp_socket, dp_min,dp_max,logged_on,d_FTP,log_file,app_path):
	    self.ftp_socket = ftp_socket
	    self.data_socket = None
	    self.data_port = ""
	    self.next_data_port = 1
	    self.DATA_PORT_MIN = dp_min 
	    self.DATA_PORT_MAX = dp_max
	    self.DATA_PORT_BACKLOG = 1
	    self.DEFAULT_FTP_PORT = d_FTP
	    self.logged_on = logged_on
	    self.VERBOSE_ON = True
	    self.type_text = False
	    self.PASSIVE_MODE = False
	    self.log_file = log_file
	    self.user = "ANONYMOUS"
	    self.app_path = app_path
	    
	    



# all the covered commands by the server
	def commands(self):
	    COMMANDS = {   
	                cmds.CMD_APPE		: self.appe_ftp,                                      
	                cmds.CMD_BYE        : self.quit_ftp,     
	                cmds.CMD_CD         : self.cwd_ftp,       
	                cmds.CMD_CDUP       : self.cdup_ftp, 
	                cmds.CMD_CLEAR		: self.clear_ftp,    
	                cmds.CMD_CLOSE      : self.quit_ftp, 
	                cmds.CMD_CLS		: self.clear_ftp,  
	                cmds.CMD_COPY		: self.rename_ftp,     
	                cmds.CMD_CWD        : self.cwd_ftp,  
	                cmds.CMD_DEL 		: self.delete_ftp,    
	                cmds.CMD_DELETE     : self.delete_ftp,   
	                cmds.CMD_DIR        : self.ls_ftp,  
	                cmds.CMD_EXCL_CD 	: self.lcd,
	                cmds.CMD_EXCL_DEL 	: self.ldelete,
	                cmds.CMD_EXCL_CDUP 	: self.lcdup,
	                cmds.CMD_EXCL_COPY  : self.lrename,  
	                cmds.CMD_EXCL_CWD 	: self.lcd,
	                cmds.CMD_EXCL_DIR 	: self.lls,
	                cmds.CMD_EXCL_DELETE: self.ldelete,
	                cmds.CMD_EXCL_LIST 	: self.lls,
	                cmds.CMD_EXCL_LS 	: self.lls,
	                cmds.CMD_EXCL_MKD 	: self.lmkd,
	                cmds.CMD_EXCL_MKDIR : self.lmkd,
	                cmds.CMD_EXCL_MV 	: self.lmove,
	                cmds.CMD_EXCL_MOVE 	: self.lmove,
	                cmds.CMD_EXCL_PWD 	: self.lpwd,
	                cmds.CMD_EXCL_REMOVE: self.ldelete,
	                cmds.CMD_EXCL_RENAME: self.lrename,
	                cmds.CMD_EXCL_RM 	: self.ldelete,
	                cmds.CMD_EXCL_RMD 	: self.lrmd,
	                cmds.CMD_EXCL_RMDIR : self.lrmd,
	                cmds.CMD_EXCL_SIZE 	: self.lsize,
	                cmds.CMD_EXIT       : self.quit_ftp,     
	                cmds.CMD_GET        : self.get_ftp,      
	                cmds.CMD_HELP       : self.help_ftp,     
	                cmds.CMD_LCD        : self.lcd,          
	                cmds.CMD_LIST       : self.ls_ftp,       
	                cmds.CMD_LLS        : self.lls,          
	                cmds.CMD_LOGIN      : self.relogin,      
	                cmds.CMD_LOGOUT     : self.logout,       
	                cmds.CMD_LPWD       : self.lpwd,         
	                cmds.CMD_LS         : self.ls_ftp,  
	                cmds.CMD_MDEL 		: self.mdelete_ftp,
	                cmds.CMD_MDELETE	: self.mdelete_ftp,
	                cmds.CMD_MGET 		: self.mget_ftp,     
	                cmds.CMD_MKD        : self.mkd_ftp,      
	                cmds.CMD_MKDIR      : self.mkd_ftp,     
	                cmds.CMD_MV			: self.move_ftp, 
	                cmds.CMD_MOVE 		: self.move_ftp,
	                cmds.CMD_MPUT		: self.mput_ftp,
	                cmds.CMD_NOOP       : self.noop,     
	                cmds.CMD_PASSIVE  	: self.passive_ftp,
	                cmds.CMD_PUT        : self.put_ftp,      
	                cmds.CMD_PWD        : self.pwd_ftp,      
	                cmds.CMD_QUEST      : self.help_ftp,     
	                cmds.CMD_QUIT       : self.quit_ftp, 
	                cmds.CMD_REMOVE 	: self.delete_ftp,    
	                cmds.CMD_RENAME     : self.rename_ftp,   
	                cmds.CMD_RETR       : self.get_ftp, 
	                cmds.CMD_RM 		: self.delete_ftp,     
	                cmds.CMD_RMD        : self.rmd_ftp,
	                cmds.CMD_RMDIR      : self.rmd_ftp,      
	                cmds.CMD_RNFR       : self.rnfr_ftp,     
	                cmds.CMD_SERVICE    : self.service_ftp,  
	                cmds.CMD_SIZE       : self.size_ftp,     
	                cmds.CMD_STOR       : self.put_ftp,  
	                cmds.CMD_TYPE		: self.type_ftp, 
	                cmds.CMD_USER		: self.user_ftp,   
	                cmds.CMD_VERBOSE    : self.verbose       
	                }
	    return COMMANDS  

	#
	def hascommand(self,command):
	    return command in self.commands()   

	#
	#@threaded
	def run_command(self,tokens):
	    msg = msgs.MSG_421 + " User needs authentication"
	    command = tokens[0].upper()
	    if(self.logged_on):
	        msg = self.commands()[command](tokens)
	    elif(command in cmds.NOT_AUTH_NEEDED):
	        msg = self.commands()[command](tokens)
	    self.printverbose(msg)
	    self.log_entry(tokens,msg)
	    
	#
	def printverbose(self,msg):
	    if(self.VERBOSE_ON):
	        print(msg)

	#
	def str_msg_encode(self,strValue):
	    msg = strValue.encode()
	    return msg

	#
	def msg_str_decode(self,msg,pStrip=False):
	    strValue = msg.decode()
	    if (pStrip):
	        strValue.rstrip()
	    return strValue

	#
	def clear_ftp(self,tokens=None):
		subprocess.call('clear',shell=True)
		return MSG_EMPTY

	#
	def passive_ftp(self,tokens):
	    parameter = ""
	    if (len(tokens)>1):
	        parameter = " " + tokens[1] + " "
	    self.ftp_socket.send(self.str_msg_encode(cmds.CMD_PASSIVE + parameter + NEW_LINE)) 
	    data_msg = self.ftp_socket.recv(RECV_BUFFER).decode()
	    self.PASSIVE_MODE = not self.PASSIVE_MODE
	    return data_msg

	#
	def pwd_ftp(self,tokens=None):
	    self.ftp_socket.send(self.str_msg_encode(cmds.CMD_PWD + NEW_LINE)) 
	    data_msg = self.ftp_socket.recv(RECV_BUFFER).decode().split(DIVIDER)
	    print(data_msg[0])
	    return data_msg[1]

	#
	def cwd_ftp(self,tokens):
	    cmd = tokens[0]
	    if (len(tokens)<2):
	        msg = cmd + "[existing_path]. Please include existing path"
	    else :
	        if(tokens[1] == ".."):
	            path = ".."
	        else:
	            path = tokens[1]
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_CWD + " " + path + NEW_LINE)) 
	        msg = self.ftp_socket.recv(RECV_BUFFER).decode()
	    return msg

	#
	def lcd(self,tokens):
	    cmd = tokens[0]
	    if (len(tokens)<2):
	        return cmd + "[existing_path]. Please include existing path"
	    else :
	        path = os.path.join(os.getcwd(),tokens[1])
	        msg = "Not a valid directory"
	        if (os.path.isdir(path)) :
	            os.chdir(path)
	            msg = os.getcwd()
	        return msg

	#
	def lpwd(self,tokens=None):
	    return os.getcwd()

	#
	def lls(self,tokens):
	    file_path = os.getcwd()
	    if(len(tokens)==2):
	        file_path = os.path.join(file_path,tokens[1])
	    
	    msg = "Invalid file path"
	    if(os.path.exists(file_path)):

	        dirs = subprocess.Popen(['ls','-l'], stdout=subprocess.PIPE)
	        while True:
	            line = dirs.stdout.readline()
	            if (not line):
	                break
	            print(line.decode().strip())
	    return "Listing finished"

	#
	def verbose(self,tokens):
	    if(len(tokens)<2):
	        mode = "ON" if self.VERBOSE_ON else "OFF"
	        return "Current verbose mode is " + mode + ". VERBOSE [ON/OFF]. Please enter the setting"

	    option = tokens[1].upper()
	    if( option not in ["ON","OFF"]):
	        return "The options for VERBOSE are  [ON/OFF]"

	    self.VERBOSE_ON = option == "ON"
	    action = "activated" if self.VERBOSE_ON else "deactivated"
	    return "The verbose mode has been", action


	#
	def cdup_ftp(self,tokens):
	    return self.cwd_ftp([cmds.CMD_CDUP,".."]) 

	#
	def lcdup(self,tokens):
	    return self.lcwd([cmds.CMD_LCD,".."]) 

	#
	def mkd_ftp(self,tokens):
	    if (len(tokens)<2):
	        return tokens[0].upper() + " [new_folder]. Please include folder name"
	    else :
	        self.ftp_socket.send(self.str_msg_encode( cmds.CMD_MKD + " " + tokens[1] + NEW_LINE)) 
	        msg = self.ftp_socket.recv(RECV_BUFFER)
	        return self.msg_str_decode(msg,True)

	#
	def rmd_ftp(self,tokens):
	    msg = tokens[0].upper() + " [folder_to_remove]. Please include folder name"
	    if (len(tokens)==2):
	        self.ftp_socket.send(self.str_msg_encode( cmds.CMD_RMD + " " + tokens[1] + NEW_LINE)) 
	        msg = self.ftp_socket.recv(RECV_BUFFER)
	    return self.msg_str_decode(msg,True)	        

	#
	def lmkd(self,tokens):
	    msg = tokens[0].upper() + " [new_folder]. Please include folder name"
	    if (len(tokens)==2):
	        msg = "Invalid directory"
	        basepath = os.getcwd()
	        path = os.path.join(basepath,tokens[1])
	        os.mkdir(path)
	        msg = "Directory succefully created"
	    return msg	     

	#
	def size_ftp(self,tokens):
	    cmd = tokens[0]
	    msg = cmd + "[existing_file]. Please include existing file"
	    if (len(tokens)>=2):
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_SIZE + " " + tokens[1] + NEW_LINE)) 
	        messages = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER)).split(DIVIDER)
	        print(messages[0])
	        msg = messages[1]
	    return msg


	#
	def lrmd(self,tokens):
	    msg = tokens[0].upper() + " [folder_to_remove]. Please include folder name"
	    if (len(tokens)==2):
	        basepath = os.getcwd()
	        msg = "Directory not found"
	        dir_to_remove = os.path.join(basepath,tokens[1])
	        if (os.path.isdir(dir_to_remove)):
	            os.rmdir(tokens[1])
	            msg = "Directory succefully removed"
	    return msg

	#
	def rename_ftp(self,tokens):
		return self.move_rename_ftp(tokens,cmds.CMD_RENAME)

	#
	def move_ftp(self,tokens):
	    return self.move_rename_ftp(tokens,cmds.CMD_MV)

	#
	def move_rename_ftp(self,tokens,cmd):
		msg = tokens[0].upper() + " [oldfilename] [new_filename]. Please include the two filenames"
		if (len(tokens)>=3):
			self.ftp_socket.send(self.str_msg_encode( cmd + " " + tokens[1] + " " + tokens[2] + NEW_LINE))
			msg = self.ftp_socket.recv(RECV_BUFFER)
		return self.msg_str_decode(msg,True)	          

	#
	def lrename(self,tokens):
		return self.make_new_file(tokens,False)

	#
	def lmove(self,tokens):
		return self.make_new_file(tokens,True)

	#
	def make_new_file(self,tokens,remove_source):
	    msg = tokens[0].upper() + " [oldfilename] [new_filename]. Please include the two filenames"
	    if (len(tokens)==3):
	        basepath = os.getcwd()
	        msg = "File or destination path not found"
	        file_path = os.path.join(basepath,tokens[1])
	        new_file_path = os.path.join(basepath,tokens[2])
	        if (os.path.exists(file_path)) :
	            try:
	                if(remove_source):
	                    shutil.move(file_path, new_file_path)
	                else:
	                    os.rename(file_path, new_file_path)
	                msg = msgs.MSG_250
	            except:
	                msg = "There was an error renaming the file"
	    return msg	    

	#
	def rnfr_ftp(self,tokens):
	    if (len(tokens)<2):
	        return ( cmds.CMD_RNFR + "[filename]. Please specify filename")
	    else:
	        self.ftp_socket.send(self.str_msg_encode( cmds.CMD_RNFR + " " + tokens[1] + "\n"))
	        file_to = input("RNTO: ")
	        self.ftp_socket.send(self.str_msg_encode( cmds.CMD_RNTO + " " + file_to + "\n"))
	        msg = self.ftp_socket.recv(RECV_BUFFER)
	        return self.msg_str_decode(msg,True)


	#
	def lsize(self,tokens):
	    msg = tokens[0] + "[existing_file]. Please include existing file"
	    if (len(tokens)==2):
	        basepath = os.getcwd()
	        msg = "File not found"
	        file_path = os.path.join(basepath,tokens[1])
	        if (os.path.exists(file_path)):
	            msg = str(os.path.getsize(file_path)) + " bytes"
	    return msg

	#
	def ftp_new_dataport(self):
		data_port_min = self.DATA_PORT_MIN
		data_port_max = self.DATA_PORT_MAX
		dport = self.next_data_port

		host = gethostname()
		host_address = gethostbyname(host)
		self.next_data_port = self.next_data_port + 1 #for next next
		dport = (data_port_min + dport) % data_port_max

		self.printverbose(("Preparing Data Port: " + host + " " + host_address + " " + str(dport)))
		self.data_socket = socket(AF_INET, SOCK_STREAM)
		# reuse port
		self.data_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.data_socket.bind((host_address, dport))
		self.data_socket.listen(self.DATA_PORT_BACKLOG)
		
		host_address_split = host_address.split('.')
		high_dport = str(dport // 256) #get high part
		low_dport = str(dport % 256) #similar to dport << 8 (left shift)
		port_argument_list = host_address_split + [high_dport,low_dport]
		port_arguments = ','.join(port_argument_list)
		cmd_port_send = cmds.CMD_PORT + ' ' + port_arguments + NEW_LINE
		self.printverbose(cmd_port_send)

		try:
		    self.ftp_socket.send(self.str_msg_encode(cmd_port_send))
		except socket.timeout:
		    print("Socket timeout. Port may have been used recently. wait and try again!")
		    return 
		except socket.error:
		    print("Socket error. Try again")
		    return 
		msg = self.ftp_socket.recv(RECV_BUFFER)
		self.printverbose(self.msg_str_decode(msg,True))

	#
	def server_port (self):
	    cmd_pasv = cmds.CMD_PASV + NEW_LINE
	    self.ftp_socket.send(cmd_pasv.encode())
	    port_msg = self.ftp_socket.recv(RECV_BUFFER).decode().split(DIVIDER)
	    self.data_port = port_msg[0]
	    self.printverbose(" Server port ready: " + port_msg[0])
	    return port_msg[1]

	#
	def connect_data_socket(self):
	    ip,port = self.divide_port()
	    clientaddress = gethostbyaddr(ip)
	    self.data_socket = socket(AF_INET, SOCK_STREAM)
	    self.data_socket.connect( (ip,int(port)) )
     
    #
	def divide_port(self):
	    client_address = self.data_port.split(',')
	    high_dport = int(client_address[4]) * 256 
	    low_dport = int(client_address[5]) 
	    port = high_dport + low_dport
	    port_arguments = '.'.join(client_address[0:4])
	    return port_arguments,str(port)


	#
	def mget_ftp(self,tokens):
		if(len(tokens)==1):
			return "Please follow the format: " + MGET_USAGE

		self.ftp_socket.send(self.str_msg_encode(cmds.CMD_MGET+ " " + " ".join(tokens[1:]) + NEW_LINE))
		
		msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
		if(msg.split()[0] == "550"):
			return msg

		msg_files = msg.split(DIVIDER)
		server_mesg = msg_files[0]
		self.printverbose(server_mesg)

		files = msg_files[1].split()
		for i_file in files:
			ans = input("mget file: " + i_file + " y? ")
			if (ans != "y"):
				self.ftp_socket.send(self.str_msg_encode("SKIP"))
				continue
			new_tokens = [cmds.CMD_GET,i_file,i_file]
			msg = self.get_ftp(new_tokens)

			self.printverbose(msg)
			self.log_entry(new_tokens,msg)
		return msgs.MSG_250

	#
	def get_ftp(self,tokens):
		if(self.PASSIVE_MODE):
			return self.get_ftp_passive(tokens)
		else:
			return self.get_ftp_active(tokens)

	#
	def send_get_command_to_server(self,tokens):
		remote_filename, filename = self.get_default_parameter(tokens)
		self.ftp_socket.send(self.str_msg_encode( cmds.CMD_RETR + " " + remote_filename + " " + filename + NEW_LINE))			
		self.printverbose(("Attempting to write file. Remote: " + remote_filename + " - Local:" + filename))
		return remote_filename, filename

	#
	def get_file_validation_on_the_server(self,remote_filename):
		msg = self.ftp_socket.recv(RECV_BUFFER)
		strValue = self.msg_str_decode(msg)
		tokens = strValue.split()
		if (tokens[0] != "150"):
			return False,"Unable to retrieve file. Check that file exists (ls) or that you have permissions"
		return True,""

	#
	def get_file_validation_in_the_client(self,local_filename):
		if (not os.path.isfile(local_filename)):
			return False,"Filename does not exists on this client. Filename: " + local_filename + " -- Check file name and path"
		return True,""			

	#
	def get_ftp_passive(self,tokens):
		self.server_port()
		self.connect_data_socket()
		socket_tokens_are_valid, msg = self.validate_datasocket_tokens(tokens)
		if(not socket_tokens_are_valid):
			return msg
		remote_filename, local_filename = self.send_get_command_to_server(tokens);

		server_file_valid, msg = self.get_file_validation_on_the_server(remote_filename)
		if(not server_file_valid):
			return msg
		self.printverbose(msg)
		return self.get(local_filename)

	#
	def get_ftp_active(self,tokens):
		self.ftp_new_dataport()
		socket_tokens_are_valid, msg = self.validate_datasocket_tokens(tokens)
		if(not socket_tokens_are_valid):
			return msg
		remote_filename, local_filename = self.send_get_command_to_server(tokens)
		server_file_valid, msg = self.get_file_validation_on_the_server(remote_filename)

		if(not server_file_valid):
			return msg
		self.printverbose(msg)
		self.data_socket, data_host = self.data_socket.accept()
		return self.get(local_filename)


	#
	def get(self,local_filename):
		file_bin = open(local_filename, self.get_write_mode())  # read and binary modes
		size_recv = 0
		sys.stdout.write("|")
		while True:
			sys.stdout.write("*")
			data = self.data_socket.recv(RECV_BUFFER)
			if (not data or data == '' or len(data) <= 0):
				file_bin.close()
				break
			else:
				data_to_write = data.decode() if(self.type_text) else data
				file_bin.write(data_to_write)
				size_recv += len(data)
		sys.stdout.write("|")
		sys.stdout.write("\n")
		self.data_socket.close()

		msg = self.ftp_socket.recv(RECV_BUFFER)
		return self.msg_str_decode(msg,True)

	#
	def get_default_parameter(self,tokens):
		explicit_filename = tokens[1]
		if (len(tokens) == 3):
			return tokens[1],tokens[2]
		else:
			return explicit_filename,explicit_filename

	#
	def validate_datasocket_tokens(self,tokens):
	    if (self.data_socket is None):
	        return False,"[" + tokens[0].upper() + "] Failed to get data port. Try again."

	    if (len(tokens) < 2):
	        return False,tokens[0].upper() + " [filename]. Please specify filename"
	    return True,""

	#
	def appe_ftp(self,tokens):
		if(self.PASSIVE_MODE):
			return self.ftp_upload_passive(tokens,True)
		else:
			return self.ftp_upload_active(tokens,True)

	#
	def put_ftp(self,tokens):
		if(self.PASSIVE_MODE):
			return self.ftp_upload_passive(tokens,False)
		else:
			return self.ftp_upload_active(tokens,False)

	#
	def mput_ftp(self,tokens):
		if(len(tokens)==1):
			return "Please follow this format: " + cmds.MPUT_USAGE

		files = self.get_files(tokens)
		if(not files):
			return msgs.MSG_550

		for i_file in files:
			input_msg = "Transfer file " + i_file + " y? "
			ans = input(input_msg)
			if(ans.upper() != "Y"):
				continue
			new_tokens = [cmds.CMD_PUT,i_file,i_file]
			msg = self.put_ftp(new_tokens)
			self.printverbose(msg)
			self.log_entry(new_tokens,msg)
		return msgs.MSG_250

	#
	def get_files(self,tokens):
		my_dir = os.getcwd()
		file_list = []

		if(tokens[1] == "*"):
			for i_file in os.listdir(my_dir):
				file_list.append(i_file)
		else:
			file_list = tokens[1:]
		return file_list

	#
	def send_upload_command_to_server(self,tokens,append):
		local_filename, remote_filename = self.get_default_parameter(tokens)
		command = "STOR" if append else "APPE"
		self.ftp_socket.send(self.str_msg_encode( command + " " + local_filename + " " + remote_filename + NEW_LINE))
		self.printverbose(("Attempting to read a file. Local: " + local_filename + " - Remote:" + remote_filename))
		return local_filename, remote_filename

	#
	def ftp_upload_passive(self,tokens,append):
		self.server_port()
		socket_tokens_are_valid, msg = self.validate_datasocket_tokens(tokens)
		if(not socket_tokens_are_valid):
			return msg
		local_filename,remote_filename = self.send_upload_command_to_server(tokens,append);
		client_file_valid, msg = self.get_file_validation_in_the_client(local_filename)
		if(not client_file_valid):
			return msg
		msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
		self.printverbose(msg)
		self.connect_data_socket()
		return self.upload(local_filename,remote_filename)

	#
	def ftp_upload_active(self,tokens,append):
		self.ftp_new_dataport()
		are_valid, msg = self.validate_datasocket_tokens(tokens)
		if(not are_valid):
			return msg
		local_filename,remote_filename = self.send_upload_command_to_server(tokens,append);
		client_file_valid, msg = self.get_file_validation_in_the_client(local_filename)
		if(not client_file_valid):
			return msg
		msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
		self.printverbose(msg)
		self.data_socket, data_host = self.data_socket.accept()
		return self.upload(local_filename,remote_filename)


	#
	def upload(self,local_filename,remote_filename):
		filestat = os.stat(local_filename)
		filesize = filestat.st_size

		self.printverbose(("Attempting to send file. Local: " + local_filename + " - Remote:" + remote_filename + " - Size:" + str(filesize)))
		
		file_bin = open(local_filename,self.get_read_mode()) #read and binary modes
		size_sent = 0
		#use write so it doesn't produce a new line (like print)
		try:
			sys.stdout.write("|")
			while True:
				sys.stdout.write("*")
				data = file_bin.read(RECV_BUFFER)
				if (not data or data == '' or len(data) <= 0):
					self.data_socket.send(MSG_EMPTY.encode())
					break
				else:
					if(self.type_text):
						data = data.encode()
					self.data_socket.send(data)
					size_sent += len(data)
			sys.stdout.write("|")
			sys.stdout.write("\n")
		except IOError as e:
			if e.errno == errno.EPIPE:
				return "426 Broken pipe error."
		except:
			return "426 Connection closed; transfer aborted."
		finally:
			file_bin.close()

		self.data_socket.close()
		msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
		return msg

	#
	def get_read_mode(self):
		return "r" if self.type_text else "rb"

	def get_write_mode(self):
		return "w" if self.type_text else "wb"		

	#
	def ls_ftp(self,tokens):
		if(self.PASSIVE_MODE):
			return self.ls_ftp_passive(tokens)
		else:
			return self.ls_ftp_active(tokens)

	#
	def send_ls_command_to_server(self,tokens):
		if (len(tokens) > 1):
			self.ftp_socket.send(self.str_msg_encode(cmds.CMD_LS + " " + tokens[1] + NEW_LINE))
		else:
			self.ftp_socket.send(self.str_msg_encode(cmds.CMD_LS + NEW_LINE))

	#
	def ls_ftp_passive(self,tokens):
		self.server_port()
		self.connect_data_socket()
		self.send_ls_command_to_server(tokens)
		return self.ls()
		
	#
	def ls_ftp_active(self,tokens):
	    self.ftp_new_dataport()
	    if (self.data_socket is None):
	        return "[" + tokens[0] + "] Failed to get data port. Try again."
	    self.send_ls_command_to_server(tokens)
	    self.data_socket, data_host = self.data_socket.accept()
	    return self.ls()

	#
	def ls(self):
	    self.printverbose("Listing directory" + NEW_LINE)
	    msg = self.data_socket.recv(RECV_BUFFER)
	    while (len(msg) > 0):
	        print(self.msg_str_decode(msg,True).strip())
	        msg = self.data_socket.recv(RECV_BUFFER)

	    self.data_socket.close()
	    msg = self.ftp_socket.recv(RECV_BUFFER)
	    return self.msg_str_decode(msg,True)


	#
	def noop(self,tokens):
	    self.ftp_socket.send(cmds.MD_NOOP)
	    return self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)

	#
	def service_ftp(self,tokens):
	    msg = "Invalid parameters, use SERVICE  STOP|START|QUIT]"
	    if(len(tokens)<2):
	    	return msg
	    if( tokens[1] in ["STOP","START","QUIT"]):
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_SERVICE + " " + tokens[1] + NEW_LINE))
	        msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
	    return msg  

	#
	def mdelete_ftp(self,tokens):
		if(len(tokens)==1):
			return "Please follow the format: " + MDELETE_USAGE

		self.ftp_socket.send(self.str_msg_encode(cmds.CMD_MDELETE+ " " + " ".join(tokens[1:]) + NEW_LINE))
		
		msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
		if(msg.split()[0] == "550"):
			return msg

		msg_files = msg.split(DIVIDER)
		server_mesg = msg_files[0]
		files = msg_files[1].split()

		self.printverbose(server_mesg)

		for i_file in files:
			ans = input("mdel file: " + i_file + "y? ")
			if (ans.upper() != "Y"):
				self.ftp_socket.send(self.str_msg_encode("SKIP"))
				continue

			new_tokens = [cmds.CMD_DELETE,i_file]
			msg = self. delete_ftp(new_tokens)
			self.printverbose(msg)
			self.log_entry(new_tokens,msg)
		return msgs.MSG_250


	#
	def delete_ftp(self,tokens):
	    msg = "You must specify a file to delete"
	    if (len(tokens) == 2):
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_DELETE + " " + tokens[1] + NEW_LINE))
	        self.printverbose(("Attempting to delete " + tokens[1]))
	        msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)
	    return msg

	#
	def ldelete(self,tokens):
	    msg = "You must specify a file to delete"
	    if (len(tokens) == 2):
	        self.printverbose(("Attempting to delete " + tokens[1]))
	        msg = "File not found"
	        file_path = os.path.join(os.getcwd(),tokens[1])
	        if (os.path.isfile(file_path)) :
	            os.remove(tokens[1])
	            msg = "File removed succefully"
	    return msg

	#
	def type_ftp(self,tokens):
	    msg = "Must specify the type [A / I] A = ASCII(text) I = Image(binary)"
	    if (len(tokens) > 1):
	        msg = "Wrong parameter"
	        mode = tokens[1].upper()
	        if (mode not in ["A","I"]):
	            return msg
	        self.type_text = mode == "A"
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_TYPE + " " + mode + NEW_LINE))
	        type_msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True).split(DIVIDER)
	        print(type_msg[0])
	        msg = type_msg[1]
	    return msg

	#
	def logout(self,tokens=None):
	    if (self.ftp_socket is None):
	        self.logged_on = False
	        return "Your connection was already terminated."

	    if (self.logged_on == False):
	        self.printverbose("You are not logged in. Logout command will be send anyways")

	    self.printverbose("Attempting to logged out")
	    msg = ""
	    try:
	        self.ftp_socket.send(self.str_msg_encode(cmds.CMD_QUIT + NEW_LINE))
	        msg = self.ftp_socket.recv(RECV_BUFFER)
	    except:
	        self.logged_on = False
	        return ("Problems logging out. Try logout again. Do not login if you haven't logged out!")
	    #self.ftp_socket = None
	    self.logged_on = False #it should only be true if logged in and not able to logout
	    return self.msg_str_decode(msg,True)


	def quit_ftp(self,tokens=None):
	    self.printverbose ("Quitting...")
	    self.logout()
	    msg = "Thank you for using FTP "
	    try:
	        if (self.ftp_socket is not None):
	            self.ftp_socket.close()
	    except:
	        msg = "Socket was not able to be close. It may have been closed already"
	    sys.exit(msg)


	def relogin(self,tokens):
	    if (len(tokens) < 3):
	        print(cmds.CMD_LOGIN + " requires more arguments." + cmds.CMD_LOGIN + " [username] [password]")
	        self.printverbose("You will be prompted for username and password now")
	        username = input("User:")
	        password = input("Pass:")
	    else:
	        username = tokens[1]
	        password = tokens[2]

	    return self.login(username, password)

	    

	def help_ftp(self,tokens=None):
		# my help is a new object
	    help_cmd = h.Help()
	    help_cmd.command_help(tokens)
	    return "To learn the usage of any specific command type: \n\r HELP [command1] [command2] ..."

	#
	def user_ftp(self,tokens):
		if(len(tokens)>=3):
			user = tokens[1]
			passw = tokens[2]
		else:
			if(len(tokens)==1):
				user = input("User:")
			else:
				user = tokens[1]
			passw = input("Pass:")
		return self.login(user,passw)


	#
	def login(self,user, passw):
	    if (user == None or user.strip() == ""):
	        return ("Username is blank. Try again")

	    self.printverbose(("Attempting to login user " + user))
	    self.ftp_socket.send(self.str_msg_encode(cmds.CMD_USER + " " + user + NEW_LINE))
	    user_msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True) 
	    if(user_msg.split()[0] == "430"):
	        return user_msg

	    self.printverbose(user_msg)

	    self.ftp_socket.send(self.str_msg_encode(cmds.CMD_PASS + " " + passw + NEW_LINE))
	    pass_msg = self.msg_str_decode(self.ftp_socket.recv(RECV_BUFFER),True)    

	    if (pass_msg.split()[0] != "230"):
	        return pass_msg 
	    else:
	        self.logged_on = True
	        self.user = user
	        return pass_msg

	#
	def log_entry(self,tokens,msg):
	    sep = "\t"
	    now = datetime.datetime.now()
	    log_line = now.isoformat() + sep 
	    log_line += "User : " + self.user + sep
	    mode = "Passive " if (self.PASSIVE_MODE) else "Active"
	    log_line += "MODE: " + mode + sep
	    log_line += ' '.join(tokens) + sep
	    log_line += "Server msg: " + msg + "\r\n"
	    log_file = os.path.join(self.app_path,self.log_file)
	    try:
	        with open(log_file, 'a') as fa:
	            fa.write(log_line)
	    except Exception as e:
	        print(e)
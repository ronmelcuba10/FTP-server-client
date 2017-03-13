import ftp_commands as cmds

class Help:

	def command_help(self,tokens):
		if(len(tokens)==1):
			self.show_help()
			return
		if (self.any_valid_parameters(tokens)):
			print("\n")
			self.show_specific(tokens)
			print("\n")

	def show_help(self):
	    print("FTP Help")
	    print("Commands are not case sensitive")
	    print("")
	    print((cmds.CMD_EXCL + "\t\t makes the commands to work locally."))
	    print((cmds.CMD_QUEST + "\t\t prints out the help."))
	    print((cmds.CMD_BYE + "\t\t logouts the account and exits the ftp."))
	    print((cmds.CMD_CD + "\t\t changes to the specified remote directory."))
	    print((cmds.CMD_CDUP + "\t\t changes to the upper remote directory."))
	    print((cmds.CMD_CLOSE + "\t\t exits ftp and close ftp client."))
	    print((cmds.CMD_CLEAR + "\t\t clears the screen.")) 
	    print((cmds.CMD_CLS + "\t\t clears the screen.")) 
	    print((cmds.CMD_COPY + "\t\t copies/duplicates a file in the remote directory."))
	    print((cmds.CMD_CWD + "\t\t changes to the specified remote working directory."))
	    print((cmds.CMD_DEL + "\t\t deletes remote file."))
	    print((cmds.CMD_DELETE + "\t\t deletes remote file."))
	    print((cmds.CMD_DIR + "\t\t prints out remote directory content."))
	    print((cmds.CMD_EXIT + "\t\t exits ftp and close ftp client."))
	    print((cmds.CMD_GET + "\t\t downloads a remote file."))
	    print((cmds.CMD_HELP + "\t\t prints out the help."))
	    print((cmds.CMD_LCD + "\t\t prints out the local directory content. No auth required."))
	    print((cmds.CMD_LIST + "\t\t prints out remote directory content."))
	    print((cmds.CMD_LLS + "\t\t prints out the local directory content. No auth required."))
	    print((cmds.CMD_LOGIN + "\t\t logins into the ftp account."))
	    print((cmds.CMD_LOGOUT + "\t\t Logout from ftp but not client."))
	    print((cmds.CMD_LPWD + "\t\t prints current local working directory."))
	    print((cmds.CMD_LS + "\t\t prints out remote directory content."))
	    print((cmds.CMD_MGET + "\t\t downloads multiple remote files from the server."))
	    print((cmds.CMD_MKD + "\t\t creates a new remote directory."))
	    print((cmds.CMD_MKDIR + "\t\t creates a new remote directory."))
	    print((cmds.CMD_MV + "\t\t renames/moves a file in the remote directory."))
	    print((cmds.CMD_MPUT + "\t\t uploads multiple local files to the server."))
	    print((cmds.CMD_MOVE + "\t\t renames/moves a file in the remote directory."))
	    print((cmds.CMD_NOOP + "\t\t receive a confirmation signal from the ftp server."))
	    print((cmds.CMD_PUT + "\t\t uploads a local file to the server."))
	    print((cmds.CMD_PWD + "\t\t prints current remote working directory."))
	    print((cmds.CMD_QUIT + "\t\t exits ftp and close ftp client."))
	    print((cmds.CMD_REMOVE + "\t\t deletes remote file."))
	    print((cmds.CMD_RENAME + "\t\t renames/moves a file in the remote directory."))
	    print((cmds.CMD_RETR + "\t\t downloads a remote file."))
	    print((cmds.CMD_RM + "\t\t deletes remote file."))
	    print((cmds.CMD_RMD + "\t\t removes an existing remote directory."))
	    print((cmds.CMD_RMDIR + "\t\t removes an existing remote directory."))
	    print((cmds.CMD_RNFR + "\t\t renames a file or directory in the remote working directory."))
	    print((cmds.CMD_SERVICE + "\t\t to manage the ftp server, for administrator use only."))
	    print((cmds.CMD_SIZE + "\t\t returns the size in bytes of a remote file."))
	    print((cmds.CMD_STOR + "\t\t uploads a local file top the server."))
	    print((cmds.CMD_TYPE + "\t\t establishes the file transference mode."))
	    print((cmds.CMD_LOGIN + "\t\t logins into the ftp account."))
	    print((cmds.CMD_VERBOSE + "\t\t to show/hide message from the ftp server."))

	def any_valid_parameters(self,tokens):
	    return set(tokens).isdisjoint(cmds.COMMANDS)
	    
	#
	def show_specific(self,tokens):
		for cmd in tokens[1:]:
			cmdupper = cmd.upper()
			if( cmdupper in cmds.COMMANDS):
				print(cmds.COMMANDS_USAGE[cmdupper])
			elif ( cmd == cmds.CMD_EXCL ):
				self.show_exclamation()
			else: 
				print(cmdupper + "\t command not supported")



	def show_exclamation(self):
		print((cmds.CMD_EXCL + " this symbol can be combined in the following ways:"))
		print(cmds.CMD_EXCL_CD)
		print(cmds.CMD_EXCL_CDUP)
		print(cmds.CMD_EXCL_COPY)
		print(cmds.CMD_EXCL_CWD)
		print(cmds.CMD_EXCL_DIR)
		print(cmds.CMD_EXCL_DELETE)
		print(cmds.CMD_EXCL_LIST)
		print(cmds.CMD_EXCL_LS)
		print(cmds.CMD_EXCL_MKD)
		print(cmds.CMD_EXCL_MKDIR)
		print(cmds.CMD_EXCL_MV)
		print(cmds.CMD_EXCL_MOVE)
		print(cmds.CMD_EXCL_PWD)
		print(cmds.CMD_EXCL_REMOVE)
		print(cmds.CMD_EXCL_RENAME)
		print(cmds.CMD_EXCL_RM)
		print(cmds.CMD_EXCL_RMD)
		print(cmds.CMD_EXCL_RMDIR)
		print(cmds.CMD_EXCL_SIZE)
		print("These combinations execute the combined command locally")


		
		







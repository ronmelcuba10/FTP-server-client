# FTP-server-client

This is a ftp server-client application developed using python3. 
This ftp implements PASSIVE and ACTIVE
and most of the extra credit features including the MGET and MPUT commands
The client implements a total of 67 commands
the server implements a total of 23 different commands
Both use their log to keep the records of the commands activity


    The server runs withthe following command  	: python3 ftp_server.py
    and the client                              : python3 ftp_client.py
    to get the list of the commands type        : help or ?
    to get help about an specific command type  : help|?  [command1] [command2] [command3]...

to run the tests files type the following :	

			- TEST START   -----------> or DIST (explained below)
			- TEST CLEAN   -----------> or CLEAN (exlplained below)
			- TEST 

Of course, the test files wont be accesssible if the intial ftp_client working directory is modified
. The tests are performed on files located in the test_file_source folder

to login the ftp:
  
    regular admin 					: login admin admin1234


The distribution of the files is the following:

    /ftpsoft----
                  | - ftpserver - |               
                  |				        | - conf      - |
                  |				        | - ftproot   - |
                  |				        |				| - user 1
                  |				        |				| - admin
                  |				        |				| - user 2
                  |				        |				| - test_file_source
                  | -			        | - log
                  | - report
                  | - tests


 
inside of:

    /ftpsoft:
        - ftp_client.cfg          : configuration for the client
        - ftp_client.py           : client's code
        - ftp_cleint_commands.py  : client's commands implementation (Object)
        - ftp_commands.py         : all the commands supported
        - ftp_help.py             : file with the Help (Object)
        - ftp_server.py           : threaded server 
        - ftp_server_commands.py  : server commands implementation (Object)
        - ftp_server_messages.py  : messages + ftp codes used in the communication

    /tests:
        - test_distribute.tsf	  : executes a batch of file operations in server
        - test_clean_up.tsf       : restores the files moved to the initial point 
        - tests.tsf               : executes another batch of operations

    /ftpsoft/ftpserver/conf:
        - fsys.cfg                : server configuration file
        - user.cfg                : users configuration file

    /ftpsoft/ftpserver/log:
        - serverlog.log           : server log

    /ftpsoft/ftpserver/ftproot/test_file_source/:	
        - achievements.jpg        : image file
        - bird.jpg                : image file
        - byebeard.jpg            : image file
        - eye.jpg                 : image file
        - hoot.jpg                : image file
        - landscape.jpg           : image file			
        - lorem.txt               : text file
        - panda.jpg               : image file
        - putty.exe               : executable file














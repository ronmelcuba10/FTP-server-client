
CMD_APPE = "APPE"
CMD_BYE = "BYE"
CMD_CD = "CD"
CMD_CDUP = "CDUP"
CMD_CLEAR = "CLEAR"
CMD_CLOSE = "CLOSE"
CMD_CLS = "CLS"
CMD_COPY = "COPY"
CMD_CWD = "CWD"
CMD_DEL = "DEL"
CMD_DELETE = "DELETE" 
CMD_DIR = "DIR"

CMD_EXCL = "!"
CMD_EXCL_CD = "!CD"
CMD_EXCL_DEL = "!DEL"
CMD_EXCL_CDUP = "!CDUP"
CMD_EXCL_COPY = "!COPY"
CMD_EXCL_CWD = "!CWD" 
CMD_EXCL_DIR = "!DIR"
CMD_EXCL_DELETE = "!DELETE"
CMD_EXCL_LIST = "!LIST"
CMD_EXCL_LS = "!LS"
CMD_EXCL_MKD = "!MKD"
CMD_EXCL_MKDIR = "!MKDIR"
CMD_EXCL_MV = "!MV"
CMD_EXCL_MOVE = "!MOVE"
CMD_EXCL_PWD = "!PWD"
CMD_EXCL_REMOVE = "!REMOVE"
CMD_EXCL_RENAME = "!RENAME"
CMD_EXCL_RM = "!RM"
CMD_EXCL_RMD = "!RMD"
CMD_EXCL_RMDIR = "!RMDIR"
CMD_EXCL_SIZE = "!SIZE"


CMD_EXIT = "EXIT"   
CMD_GET = "GET"
CMD_HELP = "HELP"
CMD_LCD = "LCD"
CMD_LIST = "LIST"
CMD_LLS = "LLS"
CMD_LOGIN = "LOGIN"
CMD_LOGOUT = "LOGOUT"
CMD_LPWD = "LPWD"
CMD_LS = "LS"
CMD_MDEL = "MDEL"
CMD_MDELETE = "MDELETE"
CMD_MGET = "MGET"
CMD_MKD = "MKD"
CMD_MKDIR = "MKDIR"
CMD_MOVE = "MOVE"
CMD_MPUT = "MPUT"
CMD_MV = "MV"
CMD_NOOP = "NOOP"
CMD_PASS = "PASS"
CMD_PASSIVE = "PASSIVE"
CMD_PASV = "PASV"
CMD_PORT = "PORT"
CMD_PUT = "PUT"
CMD_PWD = "PWD"
CMD_QUEST = "?"
CMD_QUIT = "QUIT"
CMD_REMOVE = "REMOVE"
CMD_RENAME = "RENAME"
CMD_RETR = "RETR"
CMD_RM = "RM"
CMD_RMD = "RMD"
CMD_RMDIR = "RMDIR"
CMD_RNFR = "RNFR"
CMD_RNTO = "RNTO"
CMD_SERVICE = "SERVICE"
CMD_SIZE = "SIZE"
CMD_STOR = "STOR"
CMD_TYPE = "TYPE"
CMD_USER = "USER"
CMD_VERBOSE = "VERBOSE"

APPE_USAGE          = " APPE [local_file] [remote_file].\t Will append a remote file with a supplied local file.If not second parameter is submitted then the server will attempt to append a file with the same name in the remote directory. If the file does not exist the a new file is created."                              
BYE_USAGE           = " QUIT + enter.\t Additional parameters will be ignored."
CD_USAGE            = " CD [remote_file_path].\t If the directory path does not exists or is restricted, an error is displayed."
CDUP_USAGE          = " CDUP + enter.\t Additional parameters will be ignored."
CLEAR_USAGE         = " CLEAR + enter.\t Additional parameters will be ignored."
CLOSE_USAGE         = " CLOSE + enter.\t Additional parameters will be ignored."
CLS_USAGE           = " CLS + enter.\t Additional parameters will be ignored."
COPY_USAGE          = " COPY [source_remote_file_path] [destination_remote_file_path].\t If any of the paths do not exist or are restricted an error is displayed."
CWD_USAGE           = " CWD [remote_file_path].\t Optional paremeter. If the directory path does not exists an error is displayed."
DEL_USAGE           = " DEL [remote_file].\t If file does not exits or is restricted, an error is displayed"
DELETE_USAGE        = " DELETE [remote_file].\t If file does not exits or is restricted, an error is displayed"
DIR_USAGE           = " DIR [remote_file_path].\t Optional paremeter. If the directory path does not exists  or is restricted, an error is displayed."
EXCL_CD_USAGE       = " !CD [local_file_path].\t If the directory path does not exists an error is displayed."
EXCL_CDUP_USAGE     = " !CDUP + enter.\t Additional parameters will be ignored."
EXCL_COPY_USAGE     = " !COPY [source_local_file_path] [destination_local_file_path].\t If any of the paths do not exist an error is displayed."
EXCL_CWD_USAGE      = " !CWD [local_file_path].\t If the directory path does not exists an error is displayed."
EXCL_DELETE_USAGE   = " !DELETE [local_remote_file].\t If file does not exits an error is displayed."
EXCL_DIR_USAGE      = " !DIR [local_file_path].\t Optional paremeter. If the directory path does not exists an error is displayed."
EXCL_LIST_USAGE     = " !LIST [local_file_path].\t Optional paremeter. If the directory path does not exists an error is displayed."
EXCL_LS_USAGE       = " !LS [local_file_path].\t Optional paremeter. If the directory path does not exists an error is displayed."
EXCL_MKD_USAGE      = " !MKD [local_file_path].\t If the directory path does not exists an error is displayed."
EXCL_MKDIR_USAGE    = " !MKDIR [local_file_path].\t If the directory path does not exists an error is displayed."
EXCL_MOVE_USAGE     = " !MOVE [source_local_file_path] [destination_local_file_path].\t If any of the paths do not exist an error is displayed."
EXCL_MV_USAGE       = " !MV [source_local_file_path] [destination_local_file_path].\t If any of the paths do not exist an error is displayed."
EXCL_PWD_USAGE      = " !PWD Prints local working directory.\t Additional parameters will be ignored."
EXCL_REMOVE_USAGE   = " !REMOVE [local_file_path].\t If local file is not acessible an error is displayed."
EXCL_RENAME_USAGE   = " !RENAME [source_local_file_path] [destination_local_file_path].\t If any of the paths do not exist an error is displayed."
EXCL_RM_USAGE       = " !RM [local_file_path].\t If local file is not acessible an error is displayed."
EXCL_RMD_USAGE      = " !RMD [local_directory_path].\t If directory is not acessible an error is displayed."
EXCL_RMDIR_USAGE    = " !RMDIR [local_directory_path].\t If directory is not acessible an error is displayed."
EXCL_SIZE_USAGE     = " !SIZE [local_file_path].\t If file is not acessible an error is displayed."
EXIT_USAGE          = " EXIT + enter.\t Additional parameters will be ignored."
GET_USAGE           = " GET [remote_file] [local_file].\t Downloads a file from the ftp server. The second paremeter is optional if not supplied the remote file is downloaded and saved with its same name in the local directory. If the remote file is not accessible an error is displayed"  
HELP_USAGE          = " HELP [command].\t If the command is supplied its specific usage is shown"
LCD_USAGE           = " LCD [remote_directory_path].\t If the directory path does not exists or is restricted, an error is displayed."     
LIST_USAGE          = " LIST [remote_directory_path].\t Optional paremeter. If the directory path does not exists or is restricted, an error is displayed."   
LLS_USAGE           = " LLS [local_directory_path].\t Optional paremeter. If the directory path does not exists an error is displayed."
LOGIN_USAGE         = " LOGIN [user] [password].\t If the user/password are not suplied then follow the promt."   
LOGOUT_USAGE        = " LOGOUT + enter.\t Additional parameters will be ignored."   
LPWD_USAGE          = " LPWD Prints local working directory.\t Additional parameters will be ignored."     
LS_USAGE            = " LS [remote_directory_path].\t Optional paremeter. If the directory path does not exists or is restricted, an error is displayed."     
MDEL_USAGE          = " MDEL * | [filename1] [filename2]...[filenameN]"
MDELETE_USAGE       = " MDELETE * | [filename1] [filename2]...[filenameN]"
MGET_USAGE          = " MGET * | [filename1] [filename2]...[filenameN]"
MKD_USAGE           = " MKD [remote_directory_path].\t If the directory path does not exists or is restricted, an error is displayed."
MKDIR_USAGE         = " MKDIR [remote_directory_path].\t If the directory path does not exists or is restricted, an error is displayed."
MOVE_USAGE          = " MOVE [source_remote_file_path] [destination_remote_file_path].\t If any of the paths do not exist or are restricted an error is displayed."
MPUT_USAGE          = " MPUT * | [filename1] [filename2]...[filenameN]"
MV_USAGE            = " MV [source_remote_file_path] [destination_remote_file_path].\t If any of the paths do not exist or are restricted an error is displayed."
NOOP_USAGE          = " NOOP + enter.\t Additional parameters will be ignored."    
PASSIVE_USAGE       = " PASSIVE + enter.\t Additional parameters will be ignored."
PASV_USAGE          = " PASV + enter.\t Additional parameters will be ignored. "
PUT_USAGE           = " PUT [local_file] [remote_file].\t Uploads a file to the ftp server. The second paremeter is optional if not supplied the remote file is uploaded and saved with its same name from the local directory. If the remote file is not accessible an error is displayed"  
PWD_USAGE           = " PWD \tPrints remote working directory. Additional parameters will be ignored."
QUEST_USAGE         = " ? [command].\t This is the shortcut for the HELP command, if the command is supplied its specific usage is shown"  
QUIT_USAGE          = " QUIT + enter.\t Additional parameters will be ignored."
REMOVE_USAGE        = " REMOVE [remote_file_path].\t If the file does not exists or is restricted, an error is displayed." 
RENAME_USAGE        = " RENAME [source_remote_file_path] [destination_remote_file_path].\t If any of the paths do not exist or are restricted an error is displayed."
RETR_USAGE          = " RETR [remote_file] [local_file].\t Downloads a file from the ftp server. The second paremeter is optional if not supplied the remote file is downloaded and saved with its same name in the local directory. If the remote file is not accessible an error is displayed"  
RM_USAGE            = " RM [remote_file_path].\t If the file does not exists or is restricted, an error is displayed." 
RMD_USAGE           = " RMD [remote_directory_path].\t If directory is not acessible or is restricted, an error is displayed."
RMDIR_USAGE         = " RMDIR [remote_directory_path].\t If directory is not acessible or is restricted, an error is displayed."
RNFR_USAGE          = " RNFR [source_remote_file_path].\t Starts selecting the file to be renamed, follow the prompt. If the source file path does not exist or are restricted an error is displayed."  
SERVICE_USAGE       = " SERVICE [option].\t Available options: START => resumes the server activity | STOP => stops the server activity temporarily | QUIT => stops the server permanently. In all the termination options the current processes are let to finish"
SIZE_USAGE          = " SIZE [remote_file_path].\t If file is not acessible or is restricted an error is displayed."
STOR_USAGE          = " STOR [local_file] [remote_file].\t Uploads a file to the ftp server. The second paremeter is optional if not supplied the remote file is uploaded and saved with its same name from the local directory. If the remote file is not accessible an error is displayed"  
TYPE_USAGE          = " TYPE [mode].\t Changes the mode to be use in the file transfers. Two supported modes I => binary, A => text"
USER_USAGE          = " USER [user] [password].\t If the user/password are not suplied then follow the promt."   
VERBOSE_USAGE       = " VERBOSE [option].\t Shows/hides the ftp messages. Options ON|OFF"


COMMANDS = [CMD_APPE ,
            CMD_BYE ,
            CMD_CD ,
            CMD_CDUP ,
            CMD_CLEAR,
            CMD_CLOSE ,
            CMD_CLS,
            CMD_COPY,
            CMD_CWD ,
            CMD_DEL,
            CMD_DELETE ,
            CMD_DIR ,
            CMD_EXCL,
            CMD_EXCL_CD ,
            CMD_EXCL_CDUP ,
            CMD_EXCL_COPY,
            CMD_EXCL_CWD ,
            CMD_EXCL_DELETE ,
            CMD_EXCL_DIR ,
            CMD_EXCL_LIST ,
            CMD_EXCL_LS ,
            CMD_EXCL_MKD ,
            CMD_EXCL_MKDIR ,
            CMD_EXCL_MOVE ,
            CMD_EXCL_MV ,
            CMD_EXCL_PWD ,
            CMD_EXCL_REMOVE ,
            CMD_EXCL_RENAME ,
            CMD_EXCL_RM ,
            CMD_EXCL_RMD ,
            CMD_EXCL_RMDIR ,
            CMD_EXCL_SIZE ,
            CMD_EXIT ,
            CMD_GET ,
            CMD_HELP ,
            CMD_LCD ,
            CMD_LIST ,
            CMD_LLS ,
            CMD_LOGIN ,
            CMD_LOGOUT ,
            CMD_LPWD ,
            CMD_LS ,
            CMD_MDEL,
            CMD_MDELETE,
            CMD_MGET,
            CMD_MKD ,
            CMD_MKDIR ,
            CMD_MOVE,
            CMD_MPUT,
            CMD_MV,
            CMD_NOOP ,
            CMD_PASS ,
            CMD_PASSIVE,
            CMD_PASV,
            CMD_PORT ,
            CMD_PUT ,
            CMD_PWD ,
            CMD_QUEST ,
            CMD_QUIT ,
            CMD_REMOVE ,
            CMD_RENAME ,
            CMD_RETR ,
            CMD_RM,
            CMD_RMD ,
            CMD_RMDIR,
            CMD_RNFR ,
            CMD_RNTO ,
            CMD_SERVICE ,
            CMD_SIZE ,
            CMD_STOR ,
            CMD_TYPE,
            CMD_USER ,
            CMD_VERBOSE 
            ]


NOT_AUTH_NEEDED   = [
                    CMD_BYE,
                    CMD_CLEAR,
                    CMD_CLOSE,
                    CMD_CLS,
                    CMD_EXCL_CD ,
                    CMD_EXCL_CDUP ,
                    CMD_EXCL_COPY,
                    CMD_EXCL_CWD ,
                    CMD_EXCL_DELETE ,
                    CMD_EXCL_DIR ,
                    CMD_EXCL_LIST ,
                    CMD_EXCL_LS ,
                    CMD_EXCL_MKD ,
                    CMD_EXCL_MKDIR ,
                    CMD_EXCL_MOVE ,
                    CMD_EXCL_MV ,
                    CMD_EXCL_PWD ,
                    CMD_EXCL_REMOVE ,
                    CMD_EXCL_RENAME ,
                    CMD_EXCL_RM ,
                    CMD_EXCL_RMD ,
                    CMD_EXCL_RMDIR ,
                    CMD_EXCL_SIZE ,
                    CMD_EXIT,
                    CMD_HELP,
                    CMD_LCD,
                    CMD_LLS,
                    CMD_LOGIN,
                    CMD_LPWD,
                    CMD_QUEST,
                    CMD_QUIT,
                    CMD_USER,
                    CMD_VERBOSE,
                    ]

COMMANDS_USAGE = {
                    CMD_APPE        : APPE_USAGE,                                     
                    CMD_BYE         : BYE_USAGE,     
                    CMD_CD          : CD_USAGE,       
                    CMD_CDUP        : CDUP_USAGE, 
                    CMD_CLEAR       : CLEAR_USAGE,    
                    CMD_CLOSE       : CLOSE_USAGE, 
                    CMD_CLS         : CLS_USAGE, 
                    CMD_CWD         : CWD_USAGE, 
                    CMD_DEL         : DEL_USAGE,      
                    CMD_DELETE      : DELETE_USAGE,   
                    CMD_DIR         : DIR_USAGE,
                    CMD_EXCL_CD     : EXCL_CD_USAGE,
                    CMD_EXCL_CWD    : EXCL_CWD_USAGE,
                    CMD_EXCL_DELETE : EXCL_DELETE_USAGE,
                    CMD_EXCL_DIR    : EXCL_DIR_USAGE,
                    CMD_EXCL_LIST   : EXCL_LIST_USAGE,
                    CMD_EXCL_LS     : EXCL_LS_USAGE,
                    CMD_EXCL_MKD    : EXCL_MKD_USAGE,
                    CMD_EXCL_MKDIR  : EXCL_MKDIR_USAGE,
                    CMD_EXCL_MV     : EXCL_MV_USAGE,
                    CMD_EXCL_PWD    : EXCL_PWD_USAGE,
                    CMD_EXCL_REMOVE : EXCL_REMOVE_USAGE,
                    CMD_EXCL_RENAME : EXCL_RENAME_USAGE,
                    CMD_EXCL_RM     : EXCL_RM_USAGE,
                    CMD_EXCL_RMD    : EXCL_RMD_USAGE,
                    CMD_EXCL_RMDIR  : EXCL_RMDIR_USAGE,
                    CMD_EXCL_SIZE   : EXCL_SIZE_USAGE,
                    CMD_EXIT        : EXIT_USAGE,     
                    CMD_GET         : GET_USAGE,      
                    CMD_HELP        : HELP_USAGE,     
                    CMD_LCD         : LCD_USAGE,          
                    CMD_LIST        : LIST_USAGE,       
                    CMD_LLS         : LLS_USAGE,          
                    CMD_LOGIN       : LOGIN_USAGE,      
                    CMD_LOGOUT      : LOGOUT_USAGE,       
                    CMD_LPWD        : LPWD_USAGE,         
                    CMD_LS          : LS_USAGE,  
                    CMD_MDEL        : MDEL_USAGE,  
                    CMD_MDELETE     : MDELETE_USAGE,  
                    CMD_MGET        : MGET_USAGE,     
                    CMD_MKD         : MKD_USAGE,      
                    CMD_MKDIR       : MKDIR_USAGE,  
                    CMD_MPUT        : MPUT_USAGE,   
                    CMD_MV          : MV_USAGE, 
                    CMD_NOOP        : NOOP_USAGE,     
                    CMD_PASSIVE     : PASSIVE_USAGE,  
                    CMD_PUT         : PUT_USAGE,      
                    CMD_PWD         : PWD_USAGE,      
                    CMD_QUEST       : QUEST_USAGE,     
                    CMD_QUIT        : QUIT_USAGE, 
                    CMD_REMOVE      : REMOVE_USAGE,    
                    CMD_RENAME      : RENAME_USAGE,   
                    CMD_RETR        : RETR_USAGE, 
                    CMD_RM          : RM_USAGE,     
                    CMD_RMD         : RMD_USAGE,
                    CMD_RMDIR       : RMDIR_USAGE,      
                    CMD_RNFR        : RNFR_USAGE,     
                    CMD_SERVICE     : SERVICE_USAGE,  
                    CMD_SIZE        : SIZE_USAGE,     
                    CMD_STOR        : STOR_USAGE,  
                    CMD_TYPE        : TYPE_USAGE, 
                    CMD_USER        : USER_USAGE,   
                    CMD_VERBOSE     : VERBOSE_USAGE, 
                    CMD_COPY        : COPY_USAGE,      
                    CMD_EXCL_CDUP   : EXCL_CDUP_USAGE,
                    CMD_EXCL_COPY   : EXCL_COPY_USAGE,
                    CMD_MOVE        : MOVE_USAGE, 
                    CMD_PASV        : PASV_USAGE,  
		            }                    



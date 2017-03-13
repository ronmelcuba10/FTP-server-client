from socket import *
hostname = "cnt4713.cs.fiu.edu"
ftp_socket = socket(AF_INET, SOCK_STREAM)
ftp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
ftp_socket.connect((hostname, 12023)) 
ftp_socket.send("STOP".encode())

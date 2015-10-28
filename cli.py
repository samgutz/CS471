from socket import *
import sys

def client():
	#serverName = sys.argv[1]
	#serverPort = sys.argv[2]
	
	serverName = ''
	serverPort = 12000
	
	#establish control socket 
	controlSocket = socket(AF_INET, SOCK_STREAM)
	
	#establish data socket
	#dataSocket = socket(AF_INET, SOCK_STREAM)
	
	#bind data socket to server
	#dataSocket.connect((serverName, serverPort))
	
	##bind control socket to server
	controlSocket.connect((serverName, serverPort))	
	
	option = None
	while option != "quit":
		print("ftp>", end="")
		spec = input()
		spec = spec.split()
		option = spec[0]
		
		if option == "get":
			file_name = spec[1]
			#message = input("Input a message to send the server")
			
			#establish data socket
			#dataSocket = socket(AF_INET, SOCK_STREAM)
	
			#bind data socket to server
			#dataSocket.bind((serverName, serverPort))
			
			#dataSocket.lister(1)
			
			
			bytesSent = 0
			while bytesSent != len(message):
				print(bytesSent)
				bytesSent += controlSocket.send(message[bytesSent:].encode('utf-8'))
				
			
			
		elif option == "put":
			file_name = spec[1]
			
		elif option == "ls":
			print("All of the files")
			
		elif option == "quit":
			clientSocket.close()
			#dataSocket.close()
			
		else:
			print("invalid command")
	clientSocket.close()
	



		
		
	
def show_input_format():
	print("ftp> get <file name> (downloads file <file name> from the server)")
	print("ftp> put <filename> (uploads file <file name> to the server)")
	print("ftp> ls(lists files on the server)")
	print("ftp> quit (disconnects from the server and exits)")
	
if __name__ == "__main__":
	client()

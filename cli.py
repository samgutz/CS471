from socket import *
import sys

def client():
	#serverName = sys.argv[1]
	#serverPort = sys.argv[2]
	
	serverName = ''
	serverPort = 12000
	
	#establish control socket 
	controlSocket = socket(AF_INET, SOCK_STREAM)
	
	#establish control socket
	controlSocket.connect((serverName, serverPort))	
	
	option = None
	while option != "quit":
		print("ftp>", end="")
		spec = input()
		spec = spec.split()
		option = spec[0]
		argument = spec[0] + " " + spec[1]
		
		
		if option == "get":
		
			
			#establish data socket
			dataSocket = socket(AF_INET, SOCK_STREAM)
	
			#bind data socket to server
			dataSocket.bind((serverName, 22))
			
			#make the client listen for initial file size from server
			dataSocket.listen(1)
			
			listenSock = dataSocket.accept()
			
			controlSocket.send(argument.encode())
			
			actual_file_size = listenSock.recv(10)
			
			
			print("Size of file sent from server: {}".format(actual_file_size))
			
			bytesSent = 0
			#while bytesSent != len(message):
				#print(bytesSent)
				#bytesSent += dataSocket.send(message[bytesSent:].encode('utf-8'))
				
			
			
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

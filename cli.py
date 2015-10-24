from socket import *

def client():
	serverName = ''
	serverPort = 12000
	
	clientSocket = socket(AF_INET, SOCK_STREAM)
	
	clientSocket.connect((serverName, serverPort))
	
	data = "Test string sent from the client"
	
	bytesSent = 0
	while bytesSent != len(data):
		bytesSent += clientSocket.send(data[bytesSent:].encode('utf-8'))
	
	clientSocket.close()


def handle_user_input():
	option = None
	while option != "quit":
		print("ftp>", end="")
		spec = input()
		spec = spec.split()
		option = spec[0]
		
		if option == "get":
			file_name = spec[1]
			
		elif option == "put":
			file_name = spec[1]
			
		elif option == "ls":
			print("All of the files")
			
		else:
			print("invalid command")
		
		
	
def show_input_format():
	print("ftp> get <file name> (downloads file <file name> from the server)")
	print("ftp> put <filename> (uploads file <file name> to the server)")
	print("ftp> ls(lists files on the server)")
	print("ftp> quit (disconnects from the server and exits)")
	
if __name__ == "__main__":
	handle_user_input()

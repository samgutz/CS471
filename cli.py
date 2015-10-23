from socket import *

def client():
	serverName = ''
	serverPort = 12000
	
	clientSocket = socket(AF_INET, SOCK_STREAM)
	
	clientSocket.connect((serverName, serverPort))
	
	data = "Test string sent from the client"
	
	bytesSent = 0
	
	while bytesSent != len(data):
		bytesSent += clientSocket.send(data[bytesSent:])
	
	clientSocket.close()

if __name__ == "__main__":
	client()

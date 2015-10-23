from socket import *

def client():
	serverName = ''
	serverPort = 12000
	
	clientSocket = socket(AF_INET, SOCK_STREAM)
	
	clientSocket.connect((serverName, serverPort))
	
	data = "Test string sent from the client"
	
	bytesSent = clientSocket.send("Sending") #temporary solution to keep track of the number of bytes sent over the buffer
						 #Need to clear the buffer so that when it is trying to send the real message the message size
						 #count is not wrong
						 #same situation for serv.py
	
	while bytesSent != len(data):
		bytesSent += clientSocket.send(data[bytesSent:])
	
	clientSocket.close()

if __name__ == "__main__":
	client()

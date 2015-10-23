import sys
from socket import *
	
def server():
	#serverPort = int(sys.argv[1])
	
	serverPort = 12000
	
	serverSocket = socket(AF_INET, SOCK_STREAM)
	
	serverSocket.bind(('',serverPort))
	
	serverSocket.listen(1)
	
	print("Server established")
	
	while 1:
		connectionSocket, addr = serverSocket.accept()
		
		tmpBuff = ""
		data = 0
		while len(data) != 40:
			tmpBuff = connectionSocket.recv(40)
			
			if not tmpBuff:
				break
			
			data +=tmpBuff
			
		print(data)
		
		connectionSocket.close()
if __name__ == "__main__":
    server()

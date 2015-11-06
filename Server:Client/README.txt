CPSC 471 Assignment 1 - README
FTP client and server.
(Note, this project requires python 3.2 or higher to run.)


Kenneth Gunderson, Section 1 (KGunderson.csu.fullerton.edu)


REQUIREMENTS:
Python 3.2 or higher.


Summary:
Python client and server programs that can resolve hostnames into IP addresses, upload files, and download files using a reliable TCP connection. 
This project was created using python v3.2 and requires python v3.2 or higher to run.


USAGE:
python client.py //Edit if we add to the execution of the program
python server.py //Edit if we add to the execution of the program


Commands:
help 				- Returns a list of valid commands.
quit 				- Closes both the client and the server.
ls 					- Displays a list of files on the server.
put <file name> 	- Uploads a file to the server.
get <file name> 	- Downloads a file from the server.


Technical Issues:
This project will ONLY run if you have python v3.2 or higher installed.
REMEMBER that the "ls" command ONLY display the server's list of files, NOT the client's list of files.


NOTES FOR GROUP: THIS SHOULD BE DELETED OR EDITED WHEN WE SUBMIT….

I added the protocol design from the project I was using to help with all this, please let me know if you have any question my number is 714-308-5115. Sorry it took so long to upload I was busy over the weekend and forgot the other days, plus for some reason It stopped working so I had to fix it and clean up the code a bit, As of now it uses the default 12000 port and ‘’ server name without executing with a server name or port number this can be edited if you look in the code I left them commented out. Also each program has a fts_module class in their  folders this is used to do all the heavy lifting of transferring the files across the port.
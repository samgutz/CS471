CPSC 471 Assignment 1 - README
FTP client and server.
(Note, this project requires python 3.2 or higher to run.)


Kenneth Gunderson, Section 1 (KGunderson@csu.fullerton.edu)
Sam Gutierrez, Section 2 (sam_gutz@yahoo.com)
Bastian Awischus, Section 2 (bawischus@csu.fullerton.edu)


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

=======
Running
=======

Open two terminals and go in the according directories.

In one terminal type:

python3 cli.py

In the other terminal type:

python3 serv.py


The server will report the connection,
the data sent to the client, and any
status changes or errors.



Technical Issues:
This project will ONLY run if you have python v3.2 or higher installed.
REMEMBER that the "ls" command ONLY display the server's list of files, NOT the client's list of files.


################################################
#
# CPSC 471 Assignment 1
#
# Kenneth Gunderson Section 1 (KGunderson@csu.fullerton.edu)
# Sam Gutierrez, Section 2, and sam_gutz@yahoo.com
# Bastian Awischus, Section 2 (bawischus@csu.fullerton.edu)
#
# FTP client and server.
# This is the server.
#
################################################


#----------------------
#
# Imports
#
#----------------------
from socket import *
import sys
import os
import math
import fts_module


#
# Check command line for proper args.
# add additional arguements if we need to execute with port number and/or name

if len( sys.argv ) != 1:
    print ( "USAGE: ", sys.argv[0] )
    exit( 0 )


#
# GLOBALS
#
MSG_SIZE       = 128
BACKLOG_BUFFER = 100


#----------------------
# run_server
#----------------------
def run_server():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    # Initialize the state of the server.
    server_state = "READY"
    
    print( "Starting server, please wait for connection to client ... " )
    #This can be used if we need to execute the program with the port number
#   client_port = int( sys.argv[0] )

    cmd_socket, client_address = serverSocket.accept()
    print( "Connection accpeted, client found." )

    #
    # Service the client.
    #
    print( "Server is ready to receive and process commands." + "\n" )
    while( server_state == "READY" ):
        print( "Server awaiting command ... " )
        user_input = receive_command( cmd_socket )
        print( "CLIENT: " + user_input + "\n" )
        run_command( client_address, cmd_socket, user_input )
    
    cmd_socket.close()
    
#====================
# END: run_server
#====================


#----------------------
# receive_command
#----------------------
def receive_command( cmd_socket ):
    data_size = rcv_size( cmd_socket )

    user_input = rcv_data( cmd_socket, data_size )

    return user_input
    
#====================
# END: receive_command
#====================


#----------------------
# rcv_size
#----------------------
def rcv_size( cmd_socket ):
    # receive the size string.
    str_msg_size = rcv_data( cmd_socket, MSG_SIZE )

    # Convert the size string into an integer and return it.
    return int( str_msg_size )

#====================
# END: rcv_size
#====================


#----------------------
# rcv_data
#----------------------
def rcv_data( cmd_socket, data_size ):
    # The data buffer.
    data_buffer = ""

    # receive till all the data is collected.
    while len( data_buffer ) < data_size:
        
        # Collect as many bytes as possible in one pass.
        data_buffer += cmd_socket.recv( data_size - len( data_buffer ) ).decode()

    return data_buffer

#====================
# END: rcv_data
#====================


#----------------------
# run_command
#----------------------
def run_command( client_address, cmd_socket, user_input ):
    server_response = ""

    user_input = user_input.split( " ", 1 )
    
    #
    if user_input[0] == "help":
        server_response = "SERVER: " + user_input[0] + "\n"
        display_help()
        send_to_client( cmd_socket, server_response )
        
    elif user_input[0] == "quit":
        server_response = "SERVER: " + user_input[0] + "\n"
        exit_process( cmd_socket, server_response )
        send_to_client( cmd_socket, server_response )

    elif user_input[0] == "ls":
        server_response = "SERVER: " + user_input[0] + "\n"
        server_response = server_response + "\n" + "::".join( list_files() )
        send_to_client( cmd_socket, server_response )

    elif user_input[0] == "put":
        server_response = "SERVER: " + user_input[0] + "\n"
        put_file( cmd_socket )

    elif user_input[0] == "get":
        server_response = "SERVER: " + user_input[0] + "\n"
        send_to_client( cmd_socket, server_response )
        get_file( client_address, cmd_socket, user_input )

    else:
        server_response = "SERVER: " + user_input[0] + "\n"
        print( "\n" + "FAILURE" +
               "\n" + "Command \"" + user_input[0] + "\" not recognized." +
               "\n")
        display_help()
        send_to_client( cmd_socket, server_response )

    # Send the server response to the client.
    
#====================
# END: run_command
#====================


#----------------------
# display_help
#----------------------
def display_help():
    print( "help            - displays a list of usable commands" )
    print( "get <file_name> - downloads <file_name> from server" )
    print( "put <file_name> - uploads <file_name> to server" )
    print( "ls              - display a list of files on server" )
    print( "quit            - exits the process" )
    # Newline.
    print( "" )
    
#====================
# END: display_help
#====================


#----------------------
# exit_process
#----------------------
def exit_process( cmd_socket, server_response ):
    send_to_client( cmd_socket, server_response )
    
    cmd_socket.close()
    sys.exit( "SAFE EXIT" +
              "\n" )
    
#====================
# END: exit_process
#====================


#----------------------
# list_files
#----------------------
def list_files():
    # List of files: FILE_NAME, KB
    # Grab a list of all files in the server's working directory.
    ls_files = os.listdir( os.getcwd() )
    for file in range( len( ls_files ) ):
        # Find the file size in kb, and take the ceilling.
        # file_size = str( math.ceil( os.path.getsize( ls_files[file] ) / 1024 ) )
        file_size = str( os.path.getsize( ls_files[file] ) )
        ls_files[file] = ls_files[file] + ", " + file_size
        print( ls_files[file] )
    # Newline.
    print( "" )

    return ls_files

#====================
# END: list_files
#====================


#----------------------
# send_to_client
#----------------------
def send_to_client( cmd_socket, server_response ):
    # Send the size of the message to be transmitted.
    sent = False
    while sent == False:
    	    total_sent = send_msg_size( cmd_socket, len( server_response ) )
    	    if total_sent == len(str( server_response ).zfill( MSG_SIZE )):
    	    	    sent = True
    sent = False
    
    # Send the response until all data has been sent
    while sent == False:
    	    total_sent =  send_message( cmd_socket, server_response )
    	    if total_sent == len(server_response):
    	    	    sent = True

    
    
    
#====================
# END: send_to_client
#====================


#----------------------
# send_msg_size
#----------------------
def send_msg_size( cmd_socket, msg_len ):
    
    # Convert int to string before sending.
    str_msg_len = str( msg_len )

    # Pad the front-end of the message with zeros.
    # This esnures the expected message size.
    # Python automatically discards the leading zeros when read.
    str_msg_len = str( str_msg_len ).zfill( MSG_SIZE )

    # Send the data.
    total_sent = send_message( cmd_socket, str_msg_len )
    return total_sent
    
#====================
# END: send_msg_size
#====================


#----------------------
# send_message
#----------------------
def send_message( cmd_socket, data ):

    # Encode the string as bytes before sending.
    data = data.encode()
    
    # Number of bytes to send in one pass.
    num_sent = 0

    # The total number of bytes sent so far.
    total_sent = 0

    # Keep sending bytes until we've sent everything.
    while total_sent < len( data ):
        # Send as much as we can in one pass.
        num_sent = cmd_socket.send( data[total_sent:] )

        # Updata the total number of bytes sent so far.
        total_sent += num_sent

    return total_sent

#====================
# END: send_message
#====================


#----------------------
# put_file
#----------------------
def put_file( cmd_socket ):
    print( "Creating ephemeral port for file transfer ... " )

    # Binding to port 0 binds to the first available port.
    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind( ( '', 0 ) )
    
    eph_port = listen_socket.getsockname()[1]

    # Send the ephemeral port number to the client.
    send_to_client( cmd_socket, str( eph_port ) )
    listen_socket.listen( BACKLOG_BUFFER )

    transfer_socket, client_address = listen_socket.accept()
    print( "Connection accpeted, source found." )
    
    # Create an fts and hand it a socket.
    fts = fts_module.file_transfer_system( transfer_socket )

    file_info = fts.receive_file()

    print( "Transfer successful, closing socket.\n" )
    transfer_socket.close()
    
#====================
# END: put_file
#====================


#----------------------
# get_file
#----------------------
def get_file( dest_ip, cmd_socket, user_input ):

    # Build file information list for the fts module.
    file_info = []
    file_info.append( user_input[1] )
    file_info.append( os.path.getsize( user_input[1] ) )

    eph_port = int( receive_command( cmd_socket ) )

    print( "Starting fts source, please wait for connection to fts destination ... " )
    transfer_socket = socket(AF_INET, SOCK_STREAM )
    transfer_socket.connect( ( dest_ip[0], eph_port ) )
    print( "Connection created, destination connected.\n" )

    # Create an fts and hand it a socket.
    fts = fts_module.file_transfer_system( transfer_socket )

    # Tell fts to send a file, and give it the file info as a list["name", size].
    fts.send_file( file_info )

    print( "Transfer successful, closing socket." )
    transfer_socket.close()
    
#====================
# END: get_file
#====================


#
# Default startup is run_server.
#
if __name__ == "__main__":
    run_server()


########################
#
# END: server.py
#
########################

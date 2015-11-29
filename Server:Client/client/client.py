################################################
#
# CPSC 471 Assignment 1
#
# Kenneth Gunderson, Section 1 (KGunderson@csu.fullerton.edu)
# Sam Gutierrez, Section 2, and sam_gutz@yahoo.com
# Bastian Awischus, Section 2 (bawischus@csu.fullerton.edu)
#
# FTP client and server.
# This is the client.
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
import fts_module


#
# Check command line for proper args.
# add more arg if we need to execute with port name and/or number
if len( sys.argv ) != 1:
    print ( "USAGE: ", sys.argv[0] )
    exit( 0 )


#
# GLOBALS
#
MSG_SIZE = 128
BACKLOG_BUFFER = 100


#----------------------
# run_client
#----------------------
def run_client():
    #Turn these on if we need to execute with port name and/or number
#    server_name = sys.argv[1]
#    server_port = int( sys.argv[2] )
    serverName = ''
    serverPort = 12000
    print( "server_name: " + serverName + "\n" )


    # Initialize the state of the client.
    client_state = "READY"    


    # Resolve the IP address.
    server_ip = resolve_ip( serverName )
    
    #
    # Connect to the server.
    #
    print( "Starting client, please wait for connection to server ... " )
    cmd_socket = socket(AF_INET, SOCK_STREAM )
    cmd_socket.connect( ( server_ip, serverPort ) )
    print( "Connection created, server connected." )


    # Display list of options.
    print( "Client is ready to send commands." + "\n" )
    display_help()


    #
    # Service the user.
    #
    while( client_state == "READY" ):
        # Track user input.
        user_input = input("ftp> ")

        # Send the user command to the server.
        run_command( user_input, cmd_socket, server_ip )


    #
    # End the connection to the server.
    #
    cmd_socket.close()

#====================
# END: run_client
#====================


#----------------------
# run_command
#----------------------
def run_command( user_input, cmd_socket, server_ip ):
    # Send the command to the server.
    send_to_server( cmd_socket, user_input )

    # The server's response.
    server_response = receive_response( cmd_socket )

    user_input = user_input.split( " ", 1 )

    # 
    if user_input[0] == "help":
        print( server_response )
        display_help()

    elif user_input[0] == "quit":
        print( server_response )
        exit_process( cmd_socket )

    elif user_input[0] == "ls":
        list_files( server_response )

    elif user_input[0] == "get":
        print( server_response )
        get_file( cmd_socket )

    elif user_input[0] == "put":
        print( server_response )
        put_file( server_ip, cmd_socket, user_input, server_response )

    else:
        print( server_response )
        print( "\n" + "FAILURE" +
               "\n" + "Command \"" + user_input[0] + "\" not recognized." +
               "\n")
        display_help()
        
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
def exit_process( cmd_socket ):    
    cmd_socket.close()
    sys.exit( "SAFE EXIT" +
              "\n" )
    
#====================
# END: exit_process
#====================


#----------------------
# send_to_server
#----------------------
def send_to_server( cmd_socket, user_input ):
    # Send the size of the message to be transmitted.
    
    sent = False
    while sent == False:
    	    total_sent = send_msg_size( cmd_socket, len( user_input ) )
    	    if total_sent == len(str( user_input ).zfill( MSG_SIZE )):
    	    	    sent = True
    
    sent = False

    # Send the command.
    while sent == False:
    	    total_sent = send_message( cmd_socket, user_input )
    	    if total_sent == len(user_input):
    	    	    sent = True
    	    
    
#====================
# END: send_to_server
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
# receive_response
#----------------------
def receive_response( cmd_socket ):
    data_size = rcv_size( cmd_socket )

    user_input = rcv_data( cmd_socket, data_size )

    return user_input
    
#====================
# END: receive_response
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
# list_files
#----------------------
def list_files( server_response ):
    
    srv_msg = server_response.rpartition('\n')[0]
    srv_msg = "".join( srv_msg )
    print( srv_msg )

    # List of files: FILE_NAME, KB
    ls_files = server_response.rpartition('\n')[2].split('::')

    for file in range( len( ls_files ) ):
        print( ls_files[file] )

    # Newline.
    print( "" )

#====================
# END: list_files
#====================


#----------------------
# put_file
#----------------------
def put_file( dest_ip, cmd_socket, user_input, server_response ):

    # Build file information list for the fts module.
    file_info = []
    file_info.append( user_input[1] )
    file_info.append( os.path.getsize( user_input[1] ) )
    
    # Get the ephemarl port number from the server.
    eph_port = int( server_response )
    
    print( "Starting fts source, please wait for connection to fts destination ... " )
    transfer_socket = socket( AF_INET, SOCK_STREAM )
    transfer_socket.connect( ( dest_ip, eph_port ) )
    print( "Connection created, destination connected.\n" )

    # Create an fts and hand it a socket.
    fts = fts_module.file_transfer_system( transfer_socket )

    # Tell fts to send a file, and give it the file info as a list["name", size].
    fts.send_file( file_info )

    print( "Transfer successful, closing socket." )
    transfer_socket.close()

    print( "File transfered: " + file_info[0] + ", " + str( file_info[1] ) + "\n" )
    
#====================
# END: put_file
#====================


#----------------------
# get_file
#----------------------
def get_file( cmd_socket ):
    print( "Creating ephemeral port for file transfer ... " )

    # Binding to port 0 binds to the first available port.
    listen_socket = socket( AF_INET, SOCK_STREAM )
    listen_socket.bind( ( '', 0 ) )

    eph_port = listen_socket.getsockname()[1]

    str_eph_port = str( eph_port )
    send_to_server( cmd_socket, str_eph_port )
    
    listen_socket.listen( BACKLOG_BUFFER )
    transfer_socket, server_address = listen_socket.accept()
    print( "Connection accpeted, source found." )
    
    # Create an fts and hand it a socket.
    fts = fts_module.file_transfer_system( transfer_socket )

    file_info = fts.receive_file()

    print( "Transfer successful, closing socket.\n" )
    transfer_socket.close()

    print( "File transfered: " + file_info[0] + ", " + str( file_info[1] ) + "\n" )
    
#====================
# END: 
#====================


#----------------------
# resolve_ip
#----------------------
def resolve_ip( hostname ):
#    if DBG_resolve_ip:
#        print( "Please enter a hostname ..." )
#        hostname = input( "ftp>> " )
#
    if hostname == '':
        print( "Using default hostname \"localhost\"." )
        hostname = "localhost"

    ip_address = gethostbyname( hostname )
    print( "\nThe address of \"" + hostname + "\" is " + str( ip_address ) + ".\n" )

    return ip_address

#====================
# END: resolve_ip
#====================


#
# Default startup is run_client.
#
if __name__ == "__main__":
    run_client()


########################
#
# END: client.py
#
########################

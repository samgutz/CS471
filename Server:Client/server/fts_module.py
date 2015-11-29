################################################
#
# CPSC 471 Assignment 1
#
# Kenneth Gunderson, Section 1 (KGunderson.csu.fullerton.edu)
# Sam Gutierrez, Section 2, and sam_gutz@yahoo.com
# Bastian Awischus, Section 2 (bawischus@csu.fullerton.edu)
#
# FTP client and server.
# This is the file transfer module.
#
################################################


#----------------------
#
# Imports
#
#----------------------
import socket 
import sys
import os



#
# GLOBALS
#
MSG_SIZE = 128
BACKLOG_BUFFER = 100


#~~~~~~~~~~~~~~~~~~~~~~
# file_transfer_system
#~~~~~~~~~~~~~~~~~~~~~~
class file_transfer_system:

    def __init__( self, transfer_socket ):
        self.transfer_socket = transfer_socket   

        # Default values.
        self.file_name = ""
        self.file_size = 0

        # The amount of the file in bytes
        # that we'll hand/take from the buffer to
        # send/write.
        self.file_chunk = 128


    def send_file( self, file_info ):
        # Seperate the file_data into a file name, and a file size.
        self.file_name = file_info[0]
        self.file_size = file_info[1]
        
        # Send the size of the file name.
        self.send_msg_size( len( self.file_name ) )

        # Send the file name.
        # Encode the string as bytes before sending.
        self.send_data( self.file_name.encode() )

        # Send the size of the file.
        self.send_msg_size( self.file_size )


        # Send the file.
        # Create a file handler and open a new file.
        with open( self.file_name, 'rb' ) as fh:
            # Initialize the total number of bytes sent so far.
            total_bytes_sent = 0

            # The buffer that will store a given file chunk,
            # and then send that chunk to the destination.
            send_buffer = None

            # Send until all bytes of the file have been read an sent.
            while total_bytes_sent < self.file_size:
                # Read the next chunk size into the send buffer.
                # Automatically stops at the end of the file.
                send_buffer = fh.read( self.file_chunk )

                # Send the chunk in the buffer.
                self.send_data( send_buffer )

                # Update the total number of bytes now sent.
                total_bytes_sent += len( send_buffer )

            # Close the file and the connection.
            fh.close()
            self.transfer_socket.close()


    def send_msg_size( self, msg_len ):
        # Convert int to string before sending.
        str_msg_len = str( msg_len )

        # Pad the front-end of the message with zeros.
        # This esnures the expected message size.
        # Python automatically discards the leading zeros when read.
        str_msg_len = str( str_msg_len ).zfill( MSG_SIZE )

        self.send_data( str_msg_len.encode() )


    def send_data( self, data ):
        # Number of bytes to send in one pass.
        num_sent = 0

        # The total number of bytes sent so far.
        total_sent = 0

        # Keep sending bytes until we've sent everything.
        while total_sent < len( data ):
            # Send as much as we can in one pass.
            num_sent = self.transfer_socket.send( data[total_sent:] )

            # Updata the total number of bytes sent so far.
            total_sent += num_sent

        return total_sent


    def receive_file( self ):
        # Receive the size of the filename.
        file_name_length = self.rcv_size()

        # Receive the filename.
        self.file_name = self.rcv_data_string( file_name_length )

        # Receive the size of the file.
        self.file_size = self.rcv_size()
        
        # Package file info.
        file_info = ["myFileName", "myFileSize"]
        file_info[0] = self.file_name
        self.file_name = self.file_name.split( "/" )
        self.file_name = self.file_name[-1]
        file_info[1] = self.file_size
        
        # Receive the file.
        # Open a file to write the incoming file to.
        fh = open( self.file_name, 'wb' )
        
        # Track the total number of bytes received so far.
        total_bytes_rcv = 0

        # The total number of bytes to receive at a given time.
        num_to_rcv = 0
        

        # Keep receiving and writing until we've received the entire file.
        while total_bytes_rcv < self.file_size:
            # By default, receive "file_chunk" sized pieces of the file.
            num_to_rcv = self.file_chunk

            # If this is the last piece of the file, and there is less
            # than a "file_chunk" size left.
            if self.file_size - total_bytes_rcv < self.file_chunk:
                num_to_rcv = self.file_size - total_bytes_rcv

            # Receive the file data.
            file_data = self.rcv_data_binary( num_to_rcv )

            # Write the file data into the file.
            fh.write( file_data )

            # Update the amount of the file we've received.
            total_bytes_rcv += len( file_data )

        # Close the file and the connection.
        fh.close()
        self.transfer_socket.close()

        return file_info

        
    def rcv_size( self ):
        # receive the size string.
        str_msg_size = self.rcv_data_string( MSG_SIZE )

        # Convert the size string into an integer and return it.
        return int( str_msg_size )
                

    def rcv_data_string( self, data_size ):
        # The data buffer.
        data_buffer = ""

        # receive till all the data is collected.
        while len( data_buffer ) < data_size:
            
            # Collect as many bytes as possible in one pass.
            data_buffer += self.transfer_socket.recv( data_size - len( data_buffer ) ).decode()
            
        return data_buffer


    def rcv_data_binary( self, data_size ):
        # The data buffer.
        data_buffer = b""

        # receive till all the data is collected.
        while len( data_buffer ) < data_size:
            
            # Collect as many bytes as possible in one pass.
            data_buffer += self.transfer_socket.recv( data_size - len( data_buffer ) )            
        return data_buffer

        
#++++++++++++++++++++
# END: file_transfer_system
#++++++++++++++++++++

#
# Default startup is run_client.
#
if __name__ == "__main__":
    test_fts()


########################
#
# END: fts_module.py.py
#
########################


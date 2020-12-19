import socket
import time

HEADERSIZE = 100
CHUNKSIZE = 1000

# create TCP/IP socket s
# AF_INET builds for IPv4
# SOCKET_STREAM builds for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a port on the server machine
# give a tuple containing host name and port number
s.bind((socket.gethostname(), 1242))

#this socket listens only for ne connection, queueing is not needed for this task
s.listen(1)

#get the file to be written
f = open("transfer_file_TCP_server.txt", "a")

# get information about the client requested to connect
clientsocket, address = s.accept()

# get data from client socket with predetermined CHUNKSIZE

#since we are getting the message chunk by chunk we need to concatenate them
full_msg = ""

new_msg = True
final_chunk_flag = False
while True:
    msg = clientsocket.recv(CHUNKSIZE + HEADERSIZE)
    if new_msg:
        header = msg[:HEADERSIZE]
        header = header.decode("utf-8")
        header = header.split(",")
        if len(header) == 1:
            msglen = int(header[0])
            timestamp = time.time()
        elif len(header) == 4:
            msglen = int(header[0])
            timestamp = time.time() #time of last packet received
            timestamp_incoming = float(header[1]) #time of the last packed sent
            number_of_chunks = int(header[2])
            average_transmission_time = float(header[3].strip())
            average_transmission_time += (timestamp - timestamp_incoming) / number_of_chunks
            final_chunk_flag = True
        new_msg = False

    full_msg += msg.decode("utf-8")
    
    if len(full_msg) - HEADERSIZE == msglen:
        if final_chunk_flag == True:
            print("TCP Packets Average Transmission Time: " + str(average_transmission_time * 1000) + " ms")
            f.write(full_msg[HEADERSIZE:])
            break
        timestamp_msg = str(timestamp)
        clientsocket.send(bytes(timestamp_msg, "utf-8"))
        f.write(full_msg[HEADERSIZE:])
        new_msg = True
        full_msg = ""
        
f.close()



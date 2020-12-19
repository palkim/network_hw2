import socket
import time
import os
import math

HEADERSIZE = 100
CHUNKSIZE = 1000

# create client TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind client to its sender port
s.bind((socket.gethostname(), 1235))

#client will connet to hostname and port number of server
s.connect((socket.gethostname(), 1242))

is_first = True

file_name = "transfer_file_TCP.txt"
file_stats = os.stat(file_name)

file_size = file_stats.st_size
number_of_chunks = math.ceil(file_size / CHUNKSIZE)
total_time_passed = 0
timestamp_out = 0
chunk_number = 0
with open(file_name, 'r') as f:
    while True:
        chunk_number += 1
        if not is_first:
            timestamp_inc = s.recv(100)
            timestamp_inc = timestamp_inc.decode("utf-8")
            total_time_passed += float(timestamp_inc) - float(timestamp_out)

        read_data = f.read(CHUNKSIZE)

        if chunk_number == number_of_chunks:
            average_time_passed = total_time_passed / number_of_chunks
            msg = read_data
            timestamp_out = time.time()
            msg = f"{len(msg)}," + f"{timestamp_out}," + f"{number_of_chunks}," + f"{average_time_passed:<{HEADERSIZE - len(str(len(msg))) - len(str(timestamp_out)) - len(str(number_of_chunks)) - 3}}" + msg
            s.send(bytes(msg,"utf-8"))
            break

        # send data to server
        msg = read_data
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        timestamp_out = time.time()
        s.send(bytes(msg,"utf-8"))
        if is_first:
            is_first = False


        
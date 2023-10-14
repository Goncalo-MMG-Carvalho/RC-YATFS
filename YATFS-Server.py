import os
import random
import sys
from socket import *
import pickle

serverName = "127.0.0.1"

STATUS_OK = 0
STATUS_FILE_NOT_FOUND = 1
STATUS_INVALID_OFFSET = 2


def serverReply(msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # If rand is less is than 3, do not respond
    if rand >= 3:
        sock.sendto(msg, address)
    return

def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        sys.exit(6969)

    portSP = int(sys.argv[1])

    ss = socket(AF_INET, SOCK_DGRAM)
    ss.bind((serverName, portSP))

    bufferSize = 120 + sys.getsizeof(int) * 2   # a file name and 2 ints

    while True:

        line, clientAddr = ss.recvfrom(bufferSize)
        arrLine = pickle.loads(line)  #(fileName, offset, chunk)

        fileName = arrLine[0]
        offset = arrLine[1]
        chunk = arrLine[2]


        try:
            size = os.path.getsize("./" + fileName)

        except OSError:
            print("File requested does not exists or is inaccessible.")
            ss.sendto(pickle.dumps((STATUS_FILE_NOT_FOUND, 0, 0)), clientAddr)

        if(size < offset):
            print("Offset is invalid.")
            ss.sendto(pickle.dumps((STATUS_INVALID_OFFSET, 0, 0)), clientAddr)

        file = open("./" + fileName, 'rb')
        file.seek(offset)


"""
    create socket ss and bind it to portSP
    while TRUE:
        receive datagram with request and deserialize it using pickle.
        open file for reading, if open fails reply 
         with a datagram with status 1; the other fields must be filled
         verify if the offset is valid using os.path.filesize(…) method
         if open fails reply with a datagram with status 2
         if both previous tests succeed use seek to position the file pointer
         in the required position and try to read S bytes from the file
         reply with a tuple (0, no_of_bytes_read, file_chunk)
         serialize the reply using pickle and call serverReply


    message, address = sock.recvfrom(1024)
    request=pickle.loads(message)
    fileName = request[0]
    offset = request[1]
    noBytes = request[2]
    print(f'file= {fileName},offset={offset}, noBytes={noBytes}')
"""

main()
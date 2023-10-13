import random
from socket import *
import pickle


def serverReply(msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # If rand is less is than 3, do not respond
    if rand >= 3:
        sock.sendto(msg, address)
    return


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
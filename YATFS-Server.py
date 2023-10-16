import os
import random
import sys
from socket import *
import pickle

serverName = "127.0.0.1"

STATUS_OK = 0
STATUS_FILE_NOT_FOUND = 1
STATUS_INVALID_OFFSET = 2

SERVER_FILES_DIR = "./serverFiles/"


def serverReply(msg, sock, address):
    # msg is a byte array ready to be sent
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # If rand is less is than 3, do not respond
    # IMPORTANT: represents less than 40% packet loss, it represents 4/11 packet loss
    if rand >= 3:
        sock.sendto(msg, address)
    return


def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments.")
        sys.exit(6969)

    portSP = int(sys.argv[1])

    if portSP < 1024 or portSP > 65535:
        print("Incorrect port number.")
        sys.exit(69420)

    ss = socket(AF_INET, SOCK_DGRAM)
    ss.bind((serverName, portSP))

    print("Server is Listening")

    bufferSize = 120 + sys.getsizeof(int) * 2  # a file name and 2 ints

    while True:

        line, clientAddr = ss.recvfrom(bufferSize)
        tupleLine = pickle.loads(line)  # (fileName, offset, chunk)

        fileName = tupleLine[0]
        offset = tupleLine[1]
        chunk = tupleLine[2]

        size = 0  # just to initialize it

        try:
            size = os.path.getsize(SERVER_FILES_DIR + fileName)

        except OSError:
            print("File requested does not exists or is inaccessible.")
            ss.sendto(pickle.dumps((STATUS_FILE_NOT_FOUND, 0, 0)), clientAddr)
            continue

        if size < offset:
            print("Offset is invalid.")
            ss.sendto(pickle.dumps((STATUS_INVALID_OFFSET, 0, 0)), clientAddr)
            continue



        file = open(SERVER_FILES_DIR + fileName, 'rb')
        file.seek(offset)

        data = file.read(chunk)
        noBytes = len(data)

        msg = pickle.dumps((STATUS_OK, noBytes, data))

        serverReply(msg, ss, clientAddr)

        file.close()


if __name__ == "__main__":
    main()

from socket import *
import pickle
import select
import sys
import time

CLIENT_FILES_DIR = "./clientFiles/"


def waitForReply(uSocket):
    rx, tx, er = select.select([uSocket], [], [], 1)
    # waits for data or timeout after 1 second
    if not rx:
        return False
    else:
        return True


def main():
    # Check number of arguments
    if len(sys.argv) != 5:
        print("Wrong number of arguments.")
        sys.exit(6969)

    portSP = int(sys.argv[2])
    serverAddressPort = (sys.argv[1], portSP)
    fileName = sys.argv[3]
    chunk = int(sys.argv[4])

    if portSP < 1024 or portSP > 65535:
        print("Incorrect port number.")
        sys.exit(69420)

    print("Client is running.")

    cs = socket(AF_INET, SOCK_DGRAM)

    # file open
    file = open(CLIENT_FILES_DIR + fileName, 'wb')

    offset = 0

    endTime = 0
    startTime = time.time()  # start timer

    while True:
        request = (fileName, offset, chunk)
        req = pickle.dumps(request)
        cs.sendto(req, serverAddressPort)

        # Status reply + number of bytes to receive + bytes
        bufferSize = sys.getsizeof(int) + sys.getsizeof(int) + chunk  # maybe + 1

        if waitForReply(cs):
            reply, trash = cs.recvfrom(bufferSize)
            reply = pickle.loads(reply)

            if reply[0] == 0:
                offset += reply[1]
                file.write(reply[2])

                if reply[1] < chunk:
                    endTime = time.time()  # end timer
                    print("File transfer complete.")
                    print("Offset: ", offset)
                    break

            elif reply[0] == 1:
                print("Error: " + str(reply[0]) + ", file does not exist.")
                break

            elif reply[0] == 2:
                print("Error: " + str(reply[0]) + ", offset is invalid.")
                break

            else:
                print("Error: " + str(reply[0]) + ", unknown error.")
                print("Error description: ", str(reply[1]))
                break

    file.close()
    cs.close()

    # Transfer Rate in KB/s
    transferRate = (offset/1024) / (endTime - startTime)

    print("Transfer Rate = ", transferRate, " KB/s")
    #print("Time = ", endTime - startTime, " s")


if __name__ == "__main__":
    main()

from socket import *
import pickle
import select
import sys


# bufferSize = 1024

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

    serverAddressPort = (sys.argv[1], int(sys.argv[2]))
    fileName = sys.argv[3]
    chunk = int(sys.argv[4])

    print("Server address: " + sys.argv[1])
    print("Server port: " + sys.argv[2])
    print("File name: " + sys.argv[3])
    print("Chunk size: " + sys.argv[4])

    cs = socket(AF_INET, SOCK_DGRAM)

    # file open
    file = open("./clientFiles/" + fileName, 'wb')
    offset = 0

    while True:
        request = (fileName, offset, chunk)
        req = pickle.dumps(request)
        cs.sendto(req, serverAddressPort)

        print("Sent request for file " + fileName + " with offset " + str(offset) + " and chunk " + str(chunk))

        # Status reply + number of bytes to receive + bytes
        bufferSize = sys.getsizeof(int) + sys.getsizeof(int) + chunk  # maybe + 1

        if waitForReply(cs):
            reply, trash = cs.recvfrom(bufferSize)
            reply = pickle.loads(reply)
            if reply[0] == 0:
                offset += reply[1]
                file.write(reply[2])

                print("Received " + str(reply[1]) + " bytes.")

                if reply[1] < chunk:
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
                break
        else:
            print("Timeout")
            print("Offset: " + str(offset))
            break

    file.close()


main()

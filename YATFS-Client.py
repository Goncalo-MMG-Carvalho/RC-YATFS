from socket import *
import pickle
import select
import sys

#bufferSize = 1024

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

    cs = socket(AF_INET, SOCK_DGRAM)
    cs.bind(('', 2048))

    #file open
    file = open("./" + fileName, 'wb')
    offset = 0

    while True:
        request = (fileName, offset, chunk)
        req = pickle.dumps(request)
        cs.sendto(req, serverAddressPort)

        bufferSize = sys.getsizeof(int) + sys.getsizeof(int) + chunk

        if waitForReply(cs):
            reply = cs.recvfrom(bufferSize)
            reply = pickle.loads(reply)
            if reply[0] == 0:
                offset += reply[1]
                file.write(reply[2])

            elif reply[0] == 1:
                print("Error: " + reply[0] + ", file does not exist")
                break
                
            elif reply[0] == 2:
                print("Error: " + reply[0] + ", offset is invalid")
                break

            else:
                print("Error: " + reply[0] + ", unknown error")
                break


    """
        create socket sc and bind it to some UDP port
        open local file for writing
        offset = 0
        while TRUE:
        prepare request with fileName and offset; use pickle to serialize it
        send the request to (host_of_server, portSP)
        wait for reply; if reply does not arrive, repeat request
        write byte chunk received to file
        if EOF 
        break
        else 
        offset = offset + size
    """

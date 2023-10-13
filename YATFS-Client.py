from socket import *
import pickle
import select
import sys


def waitForReply( uSocket ):
    rx, tx, er = select.select([uSocket], [], [], 1)
    # waits for data or timeout after 1 second
    if not rx:
        return False
    else:
        return True

"""
    request = (fileName, offset, blockSize)
    req = pickle.dumps(request)
    UDPSocket.sendto(req, endpoint)
    
    
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

def main():
    # Check number of arguments
    if len(sys.argv) != 4:
        print("Wrong number of arguments.")
        sys.exit(6969)

    serverAddressPort = (sys.argv[1], int(sys.argv[2]))
    fileName = sys.argv[3]

    UDPClientSocket = socket(AF_INET, SOCK_DGRAM)




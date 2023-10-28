import socket
import os

def findInFirstsOf (String, List):
    for i in range(len(List)):
        if List[i][0] == String:
            return True
    return False


# Standard socket stuff:
host = socket.gethostname()
port = 8080
IPAddr=socket.gethostbyname(host)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IPAddr, port))
sock.listen(5) 

print ('The Web server URL for this would be http://%s:%d/' % (IPAddr, port))



# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    print("Connection from: " + str(caddr))
    req = csock.recv(1024)  # get the request, 1kB max
    #print(req)
    req = str(req)
    req = req[2:-1]
    reqType = req.split("\\n")

    for i in range(len(reqType)):
        reqType[i] = reqType[i].split(":")
    
    
    
    
    
    #
    if findInFirstsOf("Referer",reqType) == False: #check text file
        filename = 'static/index.html'
        f = open(filename, 'r')
        l = f.read(1024)
        while (l):
            csock.sendall(str.encode("""HTTP/1.0 200 OK\n""",'iso-8859-1'))
            csock.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
            csock.send(str.encode('\n'))    #end of header
            csock.sendall(str.encode(""+l+"", 'iso-8859-1'))
            #print('Sent ', repr(l))
            l = f.read(1024)
        f.close()
    
    csock.close()

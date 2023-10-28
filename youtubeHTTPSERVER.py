from http.server import HTTPServer, BaseHTTPRequestHandler
import time # imported for testing

HOST = "129.12.140.209"# my ip for testing
PORT = 9999# port to be hosted


formWebsiteText = '<h1>testing123</h1>' #test html to see if page would change

def getMessages():  #reads messages text file and returns as list
    messageString = readAndReturn("messages.txt")
    
    rows = messageString.split(";") #seperates message text file into rows
    for i in range(len(rows)):
        rows[i] = rows[i].split(",") #seperates rows into the columns(fields) in each row
    return rows

def getMessagesFrom(user): #looks through messages list for ones that have user same as wanted user
    db = getMessages()
    temp = []
    for i in range(len(db)):
        if db[i][0] == user[1:]: #checks if first field is same as username given
            temp.append(db[i])
    return temp

def listToString(list): #converts list to string 
    string=""
    for i in range(len(list)):
        for j in range(len(list[i])):
            string = string + list[i][j] +"," #adds each field in row to string and seperates fields by ,(comma)
        string = string[:-1] +";" #seperates each row in rows and seperates it with ;(semicolon)
    return string
    
def readAndReturn(filename): #opens text file and reuturns it as string
    f = open(filename, 'r')
    lineCount=0
    fullFile = ""
    for line in f:
        fullFile = fullFile+line #adds line from opened file to concatination string fullline
    f.close()
    fullFile = findAndReplace(fullFile, "\n", "") #removes \n from output
    return fullFile #returns string

def replaceAndReturn(filename, lineNumber, replace): #opens file, replaces a certian line and then outputs it
    f = open(filename, 'r')
    lineCount=0
    fullFile = ""
    for line in f:
        if lineCount == lineNumber: #checks if current line is line that will be changed
            temp = replace #replaces line in file with reoplacement text
        else:
            temp = line
        fullFile = fullFile+temp #adds temp to concatination string
        lineCount = lineCount + 1
    f.close()
    fullFile = findAndReplace(fullFile, "\n", "") #removes \n from output
    return fullFile #returns string

def findAndReplace(originalText, code, replacement): #finds substring within string then replaces it 
    for i in range(len(originalText)):
        try:
            if originalText[i:i+len(code)]==code: #compares substring of orignal text to wanted string
                originalText=originalText[:i]+ replacement + originalText[i+len(code):]
        except:
            originalText = originalText #here as it will always not work near end of list
    return(originalText)

def requestsMaker(requestIn):
    index = 0
    first = True #just want first item after the original start / otherwise will get the http bit
    requestIn = findAndReplace(requestIn,"%20"," ") #makes this code into a space as when sent over network it converts space to %20
    for i in range(len(requestIn)):
        if requestIn[i] == "/" and first: #finds where the first / is
            index = i
            first = False
    requests = requestIn[index:-9].split(" ") #gets rid of start bit and end bit of request (the get part and the http part)
    return requests #returns string

def nameAndEmail(string):   #depreciated
    for i in range(len(string)):
        if string[i]=="&":
            string=string[:i]+ " " + string[i+1:]
    string = findAndReplace(string,"%40","@")
    return string

class charlieHTTP(BaseHTTPRequestHandler):
    #override
    def do_GET(self): #GET is called by website when it wants to get information from the server
        print(self.requestline)
        request = requestsMaker(self.requestline) #gets request sent by website
        print(request)

        if (request[0]) == "/": #if browser wants webpage (like it does initially) itll send a blank command(commands start with slash) 
            self.send_response(200)#says ok to browser
            self.send_header("Content-type", "text/html") #sets content of message as text/html content
            self.end_headers()# ends header
            self.wfile.write(bytes(readAndReturn("index.html"),"utf-8"))#sends back index.html to browser
            
        elif (request[0]) == "/button": #website asks for button command
            self.send_response(200) 
            self.send_header("Content-type", "text/html")
            self.end_headers() 
            self.wfile.write(bytes(formWebsiteText,"utf-8")) #sends back test string
        elif (request[0]) == "/getMessages": #website asks for getMessage command 
            user = request[1]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(listToString(getMessagesFrom(user)),"utf-8")) #sends test list as string to be decoded by website in javascript
        
        
    def do_POST(self): #POST is when website wants to send data to the server
        print(self.requestline)
        request = requestsMaker(self.requestline)
        print(request)
        self.send_response(200)
        self.send_header("Content-type", "application/json") #sets content of message as json file
        self.end_headers()

        date = time.strftime("%Y-%m-%d",time.localtime(time.time())) #calculates test data
        self.wfile.write(bytes('{"time": "'+date+'"}',"utf-8")) #sends json file with current local time


server = HTTPServer((HOST,PORT),charlieHTTP) #starts server
print("server running")
server.serve_forever() #makes sure connection will not abruptly close
server.server_close() #stops server
print("server stoped")

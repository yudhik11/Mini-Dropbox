import os,sys,thread,socket
import time

def main():
    args = len(sys.argv)

    if (args is not 2):
        print "Syntax: python filename <port_number>"
        sys.exit(1)
    port = int(sys.argv[1]) # port from argument

    host = ''               # empty for localhost

    print "Proxy Server Running on ",host,":",port
    
    if os.path.exists('./cache') is not True:
        os.system('mkdir cache')
    
    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # associate the socket to host and port
        s.bind((host, port))

        # listening
        s.listen(10)

    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    while True:
        conn, client_addr = s.accept()
        request = conn.recv(1024)
        if len(request.split()[1]) < 12:
            conn.send("Connection Established\n")
            conn.close()
            
            continue
        thread.start_new_thread(threaded_proxy_server, (conn,request, client_addr))
    s.close()
    conn.close()


def threaded_proxy_server(conn, request, client_addr):

    get_request = request.split('\r\n')[0]
    url = get_request.split(' ')[1]
    http_ptr = url.find("://")          # find ptr of ://
    
    if http_ptr is -1:
        temp = url
    else:
        temp = url[(http_ptr+3):]       # get the rest of url
    #print temp
    port_ptr = temp.find(":")           # find the port ptr (if any)
    webserver_ptr = temp.find("/")
    
    if webserver_ptr is -1 :
        webserver_ptr = len(temp)

    webserver = ""
    port = -1
    
    if port_ptr is -1 :
        port = 80
        webserver = temp[:webserver_ptr]
    else :
        port = int(temp[(port_ptr+1):webserver_ptr])
        webserver = temp[:port_ptr]
    
    try:
        # create a socket
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print webserver, port
        soc.connect((webserver, port))
    except :
        if soc:
            soc.close()
        print "Could not connect to socket:", message
    
    tym = -1
    files = os.listdir("./cache/")
    filename = temp[webserver_ptr+1:]
    
    if filename in files:
        a = time.ctime(os.path.getmtime('./cache/' + temp[webserver_ptr+1:]))
        tym = a
    
    req = "GET  " + temp[webserver_ptr:] + " HTTP/1.1\r\n"
    
    if tym != (-1):
        req += "If-Modified-Since: " + tym + "\r\n"
    req+= "\r\n"
    try:
        soc.send(req)
    except:
        print "could not send\n"

    store = ""
    
    while True:
        data = soc.recv(1024)
        #print "data: ", data
        if data:
            store+=data
        else:
            break
    
    k = store.split('\r\n')
    state = k[0].split(' ')
    #print k, state
    status = state[1]
    reason = state[2]
    
    if status == '200':
        data = k[-1]
        if (len(store) > 0):
            conn.send(store)
        if filename in files:
            with open('./cache/' + filename,'wb') as f:
                f.write(data)
        else:
            cnt = -1 
            for i in k:
                cnt+=1
                if 'Cache-control' in i:
                    break
            if k[cnt].split(' ')[1] != 'no-cache':
                if len(files) == 3:
                    tempf = ["./cache/"+s for s in files]
                    oldest = min(tempf,key=os.path.getmtime)
                    os.system('rm -f ' +  oldest)
                with open('./cache/' + filename,'wb') as f:
                    f.write(data)

    elif status == '304':
        string  = "\r\n"
        with open('./cache/' + temp[webserver_ptr+1:],'r') as f:
            data = f.read()
            #print data
            string+=data
            conn.send(string)
        
    elif status == '404':
        if (len(store) > 0):
            conn.send(store)
    
    else:
        if (len(store) > 0):
            conn.send(store)
        
    soc.close()
    conn.close()

if __name__ == '__main__':
    main()

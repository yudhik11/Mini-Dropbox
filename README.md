# Proxy Server & Caching

- The **Proxy Server** has been implemented in **python**.
- All the files are stored in **cache** if the folder doesn't exist, program will take care of it.
- To start the proxy server write the command ***python pro_server.py <port_number>*** .
- The proxy server starts at localhost and port number which it gets as input.
- Run the main server using the command ***python server.py***.
- Use the proxy server using curl command ***curl -x proxy_server_addr:port_number  server_addr:port_number/<file_name>***

-  The data of the file is recieved by the proxy server, it sends it to the client(curl command) and is shown in the terminal from which the request is made.
-  Featres Implemented :
   -  Caching is implemented.
   -  At most 3 files/responses can be cached.
   -  ***Threading*** is implemented.
   -  If a new file is requested and the cache is full then the oldest file present in cache is removed.
   -  If a file is modified then file gets updated in cache too.
   -  **Multiple requests** can be handled by the proxy server.
   -  Error handling is done
   -  Handles directory

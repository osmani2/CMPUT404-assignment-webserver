#  coding: utf-8 
import socketserver

# NAME: Natasha Osmani
# CCID: nahmed2
# LAB: H01
#
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

from os import path 
BASE_PATH = "./www"
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        req = self.data.decode("utf-8").split('\r\n')[0].split(' ')
        print ("Got a request of: %s\n" % self.data)

        # Only allowing GET requests
        if req[0]!="GET":
            response = 'HTTP/1.1 405 Method Not Allowed\n\n'
            self.request.sendall(response.encode())
        
        # GET the requested page
        else:
            # A valid path
            if path.exists(BASE_PATH+req[1]):
                # Redirects for directories that don't end in'/'
                if (not path.isfile(BASE_PATH+req[1]) and (req[1][len(req[1])-1] != '/')):
                    req[1]+='/'
                    response = 'HTTP/1.1 301 Moved Permanently\nLocation: '+'http://127.0.0.1:8080'+req[1]+'\n\n'
                    self.request.sendall(response.encode())
                
                # Valid path, serve files
                else:
                    self.serve_files(req[1])
            
            # No such path exists
            else:
                response = 'HTTP/1.1 404 Not Found\n\n'
                self.request.sendall(response.encode())

    def serve_files(self,request):
        file_path = BASE_PATH+request
        res = 'HTTP/1.1 200 OK\n'

        # Set content type
        if ".css" in request:
            res+='Content-Type: text/css\n\n'

        elif ".html" in request:
            res+='Content-Type: text/html\n\n'

        # Serve index.html in directory
        else:
            res+='Content-Type: text/html\n\n'
            file_path +='index.html'
        
        # Attempt to open .html or .css file
        try:
            file = open(file_path, 'r')
            content = file.read()
            file.close()
            res += content
            self.request.sendall(res.encode())
        
        # Not proper directory for files
        except Exception:
            response = 'HTTP/1.1 404 Not Found\n\n'
            self.request.sendall(response.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

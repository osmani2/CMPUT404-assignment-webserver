#  coding: utf-8 
import socketserver

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

from urllib import request, error 

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        path = self.data.decode("utf-8")
        print ("Got a request of: %s\n" % self.data)

        if "GET /index.html HTTP/1.1" in path:
            self.index_html()
        
        elif "GET /base.css HTTP/1.1" in path:
            self.base_css()
        
        elif "GET /deep/deep.css HTTP/1.1" in path:
            self.deep_css()
        
        elif "GET /deep/index.html HTTP/1.1" in path:
            self.deep_index()

        elif "GET HTTP/1.1" in path:
            self.request.sendall(bytearray("OK",'utf-8'))

        else:
            response = 'HTTP/1.1 404 Not Found\n\n'
            self.request.sendall(response.encode())


    def base_css(self):
        file = open('./www/base.css', 'r')
        content = file.read()
        file.close()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/css\n\n' + content
        self.request.sendall(response.encode())

    def index_html(self):
        file = open('./www/index.html', 'r')
        content = file.read()
        file.close()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + content
        self.request.sendall(response.encode())

    def deep_css(self):
        file = open('./www/deep/deep.css', 'r')
        content = file.read()
        file.close()
        response = 'HTTP/1.1 200 OK\nContent-Type: text/css\n\n' + content
        self.request.sendall(response.encode())

    def deep_index(self):
        file = open('./www/deep/index.html', 'r')
        content = file.read()
        file.close()
        response = 'HTTP/1.1 200 OK\n\n' + content
        self.request.sendall(response.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

import socket
import select
import sys
import os

class MultiConnectionHTTPServer:
  def __init__(self, port):
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKNET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind(('', self.port))
    self.server_socket.listen(5)
    self.server_socket.setblocking(False)
    self.open_connections = {}

  def serve_forever(self):
    inpus = [self.server_socket]
    print(f"[서버 시작] 포트 {self.port}에서 대기 중...")
    while True:
      readables, _, _ = select.select(inputs, [], [])

      for sock in readables:
        if sock is self.server_socket:
          client_socket, client_address = self.server_socket.accept()
          print(f"[접속 수락] {client_address} 연결됨")
          client_socket.setblocking(False)
          inputs.append(client_socket)
          self.open_connections[client_socket] = client_address

        else:
          try:
            request = sock.recv(1024).decode()
            if not request:
              raise Exception("빈 요청")
            print(f"[요청 수신] {self.open_connecions[sock]}\n{request}")


            requse_line = request.split("\r\n")[0]
            parts = request_line.split()
            if len(parts) != 3:
              self.send_error(sock, 400, "Bad Request")
              continue
            method, path, version = parts
            if method != "GET":
              self.sned_error(sock, 405, "Method Not Allowed")
              continue

            filename = path.lstrip('/')
            if not (filename.endswith('.html') or filename.endswith('.htm)):
              self.send_error(sock, 403, "Forbidden")
              continue
            if not os.path.exists(filename):
              self.send_error(sock, 404, "Not Found")
              continue
            
                                                              
                                                            
                                                                    
            



            
           



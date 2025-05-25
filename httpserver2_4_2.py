import socket
import select
import sys
import os

class MultiConnectionHTTPServer:
  def __init__(self, port):
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind(('', self.port))
    self.server_socket.listen(5)
    self.server_socket.setblocking(False)
    self.open_connections = {}

  def serve_forever(self):
    inputs = [self.server_socket]
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
            print(f"[요청 수신] {self.open_connections[sock]}\n{request}")


            request_line = request.split("\r\n")[0]
            parts = request_line.split()
            
            if len(parts) != 3:
              self.send_error(sock, 400, "Bad Request")
              continue
              
            method, path, version = parts
            
            if method != "GET":
              self.send_error(sock, 405, "Method Not Allowed")
              continue

            filename = path.lstrip('/')
            
            if not (filename.endswith('.html') or filename.endswith('.htm')):
              self.send_error(sock, 403, "Forbidden")
              continue
              
            if not os.path.exists(filename):
              self.send_error(sock, 404, "Not Found")
              continue
              
            with open(filename, 'rb') as f:
              body = f.read()

            header = "HTTP/1.0 200 OK\r\n"
            header += "Content-Type: text/html\r\n"
            header += f"Content-Length: {len(body)}\r\n"
            header += "\r\n"

            sock.sendall(header.encode() + body)
            print(f"[응답 완료] {filename}")
         
          except Exception as e:
            print(f"[에러 발생] {e}")
            self.send_error(sock, 500, "Internal Server Error")

          finally:
            sock.close()
            inputs.remove(sock)
            del self.open_connections[sock]
          


    
  def send_error(self, sock, code, message):
    body = f"<html><body><h1>{code} {message}</h1></body></html>".encode()
    header = f"HTTP/1.0 {code} {message}\r\n"
    header += "Content-Type: text/html\r\n"
    header += f"Content-Length: {len(body)}\r\n"
    header += "\r\n"
    response = header.encode() + body
      
    try:
      sock.sendall(response)
        
    except:
      pass



if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("사용법 : python httpserver2_4_1.py [포트번호]")
    sys.exit(1)

  try:
    port = int(sys.argv[1])
    if port < 1024:
      print("포트 번호는 1024 이상이어야 합니다.")
      sys.exit(1)

  except:
    print("포트 번호는 숫자여야 합니다.")
    sys.exit(1)

  server = MultiConnectionHTTPServer(port)
  server.serve_forever()


            
           



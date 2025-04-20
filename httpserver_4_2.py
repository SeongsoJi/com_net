import socket
import sys

class SimpleHTTPServer:
    def __init__(self, port):
        print(f"[서버 시작] 포트 {port}에서 대기 중...")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)

    def start(self):
        while True:
            try:
                connection_socket, client_address = self.server_socket.accept()
                print(f"[접속] 클라이언트: {client_address}")
                self.handle_client(connection_socket)
            except Exception as e:
                print(f"[서버 오류] {e}")

    def handle_client(self, connection_socket):
        try:
            request = connection_socket.recv(1024).decode()
            print(f"[요청 내용]\n{request}")

            if not request:
                return

            request_line = request.split('\r\n')[0]
            parts = request_line.split()

            if len(parts) != 3:
                self.send_error(connection_socket, 400, "Bad Request")
                return

            method, path, version = parts

            if method != "GET":
                self.send_error(connection_socket, 405, "Method Not Allowed")
                return

            filename = path.lstrip('/')

            if not (filename.endswith('.html') or filename.endswith('.htm')):
                self.send_error(connection_socket, 403, "Forbidden")
                return

            try:
                with open(filename, 'rb') as f:
                    body = f.read()
            except FileNotFoundError:
                self.send_error(connection_socket, 404, "Not Found")
                return

            header = "HTTP/1.0 200 OK\r\n"
            header += "Content-Type: text/html\r\n"
            header += f"Content-Length: {len(body)}\r\n"
            header += "\r\n"

            connection_socket.sendall(header.encode() + body)
            print(f"[전송 완료] {filename}")

        except Exception as e:
            print(f"[오류 발생] {e}")
            self.send_error(connection_socket, 500, "Internal Server Error")

        finally:
            connection_socket.close()

    def send_error(self, sock, code, message):
        body = f"<html><body><h1>{code} {message}</h1></body></html>"
        header = f"HTTP/1.0 {code} {message}\r\n"
        header += "Content-Type: text/html\r\n"
        header += f"Content-Length: {len(body.encode())}\r\n"
        header += "\r\n"
        response = header + body
        sock.sendall(response.encode())
        sock.close()
        print(f"[에러 응답] {code} {message}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python httpserver_4_2.py [포트번호]")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if port < 1024:
            print("포트 번호는 1024 이상이어야 합니다.")
            sys.exit(1)
    except ValueError:
        print("포트 번호는 숫자여야 합니다.")
        sys.exit(1)

    server = SimpleHTTPServer(port)
    server.start()


#C:\Users\User\PycharmProjects\PythonProject1
# python httpserver_4_2.py 8000
# http://localhost:8000/rfc2616.html

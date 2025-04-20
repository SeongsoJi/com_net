import socket
import sys

def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"[서버 시작] 포트 {port}에서 대기 중...")

    while True:
        try:
            connection_socket, client_address = server_socket.accept()
            print(f"[접속] 클라이언트: {client_address}")

            request = connection_socket.recv(1024).decode()
            print(f"[요청 내용]\n{request}")

            if not request:
                connection_socket.close()
                continue

            request_line = request.split('\r\n')[0]
            parts = request_line.split()

            if len(parts) != 3:
                send_error(connection_socket, 400, "Bad Request")
                continue

            method, path, version = parts

            if method != "GET":
                send_error(connection_socket, 405, "Method Not Allowed")
                continue

            filename = path.lstrip('/')

            # 확장자 검사 먼저
            if not (filename.endswith('.html') or filename.endswith('.htm')):
                send_error(connection_socket, 403, "Forbidden")
                continue

            # 파일 열기 시도 (파일 존재 여부 확인)
            try:
                with open(filename, 'rb') as f:
                    body = f.read()
            except FileNotFoundError:
                send_error(connection_socket, 404, "Not Found")
                continue

            header = "HTTP/1.0 200 OK\r\n"
            header += "Content-Type: text/html\r\n"
            header += f"Content-Length: {len(body)}\r\n"
            header += "\r\n"

            connection_socket.sendall(header.encode() + body)
            print(f"[전송 완료] {filename}")

        except Exception as e:
            print(f"[오류 발생] {e}")
            try:
                send_error(connection_socket, 500, "Internal Server Error")
            except:
                pass

        finally:
            connection_socket.close()

def send_error(sock, code, message):
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
        print("사용법: python httpserver_4_1.py [포트번호]")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if port < 1024:
            print("⚠ 포트 번호는 1024 이상이어야 합니다.")
            sys.exit(1)
    except ValueError:
        print("⚠ 포트 번호는 숫자여야 합니다.")
        sys.exit(1)

    run_server(port)

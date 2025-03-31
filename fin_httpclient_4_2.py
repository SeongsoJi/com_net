# -*- coding: utf-8 -*-
import sys
import socket

def fetch_http(url, redirect_count=0):
    if redirect_count > 5:
        print("redirect 5회 이상", file=sys.stderr)
        sys.exit(1)

    if not url.startswith("http://"):
        print("http:// 로 시작해야 함", file=sys.stderr)
        sys.exit(1)

    url = url[7:]  # http:// 제거
    slash_index = url.find('/')

    if slash_index == -1:
        host = url
        path = '/'
    else:
        host = url[:slash_index]
        path = url[slash_index:]

    if ':' in host:
        host, port_str = host.split(':', 1)
        port = int(port_str)
    else:
        port = 80

    request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, port))
        s.sendall(request.encode())
    except Exception as e:
        print(f"연결 실패: {e}", file=sys.stderr)
        sys.exit(1)

    response = b''
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
    s.close()

    decoded = response.decode(errors="ignore")
    header_data, _, body = decoded.partition("\r\n\r\n")
    status_line = header_data.split("\r\n")[0]

    try:
        status_code = int(status_line.split()[1])
    except:
        print("잘못된 응답", file=sys.stderr)
        sys.exit(1)

    content_type = ""
    location = ""
    for line in header_data.split("\r\n"):
        if line.lower().startswith("content-type:"):
            content_type = line.split(":", 1)[1].strip()
        elif line.lower().startswith("location:"):
            location = line.split(":", 1)[1].strip()

    if status_code in (301, 302):
        print(f"{status_code} 리디렉션됨 → Location: {location}", file=sys.stderr)
        if location.startswith("https://"):
            print("HTTPS 주소 불가", file=sys.stderr)
            sys.exit(1)
        return fetch_http(location, redirect_count + 1)


    if status_code >= 400:
        print(body)
        sys.exit(1)

    if not content_type.startswith("text/html"):
        print(f"지원하지 않는 Content-Type: {content_type}", file=sys.stderr)
        sys.exit(1)

    print(body)
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python http.py http://주소 형식 입력", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    fetch_http(url)

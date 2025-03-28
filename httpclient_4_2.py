import socket # 인터넷 연결을 위한 파이썬 도구임
import sys # 사용자 입력을 받기 위한 도구임

if len(sys.argv) < 2:
    print("다음과 같이 cmd창에 입력해: python httpclient.py http://주소")
    sys.exit(1)

url = sys.argv[1] # # 명령줄에서 입력한 URL 가져오기

if not url.startswith("http://"):
    print("오류: http://로 시작하는 주소만 입력해.")
    sys.exit(1)

# URL에서 필요한 정보(호스트와 경로)를 뽑아내기
url = url[7:]  # "http://" 부분은 잘라내기
parts = url.split("/", 1)  # '/' 기준으로 나누기

host = parts[0]  # 예: example.com
path = "/" + parts[1] if len(parts) > 1 else "/"  # 예: /index.html

#소켓(통신 도구)를 만든다. 전화기 같은 개념
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, 80))  # 포트 80은 HTTP 기본 포트라고함, 주소와 80번 포트로 연결을 시도한다.
except:
    print("서버 연결 실패!")
    sys.exit(1)

# HTTP 요청 만들기
# 중요한 두 줄: GET 요청과 Host 헤더
request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
client_socket.send(request.encode())  # 요청 보내기 (문자 → 바이트), 서버에 HTML 좀 주세요... 요청

# 응답 받기
response = b""  # 빈 바이트 문자열
while True: # 다 받을 때까지 반복해서 받을거임
    data = client_socket.recv(4096)  # 4096바이트씩 받기, 서버가 보내준 HTML 데이터를 받는다. 근데 왜 4096바이트? -> 가장 흔히 씀.
    # 너무 작게 받으면 자주 통신해야 해서 느려지고, 너무 크게 받으면 메모리를 낭비할 수 있는데 적당한 크기이다.
    if not data:
        break
    response += data

client_socket.close()  # 연결 종료 (전화 끊기)

# 받은 응답을 화면에 보여주기
try:
    print(response.decode())  # 바이트 → 문자열로 변환 후 출력
except:
    print("응답 해석 불가.")
    sys.exit(1)
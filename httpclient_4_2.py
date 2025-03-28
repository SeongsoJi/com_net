import socket # 인터넷 연결을 위한 파이썬 도구임
import sys # 사용자 입력을 받기 위한 도구임

# 리다이렉트 너무 많이 되면 중단할거임
MAX_REDIRECTS = 5

def fetch_page(url, count=0):
    if count > MAX_REDIRECTS:
        print("리다이렉트 5번 넘었음. 그만할게요")
        sys.exit(1)

    if not url.startswith("http://"):
        print("오류: http://로 시작하는 주소만 입력해.")
        sys.exit(1)
        
    # http:// 잘라내기
    url = url[7:]
    # (Rules to follow 10번)
    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    # 포트 번호 처리(Rules to follow 10번)
    if ":" in host_and_port:
        host, port_str = host_and_port.split(":", 1)
        try:
            port = int(port_str)
        except:
            print("포트 번호가 이상함!.")
            sys.exit(1)
    else:
        host = host_and_port
        port = 80  # 기본 포트

    # 소켓 만들고 연결하기
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, 80))
    except:
        print("서버 연결 실패함")
        sys.exit(1)

    # 요청 메시지 만들기
    req = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    sock.send(req.encode())

    # 응답 받기(Rules to follow 12번) 크고 긴 HTML 페이지도 처리할 수 있어야 한다. -> 한 번의 recv()로 다 못 받을 수 있으니까, 반복해서 받자
    res = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        res += part

    sock.close()

    try:
        res_text = res.decode()
    except:
        print("응답 해석 실패")
        sys.exit(1)

    # 상태 코드 뽑기
    first_line = res_text.split("\r\n")[0]
    code = int(first_line.split()[1])
    print("상태 코드:", code)

    # 리다이렉트면 다시 fetch_page 호출
    if code == 301 or code == 302:
        for line in res_text.split("\r\n"):
            if line.lower().startswith("location:"):
                newurl = line.split(":", 1)[1].strip()

                # 리다이렉트된 새 주소가 https://로 시작하면 종료
                if newurl.startswith("https://"):
                    print("https로 리다이렉트 됨. 종료할게.", file=sys.stderr)
                    sys.exit(1)
                    
                print("Redirected to:", newurl, file=sys.stderr)  # stderr 출력 추가
                print("리다이렉트 감지! 새 주소로 이동:", newurl)
                return fetch_page(newurl, count + 1)
        
        print("Location 헤더 못 찾음...")
        sys.exit(1)

    # 400 이상 에러 처리
    if code >= 400:
        print("\n========== 에러 응답 ==========\n")
        print(res_text)
        sys.exit(1)  # 실패 종료

    # Content-Type 검사
    content_type = ""
    for line in res_text.split("\r\n"):
        if line.lower().startswith("content-type:"):
            content_type = line.split(":", 1)[1].strip().lower()
            break

    if not content_type.startswith("text/html"):
        print(f"Content-Type이 text/html이 아님: {content_type}")
        sys.exit(1)  # 실패 처리
    
    # 정상 응답이면 출력
    print("\n========== 결과 출력 ==========\n")
    print(res_text)
    sys.exit(0)  # 성공 종료

# 시작 부분
if len(sys.argv) < 2:
    print("cmd 창에 다음과 같이 입력해: python 파일명.py http://주소")
    sys.exit(1)

fetch_page(sys.argv[1])

import socket

HOST = ''
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #소켓 객체 생성
    #어드레스 패밀리(IPv4), 소켓타입
    s.bind((HOST, PORT)) #소켓과 AF 연결
    s.listen(1) #상대방의 접속이 올 때까지 대기. 큐 사이즈 1로 설정
    print('Start server')

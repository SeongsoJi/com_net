네트워크 소켓 프로그래밍 과제
작업 계획!!
URL 파싱	: 사용자가 준 URL에서 도메인, 포트, 경로(path)를 분리
소켓 생성	: socket.socket()으로 소켓 만들기
서버에 연결	: socket.connect((host, port))
HTTP GET 요청 보내기 :	요청 메시지 직접 만들기 (GET / HTTP/1.0\r\nHost: ...)
응답 받기	: recv() 반복해서 읽기
HTML 출력	: 응답에서 body만 골라 출력
리다이렉트 처리	: 301/302 코드면 다시 요청 보내기 (최대 5번)
오류 처리	: http://로 안 시작하거나, https는 못 다루는 등

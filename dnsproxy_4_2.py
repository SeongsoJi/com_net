import socket
import sys

class DNSProxy:
  def __init__(self, listen_host='0.0.0.0', listen_port = 1053, upstream_dns=('8.8.8.8', 53), fake_ip='203.0.113.1'):
    self.listen_host = listen_host
    self.listen_port = listen_port
    self.upstream_dns = upstream_dns
    self.fake_ip = fake_ip
    self.buffer_size = 512
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


  def start(self):
    try:
      self.server_socket.bind((self.listen_host, self.listen_port))
      print("DNS 프록시가 {self.listen_host}:{self.listen_port}에서 수신 대기 중입니다")

      while True:
        data, client_addr = self.server_socket.recvform(self.buffer_size)
        print(f"{client_addr}로부터 DNS 요청을 받았습니다")
        
        self.server_socket.sendto(data, self.upstream_dns)
        response, _ = self.server_socket.recvfrom(self.buffer_size)
        
        if self.is_nxdomain(response):
          print("NXDOMAIN(도메인 없음) 응답 감지됨 → 조작된 응답을 전송합니다")
          response = self.craft_fake_response(data)

        self.server_socket.sendto(response, client_addr)
        print(f"{client_addr}에게 응답을 전송했습니다")

    except KeyboardInterrupt:
      print("DNS 프록시를 종료합니다.")
    finally:
      self.server_socket.close()

  def is_nxdomain(self, data):
    flags_high = data[2]
    flags_low = data[3]
    rcode = flags_low & 0x0F
    return rcode ==3

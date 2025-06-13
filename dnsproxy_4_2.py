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

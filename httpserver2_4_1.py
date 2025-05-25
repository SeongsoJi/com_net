import socket
import select
import sys
import os

class MultiConnectionHTTPServer:
  def __init__(self, port):
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKNET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind(('', self.port))
    self.server_socket.listen(5)
    self.server_socket.setblocking(False)
    self.open_connections = {}



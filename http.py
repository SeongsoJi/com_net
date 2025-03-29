import sys
import socket

if len(sys.argv) != 2:
  print("python http.py http://주소 형식 입력", file=sys.stderr)
  sys.exit(1)

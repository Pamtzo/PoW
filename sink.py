import sys
import time
import zmq
import hashlib

def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

context = zmq.Context()

fan = context.socket(zmq.REQ)
fan.bind("tcp://*:5558")

work = context.socket(zmq.PULL)
work.bind("tcp://*:5559")

workers=0
while True:
    if work.recv_string()=="Ok":
        break
    workers+=1
fan.send_string(str(workers))
fan.recv_string()

o_challenge=hashString("CS-rocks!")
fan.send_string(o_challenge)

# Process 100 confirmations
fan.recv_string()
while True:
    answer = work.recv_multipart()
    print(answer)
    if answer[0].decode()==o_challenge:
        fan.send_string(answer[1].decode())
        o_challenge=answer[1].decode()
        fan.recv_string()
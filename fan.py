import zmq
import random
import time

context = zmq.Context()

# socket with workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket with sink
sink = context.socket(zmq.REP)
sink.connect("tcp://localhost:5558")

sink2 = context.socket(zmq.PUSH)
sink2.connect("tcp://localhost:5559")

print("Press enter when workers are ready...")
_ = input()
print("sending tasks to workers")

sink2.send_string('Ok')
n=int(sink.recv_string())#workers
print("somos %i trabajadores" % n)
sink.send_string("Ok")
random.seed()

while True:
    challenge=sink.recv_string()
    print("The challenge is %s" % challenge)
    for w in range(n):
        workers.send_string(challenge)
    sink.send_string('Ok')
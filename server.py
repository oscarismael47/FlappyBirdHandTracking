
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5555")
# Process tasks forever
while True:
    s = socket.recv_string()
    print('received {}'.format(s))
    time.sleep(2)
    print('value: {}'.format(s)) 
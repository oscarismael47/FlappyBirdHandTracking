import zmq

context = zmq.Context()

# Socket to send messages on
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")

for i in range(30):
    print('sending {}'.format(i))
    socket.send_string(str(i))

import socket
import struct
import base64
import time
from locust import User, task, events

class TcpClientUser(User):

    @task
    def send_and_receive_message(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 4000))
        while True:
            start_time = time.time()

            try:
                encoded_message_base64 = "CgRsZW5hEM3p7agGIgVoZWxsbw=="
                decoded_message = base64.b64decode(encoded_message_base64)

                message_length = len(decoded_message)

                s.sendall(struct.pack('!I', message_length))
                s.sendall(decoded_message)

                length_data = s.recv(4)
                message_length = struct.unpack('!I', length_data)[0]
                received_data = s.recv(message_length)

                total_time = int((time.time() - start_time) * 1000)  # ms로 변환
                events.request.fire(request_type="tcp", name="send_and_receive_message",
                                    response_time=total_time, response_length=message_length, 
                                    exception=None, context={})

            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)  # ms로 변환
                events.request.fire(request_type="tcp", name="send_and_receive_message",
                                    response_time=total_time, response_length=0, 
                                    exception=e, context={})

            time.sleep(2)

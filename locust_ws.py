import base64
import time
from locust import User, task, events
import websocket

class WebsocketClientUser(User):

    @task
    def send_and_receive_message(self):
        start_time = time.time()
        ws = websocket.create_connection("ws://localhost:4001/ws")
        while True:
            try:
                encoded_message_base64 = "CgRsZW5hEM3p7agGIgVoZWxsbw=="
                decoded_message = base64.b64decode(encoded_message_base64)

                ws.send(decoded_message, opcode=websocket.ABNF.OPCODE_BINARY)

                received_data = ws.recv()

                total_time = int((time.time() - start_time) * 1000)
                message_length = len(received_data)
                events.request.fire(request_type="websocket", name="send_and_receive_message",
                                    response_time=total_time, response_length=message_length,
                                    exception=None, context={})

            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request.fire(request_type="websocket", name="send_and_receive_message",
                                    response_time=total_time, response_length=0,
                                    exception=e, context={})
            time.sleep(2)
        


import json
import socket

# from face_recognition.face_recognition import FaceRecognition
# from image_to_text.image_to_text import ImageToText
# from vqa.vqa import Vqa
import threading


class Server:
    def __init__(self, host=socket.gethostname(), port=1234):
        self.host = host
        self.port = port
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        # self.vqa = Vqa()
        # self.face_recognition = FaceRecognition()
        # self.image_to_text = ImageToText()

        self.client_socket, self.address = None, None

    def handle_client_connection(self, client_socket):
        message = client_socket.recv(100000)
        message = json.loads(message)
        print(message)
        type = message["type"].lower()
        # image = message["image"]
        # image = base64.decodebytes(image)
        result = {"result": 'test'}
        if type == "visual-question-answering":
            question = message["question"]
            result["result"] = self.vqa.predict(question, image)
        elif type == "face-recognition":
            result["result"] = self.face_recognition.predict(image)
        elif type == "image-to-text":
            result["result"] = self.image_to_text.predict(image)
        result = json.dumps(result)
        client_socket.send(result.encode())

    def start(self):
        print('server started at {}:{}'.format(self.host, str(self.port)))
        while True:
            client_socket, address = self.socket.accept()
            print('Accepted connection from {}:{}'.format(address[0], address[1]))

            client_handler = threading.Thread(
                target=self.handle_client_connection,
                args=(client_socket,)
            )
            client_handler.start()

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    try:
        server.start()
    except:
        print('server stopped')
    finally:
        server.close()

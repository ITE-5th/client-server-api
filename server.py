import base64
import json
import socket

from face_recognition.face_recognition import FaceRecognition
from image_to_text.image_to_text import ImageToText
from vqa.vqa import Vqa


class Server:
    def __init__(self, host=socket.gethostname(), port=8888):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        self.vqa = Vqa()
        self.face_recognition = FaceRecognition()
        self.image_to_text = ImageToText()

    def start(self):
        while True:
            message, _ = self.receive()
            message = json.loads(message)
            type = message["type"].lower()
            image = message["image"]
            image = base64.decodebytes(image)
            result = {}
            if type == "visual-question-answering":
                question = message["question"]
                result["result"] = self.vqa.predict(question, image)
            elif type == "face-recognition":
                result["result"] = self.face_recognition.predict(image)
            elif type == "image-to-text":
                result["result"] = self.image_to_text.predict(image)
            result = json.dumps(result)
            self.send(result)

    def receive(self):
        return self.socket.recv(100000)

    def send(self, result):
        self.socket.send(result)

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    try:
        server.start()
    finally:
        server.close()

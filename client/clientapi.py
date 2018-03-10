from TTS import TTS

# from client.camera import Camera
from client.recognizer import Recognizer
from lib.socket import Client


class ClientApi:
    def __init__(self, port=8001, host='localhost'):
        self.host = host
        self.port = port
        # self.cam = Camera()
        self.client = Client()
        self.tts = TTS()
        self.recognizer = Recognizer(server=self)

    def start(self):
        self.client.connect(self.host, self.port)

        #     start recogniser
        self.recognizer.start()

    def close(self):
        self.client.close()

    def send(self):
        self.client.send(self._build_message('caption'))
        response = self.client.recv()
        self.tts.say(response['result'])

    def _build_message(self, type, question=None):
        # type == "visual-question-answering"
        # type == "face-recognition"
        # type == "image-to-text"

        if question is None:
            return {
                "type": type,
                # "image": self.cam.take_image(),
            }
        return {
            "type": "visual-question-answering",
            # "image": self.cam.take_image(),
            "question": question,
        }


if __name__ == '__main__':
    api = ClientApi()
    api.start()

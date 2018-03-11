import json
import socket

from TTS import TTS


# from client.camera import Camera


class Client:
    def __init__(self, host=socket.gethostname(), port=1234):
        self.host = host
        self.port = port
        # self.cam = Camera()
        self.tts = TTS(festival=False, espeak=False, pico=True)
        # self.recognizer = Recognizer(server=self)

        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect the client
        # client.connect((target, port))

    def start(self):
        print('connected to server ' + self.host + ':' + str(self.port))

        self.socket.connect((self.host, self.port))
        self.send()
        self.send()
        self.send()
        self.send()
        self.close()
        #     start recogniser
        # self.recognizer.start()

    def close(self):
        self.socket.close()

    def send(self):
        message = self._build_message('caption')
        self.socket.send(message)
        response = self.socket.recv(4096)
        response = json.loads(response)

        self.tts.say(response['result'])

    def _build_message(self, type, question=None):
        # type == "visual-question-answering"
        # type == "face-recognition"
        # type == "image-to-text"

        if question is None:
            return json.dumps(
                {
                    "type": type,
                    "image": "",
                    # "image": self.cam.take_image(),
                }).encode()
        return json.dumps({
            "type": "visual-question-answering",
            "image": "",
            # "image": self.cam.take_image(),
            "question": question,
        }).encode()


if __name__ == '__main__':
    api = Client()
    api.start()

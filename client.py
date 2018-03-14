import base64
import socket
# from client.camera import Camera
import time

import speech_recognition as sr

from client.TTS import TTS
# from client.recognizer import Recognizer
# from client.speaker import Speaker
# from client.speaker import SpeakersModel
from helper import Helper


class ClientAPI:
    def __init__(self, speaker_name, host=socket.gethostname(), port=1234):
        self.host = host
        self.port = port
        self.speaker_name = speaker_name
        # self.cam = Camera()
        self.tts = TTS(festival=False, espeak=False, pico=True)
        # self.recognizer = Recognizer(server=self)
        # response now is {'data': {'some_list': [123, 456]}}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        print('connected to server ' + self.host + ':' + str(self.port))

        self.socket.connect((self.host, self.port))
        #     start recogniser
        # self.recognizer.start(self.audio_recorder_callback)
        self.audio_recorder_callback('')

    def audio_recorder_callback(self, fname):
        # verify speaker
        threshold = 0.1
        # if self.get_speaker(fname) > threshold:
        #     print("converting audio to text")
        #     speech = self.speech_to_text(fname)
        while threshold > 0:
            speech = 'test message'
            message = self._build_message('vqa', question=speech)
            self.communicate_with_server(message)
            threshold -= 0.1
            time.sleep(1)
        # else:
        #     print('speaker is not verified')
        # os.remove(fname)

    def get_speaker(self, fname):
        # Speaker() used for import speaker class only
        Speaker(name='test')
        model: SpeakersModel = SpeakersModel.load("models/gmms.model")
        return model.verify_speaker(fname, self.speaker_name.title())

    def speech_to_text(self, fname):
        r = sr.Recognizer()
        with sr.AudioFile(fname) as source:
            audio = r.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            print("Sphinx thinks you said " + r.recognize_sphinx(audio))

        except sr.UnknownValueError:
            print("Sphinx could not understand audio")

        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
        googleSTT = ''
        try:
            googleSTT = r.recognize_google(audio)
            print(googleSTT)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return googleSTT

    def close(self):
        self.socket.close()

    def communicate_with_server(self, message):
        Helper.send_json(self.socket, message)
        response = Helper.receive_json(self.socket)
        print(response)

        # self.tts.say(response['result'])

    def _build_message(self, type, question=None):
        # type == "visual-question-answering"
        # type == "face-recognition"
        # type == "image-to-text"
        with open("test.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        json_data = {
            "type": type,
            "image": encoded_string,
        }
        if question is not None:
            json_data["question"] = question
        # print('json_data')
        # print(json_data)
        return json_data


if __name__ == '__main__':
    api = ClientAPI(speaker_name='zaher')
    try:
        api.start()
    finally:
        api.close()

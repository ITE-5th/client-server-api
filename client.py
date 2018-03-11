import json
import os
import socket

import speech_recognition as sr

# from client.camera import Camera
from client.TTS import TTS
from client.recognizer import Recognizer
from client.speaker import Speaker
from client.speaker import SpeakersModel


class Client:
    def __init__(self, speaker_name, host=socket.gethostname(), port=1234):
        self.host = host
        self.port = port
        self.speaker_name = speaker_name
        # self.cam = Camera()
        self.tts = TTS(festival=False, espeak=False, pico=True)
        self.recognizer = Recognizer(server=self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        print('connected to server ' + self.host + ':' + str(self.port))

        self.socket.connect((self.host, self.port))
        #     start recogniser
        self.recognizer.start(self.audio_recorder_callback)

    def audio_recorder_callback(self, fname):
        # verify speaker
        threshold = 0.5
        if self.get_speaker(fname) > threshold:
            print("converting audio to text")
            speech = self.speech_to_text(fname)
            message = self._build_message('vqa', question=speech)
            self.communicate_with_server(message)
        else:
            print('speaker is not verified')
        os.remove(fname)

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
            # "type": "visual-question-answering",
            "type": type,
            "image": "",
            # "image": self.cam.take_image(),
            "question": question,
        }).encode()


if __name__ == '__main__':
    api = Client(speaker_name='zaher')
    try:
        api.start()
    finally:
        api.close()

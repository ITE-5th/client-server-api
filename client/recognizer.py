import os
import signal
import speech_recognition as sr

from client import snowboydecoder

interrupted = False


class Recognizer:
    def __init__(self, pmdl_path=None, sensitivity=0.38, sphinx=True, google=True, server=None):
        if pmdl_path is None:
            pmdl_path = ['./resources/models/snowboy.umdl']

        model = pmdl_path
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        self.detector = snowboydecoder.HotwordDetector(model, sensitivity=sensitivity)
        self.sphinx = sphinx
        self.google = google
        self.server = server

    def start(self):
        # main loop
        print('Listening... Press Ctrl+C to exit')
        self.detector.start(detected_callback=self.detectedCallback,
                            audio_recorder_callback=self.audioRecorderCallback,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.01)

        self.detector.terminate()

    def audioRecorderCallback(self, fname):

        print("converting audio to text")
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

        try:
            print(r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove(fname)

    def detectedCallback(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        print('recording audio...', end='', flush=True)

    def signal_handler(self, signal, frame):
        global interrupted
        interrupted = True

    def interrupt_callback(self):
        global interrupted
        return interrupted


if __name__ == '__main__':
    r = Recognizer()
    r.start()

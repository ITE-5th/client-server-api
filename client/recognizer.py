import signal

from client import snowboydecoder

interrupted = False


class Recognizer:
    def __init__(self, pmdl_path=None, sensitivity=0.38, sphinx=True, google=True, server=None):
        if pmdl_path is None:
            pmdl_path = ['./client/resources/models/snowboy.umdl']

        model = pmdl_path
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        self.detector = snowboydecoder.HotwordDetector(model, sensitivity=sensitivity)
        self.sphinx = sphinx
        self.google = google
        self.server = server

    def start(self, callback_function):
        # main loop
        print('Listening... Press Ctrl+C to exit')
        self.detector.start(detected_callback=self.detectedCallback,
                            audio_recorder_callback=callback_function,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.01)

        self.detector.terminate()

    def detectedCallback(self):
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        print('recording audio...')

    def signal_handler(self, signal, frame):
        global interrupted
        interrupted = True

    def interrupt_callback(self):
        global interrupted
        return interrupted


if __name__ == '__main__':
    r = Recognizer()
    r.start()

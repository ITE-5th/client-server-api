import signal

from client import snowboydecoder

interrupted = False


class Recognizer:
    def __init__(self, pmdl_path=None, sensitivity=0.38, sphinx=True, google=True, server=None):
        if pmdl_path is None:
            pmdl_path = [
                '../client/resources/models/snowboy.umdl',
                '../client/resources/models/alexa.umdl',
                '../client/resources/models/smart_mirror.umdl',
                '../client/resources/models/alexa_02092017.umdl'
            ]

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
        callbacks = [lambda: [snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)],
                     lambda: [
                         snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG),
                         callback_function(hotword_id='caption')
                     ],
                     lambda: [
                         snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG),
                         callback_function(hotword_id='ocr')
                     ],
                     lambda: [
                         snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG),
                         callback_function(hotword_id='face')
                     ]]

        acallbacks = [lambda fname: callback_function(fname, hotword_id='vqa'), None, None, None]

        self.detector.start(detected_callback=callbacks,
                            audio_recorder_callback=acallbacks,
                            interrupt_check=self.interrupt_callback,
                            sleep_time=0.01)

        self.detector.terminate()

    def signal_handler(self, signal, frame):
        global interrupted
        interrupted = True

    def interrupt_callback(self):
        global interrupted
        return interrupted


if __name__ == '__main__':
    r = Recognizer()
    r.start()

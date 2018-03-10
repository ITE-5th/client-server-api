import os


class Speaker:
    def __init__(self, festival=True, espeak=True, pico=True):
        self.Festival = festival
        self.Espeak = espeak
        self.Pico = pico

    def say(self, message):
        if self.Festival:
            print('Festival Text to Speech')
            os.system('echo "' + message + '" | festival --tts')

        if self.Espeak:
            print('Espeak Text to Speech')
            os.system('espeak -ven+f3 -k5 -s150 "' + message + '"')

        if self.Pico:
            print('Pico Text to Speech')
            os.system('pico2wave -w voice.wav "' + message + '" && aplay voice.wav')


if __name__ == '__main__':
    Speaker(festival=True, espeak=True, pico=True).say('Hello World')
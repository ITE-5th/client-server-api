import base64

import picamera


class Camera:
    def __init__(self, width=800, height=600, vflip=True):
        self.camera = picamera.PiCamera()
        self.camera.vflip = vflip
        self.camera.resolution = (width, height)

    def take_image(self):
        file_name = 'Image.jpg'
        self.camera.capture(file_name)
        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string


if __name__ == '__main__':
    c = Camera(width=800, height=100)
    print(c.take_image())
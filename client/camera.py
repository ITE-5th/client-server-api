import base64


import picamera


class Camera:
    def __init__(self, width=800, height=600, vflip=True, hflip=True):
        self.camera = picamera.PiCamera()
        self.camera.vflip = vflip
        self.camera.hflip = hflip
        self.camera.resolution = (width, height)

    def take_image(self):
        file_name = 'client/temp/Image.jpg'
        self.camera.capture(file_name)
        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # with open("../Image.jpg", "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string


if __name__ == '__main__':
    c = Camera(width=50, height=50)
    print(c.take_image())

import os
import socket
# from face_recognition.face_recognition import FaceRecognition
# from image_to_text.image_to_text import ImageToText
# from vqa.vqa import Vqa
import threading

from helper import Helper


class Server:
    def __init__(self, host=socket.gethostname(), port=1235):
        self.host = host
        self.port = port
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        # self.vqa = Vqa()
        # self.face_recognition = FaceRecognition()
        # self.image_to_text = ImageToText()
        self.client_socket, self.address = None, None

    def handle_client_connection(self, client_socket):
        try:
            while True:
                message = Helper.receive_json(client_socket)
                # message = client_socket.recv(100000)
                # message = json.loads(message)
                # print("message\n")
                # print(message)
                if message != '':
                    img_data, question, type = self.get_data(message)
                    # nparr = np.fromstring(base64.decodebytes(img_data.encode()), np.uint8)
                    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    # img = cv2.imread('D:\Projects\PycharmProjects\mclient-server-api\images.jpg')
                    # cv2.imshow('Image', img)
                    # with open("imageToSave.jpg", "wb") as fh:
                    #     fh.write(base64.decodebytes(img_data.encode('utf-8')))
                    result = {"result": question}
                    if type == "visual-question-answering":
                        result["result"] = self.vqa.predict(question, image)
                    elif type == "face-recognition":
                        result["result"] = self.face_recognition.predict(image)
                    elif type == "image-to-text":
                        result["result"] = self.image_to_text.predict(image)
                    Helper.send_json(client_socket, result)
        except:
            print('Client Disconnected stopped')
        finally:
            client_socket.close()

    def get_data(self, message):
        type = ''
        img_data = ''
        question = ''
        try:
            type = message['type'].lower()
            img_data = message["image"]
            question = message["question"]
        finally:
            return img_data, question, type

    def start(self):
        print('server started at {}:{}'.format(self.host, str(self.port)))
        while True:
            client_socket, address = self.socket.accept()
            print('Accepted connection from {}:{}'.format(address[0], address[1]))

            client_handler = threading.Thread(
                target=self.handle_client_connection,
                args=(client_socket,)
            )
            client_handler.start()

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    # when server Address already in use
    os.system('ps -fA | grep python | tail -n1 | awk \'{ print $3 }\'|xargs kill')
    server = Server(host='localhost')

    try:
        server.start()
    except:
        print('server stopped')
    finally:
        server.close()

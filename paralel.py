import threading
import xmlrpc.client
import os

LISTEN_PORT = 6969
LISTEN_HOST = "127.0.0.1"

proxy = xmlrpc.client.ServerProxy(f'http://{LISTEN_HOST}:{LISTEN_PORT}')
lock = threading.Lock()


class Downloads(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.file = file

    def run(self):
        if os.path.exists(f'downloaded/{self.file}'):
            print("File already exist !!")
        else:
            # Write file from server to download directory
            with lock:
                with open(f'downloaded/{self.file}', 'wb') as writer:
                    data = proxy.download(self.file).data
                    writer.write(data)
            print('Download berhasil !!')


class Uploads(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.file = file

    def run(self):
        if os.path.exists(f'storage/{self.file}'):
            print("File already exist !!")
        else:
            # Write file from client to storage directory
            with lock:
                with open(self.file, 'rb') as data:
                    raw_data = xmlrpc.client.Binary(data.read())
                    is_uploaded = proxy.upload(raw_data, self.file)
                    if not is_uploaded:
                        print("File already exists !!")
            print('Upload berhasil !!')

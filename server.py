from xmlrpc.server import SimpleXMLRPCServer

import xmlrpc.client
import os

LISTEN_PORT = 6969
LISTEN_HOST = "127.0.0.1"


def download(file_name):
    if os.path.exists(f'storage/{file_name}'):
        with open(f'storage/{file_name}', 'rb') as file:
            return xmlrpc.client.Binary(file.read())
    else:
        print("Error: File not found")
        return xmlrpc.client.Binary(b'Error: File not found !!')


def upload(file_data, filename):
    if not os.path.exists(f'storage/{filename}'):
        with open(f"storage/{filename}", 'wb') as file:
            file.write(file_data.data)
            return True
    else:
        print('Error: File already exists')
        return False


def show_al_files():
    files = ','.join(os.listdir('storage')).encode()
    return xmlrpc.client.Binary(bytes(files))


# Create server
server = SimpleXMLRPCServer((LISTEN_HOST, LISTEN_PORT))

# Register function to RPC
server.register_function(download, 'download')
server.register_function(upload, 'upload')
server.register_function(show_al_files, 'show_all_files')

print(f"Listen on {LISTEN_HOST}:{LISTEN_PORT}")

server.serve_forever()

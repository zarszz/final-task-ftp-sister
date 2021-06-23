from paralel import Downloads, Uploads

import xmlrpc.client
import os

LISTEN_PORT = 6969
LISTEN_HOST = "127.0.0.1"

proxy = xmlrpc.client.ServerProxy(f'http://{LISTEN_HOST}:{LISTEN_PORT}')


def upload():
    # Create storage folder if not exist
    if not os.path.exists(os.getcwd() + '/storage'):
        os.mkdir('storage')

    os.system("clear")

    # Get all files in current work directory
    files = os.listdir(os.getcwd())
    for i in range(len(files)):
        print(f"{i + 1}.{files[i]}")

    # Select the file that will uploaded to server
    choice = int(input("Silahkan pilih file diatas")) - 1
    if choice not in range(len(files)):
        print('Pilihan tidak valid !!')
        exit(1)

    # Write file to storage directory
    with open(files[choice], 'rb') as data:
        raw_data = xmlrpc.client.Binary(data.read())
        is_uploaded = proxy.upload(raw_data, files[choice])
        if not is_uploaded:
            print("File already exists !!")


def download():
    # Create downloaded folder if folder not exist
    if not os.path.exists(os.getcwd() + '/downloaded'):
        os.mkdir('downloaded')

    # Retrieve list of files that available in server storage
    files = str(proxy.show_all_files()).split(',')

    # Select available file to download
    print('Silahkan pilih yang akan di download')
    for i in range(len(files)):
        print(f'{i + 1}. {files[i]}')
    choice = int(input('Masukkan pilihan anda -> '))
    filename = files[choice - 1]

    # Check if that file is exist in download directory
    if os.path.exists(f'downloaded/{filename}'):
        print('Ooopss.. File already exist !!')
        exit(0)

    # Write file from server to download directory
    with open(f'downloaded/{filename}', 'wb') as writer:
        data = proxy.download(filename).data
        writer.write(data)
    print('Download berhasil !!')


def downloads():
    file_array = []
    is_finished = False
    # Create downloaded folder if folder not exist
    if not os.path.exists(os.getcwd() + '/downloaded'):
        os.mkdir('downloaded')

    # Retrieve list of files that available in server storage
    files = str(proxy.show_all_files()).split(',')

    # Select available file to download
    while not is_finished:
        print(f'File yang akan di download adalah : \n {",".join(file_array)}')
        print('Silahkan pilih yang akan di download')
        for i in range(len(files)):
            print(f'{i + 1}. {files[i]}')
        print(f'{len(files) + 1}. Cukup')
        choice = int(input('Masukkan pilihan anda -> '))
        if choice == len(files) + 1:
            is_finished = True
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Downloads(file)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)
    finally:
        print("Success")


def uploads():
    file_array = []
    is_finished = False

    # Retrieve list of files that available in server storage
    files = os.listdir(os.getcwd())

    # Select available file to download
    while not is_finished:
        print(f'File yang akan di upload adalah : \n {",".join(file_array)}')
        print('Silahkan pilih yang akan di upload')
        for i in range(len(files)):
            print(f'{i + 1}. {files[i]}')
        print(f'{len(files) + 1}. Cukup')
        choice = int(input('Masukkan pilihan anda -> '))
        if choice == len(files) + 1:
            is_finished = True
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Uploads(file)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)
    finally:
        print("Operasi berhasil ....")

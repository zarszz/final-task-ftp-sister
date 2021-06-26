from progress.spinner import PixelSpinner
from tabulate import tabulate

from processing import Downloads, Uploads

import xmlrpc.client
import os
import time

LISTEN_PORT = 6969
LISTEN_HOST = "127.0.0.1"

proxy = xmlrpc.client.ServerProxy(f'http://{LISTEN_HOST}:{LISTEN_PORT}')


def loading(loading_time):
    spinner = PixelSpinner('Loading ')
    for _ in range(loading_time):
        time.sleep(0.5)
        spinner.next()
    print("\n")


def login(username, password):
    return proxy.login(f'{username},{password}')


def upload(username):
    os.system("clear")

    # Get all files in current work directory
    files = os.listdir(os.getcwd())
    for i in range(len(files)):
        print(f"{i + 1}.{files[i]}")
    print(f'{len(files) + 1}. Kembali')
    # Select the file that will uploaded to server
    choice = int(input(f"Silahkan pilih file diatas(1-{len(files) + 1}) -> ")) - 1
    if choice not in range(len(files) + 1):
        print('Pilihan tidak valid !!')
        loading(2)
        from cli import main
        main(username)

    if choice == len(files):
        from cli import main
        main(username)
    else:
        # Write file to storage directory
        with open(files[choice], 'rb') as data:
            raw_data = xmlrpc.client.Binary(data.read())
            is_uploaded = proxy.upload(raw_data, files[choice], username)
            if not is_uploaded:
                print("File already exists !!")
        loading(3)
        print("Operasi berhasil !!")


def download(username):
    # Create downloaded folder if folder not exist
    if not os.path.exists(os.getcwd() + '/downloaded'):
        os.mkdir('../downloaded')

    # Retrieve list of files that available in server storage
    files = str(proxy.show_all_files()).split(',')

    # Select available file to download
    print("Silahkan pilih yang akan di download")
    for i in range(len(files)):
        print(f'{i + 1}. {files[i]}')
    print(f'{len(files) + 1}. Kembali')
    choice = int(input(f"Masukkan pilihan anda (1-{len(files) + 1}) -> "))

    if choice not in range(len(files) + 2):
        print('Pilihan tidak valid !!')
        loading(2)
        from cli import main
        main(username)

    if choice == len(files) + 1:
        from cli import main
        main(username)
    else:
        filename = files[choice - 1]

        # Check if that file is exist in download directory
        if os.path.exists(f'downloaded/{filename}'):
            print('Ooopss.. File already exist !!')

        # Write file from server to download directory
        with open(f'downloaded/{filename}', 'wb') as writer:
            data = proxy.download(filename, username).data
            writer.write(data)

        loading(3)
        print('Download berhasil !!')
        loading(4)


def downloads(username):
    file_array = []
    is_finished = False

    # Create downloaded folder if folder not exist
    if not os.path.exists(os.getcwd() + '/downloaded'):
        os.mkdir('../downloaded')

    # Retrieve list of files that available in server storage
    files = str(proxy.show_all_files()).split(',')

    # Select available file to download
    while not is_finished:
        print(f'File yang akan di download adalah : \n {",".join(file_array)}')
        print('Silahkan pilih yang akan di download')
        for i in range(len(files)):
            print(f'{i + 1}. {files[i]}')
        print(f'{len(files) + 1}. Cukup')
        print(f'{len(files) + 2}. Kembali')
        choice = int(input(f'Masukkan pilihan anda (1-{len(files) + 2}) -> '))

        if choice not in range(len(files) + 3):
            print('Pilihan tidak valid !!')
            loading(2)
            from cli import main
            main(username)

        if choice == len(files) + 1:
            is_finished = True
        if choice == len(files) + 2:
            is_finished = True
            from cli import main
            main(username)
            loading(3)
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Downloads(file, username)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)
    finally:
        loading(3)
        print("Operasi Berhasil ....")


def uploads(username):
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
        print(f'{len(files) + 2}. Kembali')
        choice = int(input(f'Masukkan pilihan anda (1-{len(files) + 2}) -> '))

        if choice not in range(len(files) + 3):
            print('Pilihan tidak valid !!')
            loading(2)
            from cli import main
            main(username)

        if choice == len(files) + 1:
            is_finished = True
        if choice == len(files) + 2:
            is_finished = True
            from cli import main
            main(username)
            loading(3)
        if not is_finished:
            file_array.append(files[choice - 1])

    results = []
    try:
        for file in file_array:
            current = Uploads(file, username)
            results.append(current)
            current.start()
        for result in results:
            result.join()
    except Exception as e:
        print(e)
    finally:
        loading(3)
        print("Operasi berhasil ....")


def clients_activity():
    loading(3)
    clients = proxy.clients_activity()
    header = clients[0].keys()
    rows = [x.values() for x in clients]
    is_continued = True
    while is_continued:
        print(tabulate(rows, header))
        continued = str(input("Sudah cukup (yes/no) ?? -> "))
        if continued == "yes":
            is_continued = False
        else:
            continue
    loading(3)

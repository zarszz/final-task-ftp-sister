from processing import upload, uploads, download, downloads, clients_activity

import os


def main(username):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Selamat data di tugas besar sister - FTP')
    print('1. Upload File')
    print('2. Upload File(s)')
    print('3. Download File')
    print('4. Download File(s)')
    print('5. Aktivitas user')
    print('6. Logout')
    print('7. Exit')
    choice = int(input('Masukkan pilihan anda (1-7) -> '))
    if choice == 1:
        upload(username)
        main(username)
    elif choice == 2:
        uploads(username)
        main(username)
    elif choice == 3:
        download(username)
        main(username)
    elif choice == 4:
        downloads(username)
        main(username)
    elif choice == 5:
        clients_activity()
        main(username)
    elif choice == 6:
        import cli
        cli.login_prompt()
        main(username)
    elif choice == 7:
        exit(0)
    else:
        print('Pilihan tidak valid !!')

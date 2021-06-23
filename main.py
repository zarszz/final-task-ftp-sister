import os

from client import upload, uploads, download, downloads
# from getpass import getpass


# def login_prompt():
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print("Silahkan login ke sistem !!")
#     username = str(input("Masukkan username anda -> "))
#     password = getpass()
#     return username, password
# 
# 
# def login():
#     is_repeat = True
#     while is_repeat:
#         username, password = login_prompt()
#         if username == "ucok" and password == "123":
#             main(username)
#         else:
#             print("Opsss.. username/pasword salah !!")
#             is_will_repeat = str(input("Ulangi lagi ? (yes/no) -> "))
#             if is_will_repeat == "yes":
#                 login()
#             else:
#                 is_repeat = False
#                 exit(0)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('1. Upload File')
    print('2. Upload File(s)')
    print('3. Download File')
    print('4. Download File(s)')
    print('6. Exit')
    choice = int(input('Masukkan pilihan anda -> '))
    if choice == 1:
        upload()
    elif choice == 2:
        uploads()
    elif choice == 3:
        download()
    elif choice == 4:
        downloads()
    elif choice == 5:
        exit(0)
    else:
        print('Pilihan tidak valid !!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

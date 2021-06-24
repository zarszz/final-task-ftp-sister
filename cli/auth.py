import os

from processing import login
from getpass import getpass


def login_prompt():
    is_repeat = True
    while is_repeat:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Silahkan login ke sistem !!")
        username = str(input("Masukkan username anda -> "))
        password = getpass()
        is_valid = login(username, password)
        if is_valid:
            from cli import main
            main(username)
        else:
            print("Opsss.. username/pasword salah !!")
            is_will_repeat = str(input("Ulangi lagi ? (yes/no) -> "))
            if is_will_repeat == "yes":
                login_prompt()
            else:
                is_repeat = False
                exit(0)

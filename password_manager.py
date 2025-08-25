import os, json
from cryptography.fernet import Fernet

KEY_FILE = 'key.key'
DATA_FILE = 'passwords.json'

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

def load_key():
    return open(KEY_FILE, 'rb').read()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data).decode()

def save_passwords(passwords, key):
    data = json.dumps(passwords)
    encrypted = encrypt_data(data, key)
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted)

def load_passwords(key):
    if not os.path.exists(DATA_FILE):
        return {}
    encrypted = open(DATA_FILE, 'rb').read()
    data = decrypt_data(encrypted, key)
    return json.loads(data)

def main():
    if not os.path.exists(KEY_FILE):
        generate_key()
    key = load_key()
    passwords = load_passwords(key)

    while True:
        choice = input("1. Add Password\n2. View Passwords\n3. Exit\n> ")
        if choice == '1':
            site = input("Enter site: ")
            pwd = input("Enter password: ")
            passwords[site] = pwd
            save_passwords(passwords, key)
        elif choice == '2':
            for site, pwd in passwords.items():
                print(f"{site}: {pwd}")
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
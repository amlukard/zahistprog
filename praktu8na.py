from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Функція для генерації ключа
def generate_key():
    return Fernet.generate_key()

# Функція для збереження ключа у файл
def save_key_to_file(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

# Функція для завантаження ключа з файлу
def load_key_from_file(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

# Функція для шифрування файлу
def encrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
        encrypted_data = fernet.encrypt(file_data)
    with open(f'encrypted_{filename}', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    print("Файл зашифровано!")

# Функція для дешифрування файлу
def decrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
    with open(f'decrypted_{filename}', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    print("Файл розшифровано!")

# Приклад використання функцій
if __name__ == "__main__":
    file_to_encrypt = 'fileforencrypto.txt'
    key = generate_key()
    save_key_to_file(key, 'key.key')
    
    encrypt_file(file_to_encrypt, key)
    
    loaded_key = load_key_from_file('key.key')
    decrypt_file(f'encrypted_{file_to_encrypt}', loaded_key)

# Функція для генерації пари відкритий-закритий ключ
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Функція для збереження ключа у файл
def save_key_to_file(key, filename):
    with open(filename, 'wb') as key_file:
        serialized_key = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        key_file.write(serialized_key)

# Функція для завантаження ключа з файлу
def load_key_from_file(filename):
    with open(filename, 'rb') as key_file:
        key_data = key_file.read()
        return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())

# Функція для шифрування файлу за допомогою публічного ключа
def encrypt_file(filename, public_key):
    with open(filename, 'rb') as file:
        file_data = file.read()
        encrypted_data = public_key.encrypt(
            file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    with open(f'encrypted_{filename}', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    print("Файл зашифровано!")

# Функція для дешифрування файлу за допомогою приватного ключа
def decrypt_file(filename, private_key):
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    with open(f'decrypted_{filename}', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    print("Файл розшифровано!")

# Приклад використання функцій
if __name__ == "__main__":
    file_to_encrypt = 'fileforencrypto.txt'
    private_key, public_key = generate_key_pair()
    save_key_to_file(private_key, 'private_key.pem')
    
    encrypt_file(file_to_encrypt, public_key)
    
    loaded_private_key = load_key_from_file('private_key.pem')
    decrypt_file(f'encrypted_{file_to_encrypt}', loaded_private_key)

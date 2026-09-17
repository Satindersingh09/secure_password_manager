from cryptography.fernet import Fernet

from config import ENCRYPTION_KEY


cipher = Fernet(ENCRYPTION_KEY)


def encrypt_password(password):

    encrypted = cipher.encrypt(
        password.encode()
    )

    return encrypted.decode()


def decrypt_password(password):

    decrypted = cipher.decrypt(
        password.encode()
    )

    return decrypted.decode()
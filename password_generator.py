import random
import string

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%"
    password = ""
    for i in range(length):
        password += random.choice(characters)
    return password
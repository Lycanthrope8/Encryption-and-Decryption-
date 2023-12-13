from cryptography.fernet import Fernet
import random

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1 or n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        if candidate % 2 != 0 and is_prime(candidate):
            return candidate
        
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def find_coprime(phi_n):
    e = 11  # Starting with 11
    while True:
        if 1 < e < phi_n and gcd(e, phi_n) == 1:
            return e
        e += 2  # Incrementing by 2 so that it stays odd

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return print("Modular inverse does not exist")
    else:
        return x % m

p = generate_large_prime(128)
q = generate_large_prime(128)

n = p * q
phi_n = (p - 1) * (q - 1)
e = find_coprime(phi_n)
d = mod_inverse(e, phi_n)

# print('p:',p)
# print('q:',q)   
# print('n:',n)
# print('phi_n:',phi_n)
# print('e:',e)
# print('d:',d)

def encrypt_rsa(m, e, n):
    return pow(m, e, n)

def decrypt_rsa(c, d, n):
    return pow(c, d, n)


def generate_encryption_key():
    return Fernet.generate_key()

def encrypt_with_fernet_and_rsa(path, encryption_key, e, n):
    cipher = Fernet(encryption_key)
    with open(path, "rb") as file:
        data = file.read()
        m = int(data.hex(), 16)
        print('m:',m)
        ciphertext_rsa = encrypt_rsa(m, e, n)
        print('ciphertext_rsa: ',ciphertext_rsa)
        encrypted_data = cipher.encrypt(ciphertext_rsa.to_bytes((ciphertext_rsa.bit_length() + 7) // 8, 'big'))

    with open(path + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_with_fernet_and_rsa(path, encryption_key, d, n):
    cipher = Fernet(encryption_key)
    with open(path + ".enc", "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        ciphertext_rsa = int.from_bytes(decrypted_data, 'big')
        decrypted_message = decrypt_rsa(ciphertext_rsa, d, n)
        print('decrypted_message:',decrypted_message)
    with open(path + ".dec", "wb") as decrypted_file:
        decrypted_file.write(decrypted_message.to_bytes((decrypted_message.bit_length() + 7) // 8, 'big'))

encryption_key = generate_encryption_key()
filePath = "secret.txt"
encrypt_with_fernet_and_rsa(filePath, encryption_key, e, n)
decrypted_message = decrypt_with_fernet_and_rsa(filePath, encryption_key, d, n)

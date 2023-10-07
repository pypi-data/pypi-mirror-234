from cryptography.fernet import Fernet
key = Fernet.generate_key().decode()
print(key)

f = Fernet(key)
crypt_user = f.encrypt('projeto'.encode())
crypt_pass = f.encrypt('mysecretpassword'.encode())

print(f"crypt_user: {crypt_user.decode()}")
print(f"crypt_pass: {crypt_pass.decode()}")

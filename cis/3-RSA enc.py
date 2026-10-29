from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# 1. Generate RSA key pair (2048-bit key size is standard and secure)
private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048
)
public_key = private_key.public_key()

# 2. Encrypt data using the public key
message = b"Hello TYBCS class, Welcome to the RSA Practical"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
print(f"Ciphertext (bytes): {ciphertext.hex()[:60]}...")

# 3. Decrypt data using the private key
decrypted_message = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

print("Decrypted message:", decrypted_message.decode())
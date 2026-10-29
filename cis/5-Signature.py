import hashlib
import hmac

# Function to create SHA-256 hash of message
def create_hash(message):
    hash_value = hashlib.sha256(message.encode()).hexdigest()
    return hash_value


# Function to convert hash into small integer for demo RSA
def hash_to_integer(message, n):
    hash_hex = create_hash(message)
    hash_int = int(hash_hex, 16)

    # Reduce hash value so it fits inside RSA modulus n
    return hash_int % n


# Function to generate digital signature
def generate_signature(message, private_key, n):
    message_hash = hash_to_integer(message, n)

    # Signature = hash^d mod n
    signature = pow(message_hash, private_key, n)

    return signature


# Function to verify digital signature
def verify_signature(message, signature, public_key, n):
    message_hash = hash_to_integer(message, n)

    # Decrypted signature = signature^e mod n
    verified_hash = pow(signature, public_key, n)

    # Secure comparison using hmac.compare_digest()
    if hmac.compare_digest(str(message_hash), str(verified_hash)):
        return True
    else:
        return False
    # Main Program

# RSA values for demonstration
p = 61  # phi of 61 is 60
q = 53  # phi of 53 is 52

n = p * q  # n = 3233
phi = (p - 1) * (q - 1)  # phi = 3120

# Public key
e = 17  # RSA uses phi to calculate the private key (d)
# To find d: (d x 17) mod 3120 = 1 [(d x e) mod phi = 1]
# The answer is d = 2753

# Private key
d = 2753

print("Public Key :", e, n)
print("Private Key :", d, n)

message = input("Enter the message: ")

signature = generate_signature(message, d, n)

print("\nDigital Signature:")
print(signature)

print("\n----- Signature Verification -----")

received_message = input("Enter received message: ")
received_signature = int(input("Enter received signature: "))

if verify_signature(received_message, received_signature, e, n):
    print("Signature Verified Successfully.")
    print("Message integrity and authenticity are confirmed.")
else:
    print("Signature Verification Failed.")
    print("Message may be modified or signature is invalid.")
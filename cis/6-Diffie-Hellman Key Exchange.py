# Diffie-Hellman Key Exchange

# Public values
p = 23  # Prime number
g = 5   # Primitive root, g power1 mod p = 5

# Alice's private key
a = 8

# Bob's private key
b = 15

# Public keys
A = (g**a) % p  # Alice computes and sends A to Bob
B = (g**b) % p  # Bob computes and sends B to Alice

print("Alice Public Key:", A)
print("Bob Public Key:", B)

# Shared secret keys
alice_secret = (B**a) % p
bob_secret = (A**b) % p

print("Alice Secret Key:", alice_secret)
print("Bob Secret Key:", bob_secret)

if alice_secret == bob_secret:
    print("Key Exchange Successful!")
    print("Shared Secret Key =", alice_secret)
else:
    print("Key Exchange Failed!")
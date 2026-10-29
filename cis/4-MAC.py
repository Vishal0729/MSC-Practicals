import hmac
import hashlib

# Function to generate MAC
def generate_mac(message, secret_key):
    mac = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256)
    return mac.hexdigest()


# Function to verify MAC
def verify_mac(message, secret_key, received_mac):
    generated_mac = generate_mac(message, secret_key)

    # Secure comparison
    if hmac.compare_digest(generated_mac, received_mac):
        return True
    else:
        return False


# Main program
message = input("Enter the message: ")
secret_key = input("Enter the secret key: ")

# Generate MAC
mac_value = generate_mac(message, secret_key)

print("\nGenerated MAC:")
print(mac_value)

# Verification
print("\n--- MAC Verification ---")
received_message = input("Enter received message: ")
received_key = input("Enter received key: ")
received_mac = input("Enter received MAC: ")

if verify_mac(received_message, received_key, received_mac):
    print("MAC Verified Successfully.")
    print("Message integrity and authenticity are confirmed.")
else:
    print("MAC Verification Failed.")
    print("Message may be modified or secret key is incorrect.")
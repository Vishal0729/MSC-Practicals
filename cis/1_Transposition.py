def encrypt(text):
    even = ""
    odd = ""

    for i in range(len(text)):
        if i % 2 == 0:
            even += text[i]
        else:
            odd += text[i]

    return even + odd


def decrypt(cipher):
    n = len(cipher)
    even_len = (n + 1) // 2

    even = cipher[:even_len]
    odd = cipher[even_len:]

    result = ""
    e = 0
    o = 0

    for i in range(n):
        if i % 2 == 0:
            result += even[e]
            e += 1
        else:
            result += odd[o]
            o += 1

    return result


text = input("Enter Plain Text: ")
cipher = encrypt(text)
print("Encrypted Text:", cipher)

plain = decrypt(cipher)
print("Decrypted Text:", plain)
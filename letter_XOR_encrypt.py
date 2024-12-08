def xor_encrypt(message, key):
    #  One liner, needs breakdown for actually understanding
    # return ''.join(chr(ord(c) ^ ord(key)) for c in message)

    # dummy arr
    lame_arr = []
    # loop for going over each letter in the message
    for letter in message:
        # bitwise comparison between a given letter and the key letter
        compared_bit_result = (ord(letter) ^ ord(key))
        # convert the resultant bits back into a character
        new_char = chr(compared_bit_result)
        # append it to the dummy arr
        lame_arr.append(new_char)
    # put together the new characters into a finished string
    return ('').join(lame_arr)


def xor_decrypt(encrypted, key):
    return ''.join(chr(ord(c) ^ ord(key)) for c in encrypted)

with open("myPlaintextMessage.txt", "r", encoding="UTF-8") as file:
    # Read the entire file content as a string
    message = file.read() 

# keyword used for XOR encryption; can be any char
key = "a"

encrypted = xor_encrypt(message, key)

decrypted = xor_decrypt(encrypted, key)


print(f"Original: {message}")

print(f"Encrypted: {encrypted}")

print(f"Decrypted: {decrypted}")

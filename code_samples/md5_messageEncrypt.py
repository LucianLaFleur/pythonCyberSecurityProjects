import hashlib

def generate_md5_hash(key_phrase):
    # Create an md5 hash object
    md5 = hashlib.md5()
    # Update the hash object with the bytes of the key phrase
    md5.update(key_phrase.encode('utf-8'))
    # Return the hexadecimal digest of the hash
    return md5.hexdigest()

#Shorter versions saved for berevity

# def xor_encrypt(message, key_phrase):
#     key_hash = generate_md5_hash(key_phrase)
#     key_bytes = bytes.fromhex(key_hash)
#     return ''.join(chr(ord(c) ^ key_bytes[i % len(key_bytes)]) for i, c in enumerate(message))

# def xor_decrypt(encrypted, key_phrase):
#     key_hash = generate_md5_hash(key_phrase)
#     key_bytes = bytes.fromhex(key_hash)
#     return ''.join(chr(ord(c) ^ key_bytes[i % len(key_bytes)]) for i, c in enumerate(encrypted))

# Longer version made for clarity 

def xor_encrypt(message, key_phrase):
    # Generate the MD5 hash of the key phrase
    key_hash = generate_md5_hash(key_phrase)
    # Convert the hash to bytes
    key_bytes = bytes.fromhex(key_hash)
    # Initialize an empty list to store the encrypted characters
    encrypted_chars = []
    # Loop through each character in the message along with its index
    for i, c in enumerate(message):
        # Get the corresponding byte from the key (cyclically)
        key_byte = key_bytes[i % len(key_bytes)]
        # XOR the character with the key byte and convert to a new character
        encrypted_char = chr(ord(c) ^ key_byte)
        # Append the encrypted character to the list
        encrypted_chars.append(encrypted_char)
    # Join the list of encrypted characters into a single string
    encrypted_message = ''.join(encrypted_chars)
    return encrypted_message

def xor_decrypt(encrypted, key_phrase):
    # Generate the MD5 hash of the key phrase
    key_hash = generate_md5_hash(key_phrase)
    # Convert the hash to bytes
    key_bytes = bytes.fromhex(key_hash)
    # Initialize an empty list to store the decrypted characters
    decrypted_chars = []
    # Loop through each character in the encrypted message along with its index
    for i, c in enumerate(encrypted):
        # Get the corresponding byte from the key (cyclically)
        key_byte = key_bytes[i % len(key_bytes)]
        # XOR the character with the key byte and convert to a new character
        decrypted_char = chr(ord(c) ^ key_byte)
        # Append the decrypted character to the list
        decrypted_chars.append(decrypted_char)
    # Join the list of decrypted characters into a single string
    decrypted_message = ''.join(decrypted_chars)
    return decrypted_message

with open("myPlaintextMessage.txt", "r", encoding="UTF-8") as file:
    # Read the entire file content as a string
    message = file.read() 

raw_key_phrase = "creative sentence to be hashed"

md5_key = generate_md5_hash(raw_key_phrase)

encrypted = xor_encrypt(message, md5_key)

decrypted = xor_decrypt(encrypted, md5_key)

print(f"Original: {message}")

print(f"Encrypted: {encrypted}")

print(f"Decrypted: {decrypted}")

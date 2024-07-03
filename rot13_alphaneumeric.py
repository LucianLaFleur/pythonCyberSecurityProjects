def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Determine the ASCII offset (65 for uppercase, 97 for lowercase)
            ascii_offset = 65 if char.isupper() else 97
            # Shift the character and wrap around the alphabet
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += shifted_char
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    return result

# Example usage
message = "Hello, World! 123"
shift_amount = 13

encrypted = caesar_cipher(message, shift_amount)
decrypted = caesar_cipher(encrypted, -shift_amount)

print(f"Original: {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
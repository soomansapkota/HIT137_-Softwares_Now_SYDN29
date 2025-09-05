# Assignment 2

# Simple file encryptor/decryptor with custom shifting rules.

# Rules:
# - Lowercase:
#   * a–m: shift forward by (key1 * key2)
#   * n–z: shift backward by (key1 + key2)

# - Uppercase:
#   * A–M: shift backward by key1
#   * N–Z: shift forward by (key2 ** 2)
#
# - Any other characters (digits, spaces, punctuation, tabs, newlines)
#   remain unchanged.

# Program Steps:
# 1. Ask the user for two integer keys (key1, key2)
# 2. Encrypt the content of raw_text.txt → encrypted_text.txt
# 3. Decrypt encrypted_text.txt → decrypted_text.txt
# 4. Check whether the decrypted file matches the original


# Core helper
def rotate_half(ch, start, amount):
    """Rotate a character within its 13-letter half by a given amount."""
    return chr((ord(ch) - ord(start) + (amount % 13)) % 13 + ord(start))

# Character encryption
def encrypt_char(ch, key1, key2):
    """Encrypt a single character based on the rules."""
    if "a" <= ch <= "m":
        return rotate_half(ch, "a", key1 * key2)
    elif "n" <= ch <= "z":
        return rotate_half(ch, "n", -(key1 + key2))
    elif "A" <= ch <= "M":
        return rotate_half(ch, "A", -key1)
    elif "N" <= ch <= "Z":
        return rotate_half(ch, "N", key2 ** 2)
    else:
        return ch


def decrypt_char(ch, key1, key2):
    """Decrypt a single character (inverse of encrypt_char)."""
    if "a" <= ch <= "m":
        return rotate_half(ch, "a", -(key1 * key2))
    elif "n" <= ch <= "z":
        return rotate_half(ch, "n", (key1 + key2))
    elif "A" <= ch <= "M":
        return rotate_half(ch, "A", key1)
    elif "N" <= ch <= "Z":
        return rotate_half(ch, "N", -(key2 ** 2))
    else:
        return ch


# Recursive text processing
def encrypt_text_recursive(text, idx, key1, key2):
    """Recursively encrypt text from a given index."""
    if idx >= len(text):
        return ""
    return encrypt_char(text[idx], key1, key2) + encrypt_text_recursive(text, idx + 1, key1, key2)


def decrypt_text_recursive(text, idx, key1, key2):
    """Recursively decrypt text from a given index."""
    if idx >= len(text):
        return ""
    return decrypt_char(text[idx], key1, key2) + decrypt_text_recursive(text, idx + 1, key1, key2)


#File Operations
def read_file(path):
    """Read file content safely with error handling."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        if path == "raw_text.txt":
            print("raw_text.txt is missing. Please create it first.")
        raise
    except Exception as e:
        print("Could not read file:", e)
        raise


def write_file(path, content):
    """Write text to a file safely."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print("Could not write file:", e)
        raise


#Encrypt and decrypt functions
def encrypt_file(key1, key2):
    original_text = read_file("raw_text.txt")
    encrypted_text = encrypt_text_recursive(original_text, 0, key1, key2)
    write_file("encrypted_text.txt", encrypted_text)
    print("raw_text.txt has been encrypted into encrypted_text.txt")


def decrypt_file(key1, key2):
    encrypted_text = read_file("encrypted_text.txt")
    decrypted_text = decrypt_text_recursive(encrypted_text, 0, key1, key2)
    write_file("decrypted_text.txt", decrypted_text)
    print("encrypted_text.txt has been decrypted into decrypted_text.txt")


def verify_files():
    """Check if decrypted_text.txt matches raw_text.txt."""
    try:
        original = read_file("raw_text.txt")
        decrypted = read_file("decrypted_text.txt")
    except Exception:
        return
    if original == decrypted:
        print("Decryption successful: the files match!")
    else:
        print("Decryption failed: the files are different.")


# Input handling
def get_int(prompt):
    """Ask user for an integer, retry until valid."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("That was not a valid number. Try again.")
        return get_int(prompt)  # recursion for retry


# Main Function
def main():
    print("Text Encrypt/Decrypt")
    key1 = get_int("Enter key1 (integer): ")
    key2 = get_int("Enter key2 (integer): ")

    try:
        encrypt_file(key1, key2)
        decrypt_file(key1, key2)
        verify_files()
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()


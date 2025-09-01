# assignment2.py
# Character shifting functions
def shift_lowercase(ch: str, shift: int) -> str:
    base = ord('a')
    return chr((ord(ch) - base + shift) % 26 + base)

def shift_uppercase(ch: str, shift: int) -> str:
    base = ord('A')
    return chr((ord(ch) - base + shift) % 26 + base)

#Rotate within 13 characters
def _shift_in_half(ch: str, start: str, k: int) -> str:
    return chr((ord(ch) - ord(start) + (k % 13)) % 13 + ord(start))

# Per-character encoding
def encode_char(ch: str, shift1: int, shift2: int) -> str:
    """Apply encryption rule to one character (keeps letters within their half)."""
    if 'a' <= ch <= 'm':                          # a–m: forward by shift1*shift2
        return _shift_in_half(ch, 'a', shift1 * shift2)
    elif 'n' <= ch <= 'z':                        # n–z: backward by shift1+shift2
        return _shift_in_half(ch, 'n', -(shift1 + shift2))
    elif 'A' <= ch <= 'M':                        # A–M: backward by shift1
        return _shift_in_half(ch, 'A', -shift1)
    elif 'N' <= ch <= 'Z':                        # N–Z: forward by shift2**2
        return _shift_in_half(ch, 'N', (shift2 ** 2))
    else:
        return ch  

# Decoding
def decode_char(ch: str, shift1: int, shift2: int) -> str:
    """Exact inverse of encode_char (half-preserving rotations)."""
    if 'a' <= ch <= 'm':                          # undo a–m forward
        return _shift_in_half(ch, 'a', -(shift1 * shift2))
    elif 'n' <= ch <= 'z':                        # undo n–z backward
        return _shift_in_half(ch, 'n', (shift1 + shift2))
    elif 'A' <= ch <= 'M':                        # undo A–M backward
        return _shift_in_half(ch, 'A', shift1)
    elif 'N' <= ch <= 'Z':                        # undo N–Z forward
        return _shift_in_half(ch, 'N', -(shift2 ** 2))
    else:
        return ch  


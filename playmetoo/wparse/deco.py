#-*- coding: utf-8 -*-
# deco.py  (c)2020  Henrique Moreira

"""
Code and Decoder (Base64), wrapper.
"""

# pylint: disable=unused-argument, missing-function-docstring

import base64

# https://tools.ietf.org/html/rfc4648#section-4 -- Base 64 Encoding (alphabet)
BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# referred to as 'base64url' in section 5 of RFC-4648, is as follow:
BASE64URL_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+_"


def main():
    """ Main script """
    assert check_samples()


def check_samples() -> bool:
    samples = (
        "HCM",
        "Henrique Moreira",
        )
    for word in samples:
        outstr = to_base64(word)
        print(f"Encoded {word} to: {outstr}, string='{outstr.decode('ascii')}'")
        if not check_words(word):
            return False
    what = bytes()
    word = "hm"
    s_hex = f"0x{ord(word[0]):02x}{ord(word[1]):02x}"	# s_hex = '0x686d'
    is_ok = what.fromhex(s_hex[2:]) == bytes(word, "ascii")
    assert is_ok
    # If padding is incorrect, you can enforce this check using 'check_pad=True', e.g.:
    #	from_base64(base64.b64encode(b'Ah').decode("ascii").rstrip('='), check_pad=True)
    return True


def check_words(word) -> bool:
    what = base64.b64encode(bytes(word, "ascii"))
    msg = base64.b64decode(what).decode("ascii")
    is_ok = word == msg
    shown = "" if is_ok else " -- FAILED"
    print(f"Encoded: {what}, decoded as '{msg}'{shown}")
    return is_ok


def to_base64(astr) -> str:
    """ Main encoding function of this module; basically a wrapper to base64.b64encode() ! """
    s_ascii = "ascii"
    if isinstance(astr, str):
        what = bytes(astr, s_ascii)
    elif isinstance(astr, bytes):
        what = astr
    elif isinstance(astr, (tuple, list)):
        res = []
        for name in astr:
            res.append(to_base64(name))
        return res
    else:
        return None
    return base64.b64encode(what)

def from_base64(astr, s_ascii="ascii", check_pad=False) -> str:
    """ Main decoding function of this module; basically a wrapper to base64.b64deode() ! """
    if isinstance(astr, bytes):
        encc = astr.decode("ascii")
    elif isinstance(astr, str):
        encc = astr
    else:
        return ""
    safe_str = encc.rstrip("=")
    for ach in safe_str:
        if ach not in BASE64_ALPHABET:
            return ""
    if check_pad:
        safe_str = astr
    else:
        safe_str += "==="
    bstr = base64.b64decode(safe_str)
    #	binascii.Error: Incorrect padding ...if padding ('=') is insufficient!
    assert isinstance(bstr, bytes)
    res = bstr.decode(s_ascii)
    return res


# Main script
if __name__ == "__main__":
    # import importlib; importlib.reload(wparse.deco); from wparse.deco import *
    main()

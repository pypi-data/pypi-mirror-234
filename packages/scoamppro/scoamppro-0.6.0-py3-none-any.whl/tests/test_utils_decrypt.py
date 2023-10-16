import unittest
import random
import string
import binascii

import pytest

from scoamp.utils.decrypt import (encrypt_aes256gcm, decrypt_aes256gcm)

class TestDecrypt(unittest.TestCase):
    def test_decrypt(self):
        data = 'hello scoamp'
        iv = b'1' * 12

        # 32-bit raw key
        key = ''.join(random.choices(string.ascii_letters, k=32))
        enc_data = encrypt_aes256gcm(key, data, iv)
        dec_data = decrypt_aes256gcm(key, enc_data)
        self.assertEqual(dec_data, data)

        # 64-bit hex encode key
        key = ''.join(random.choices(string.hexdigits, k=64))
        enc_data = encrypt_aes256gcm(key, data, iv)
        dec_data = decrypt_aes256gcm(key, enc_data)
        self.assertEqual(dec_data, data)

        # invalid key: non hexadecimal char
        key = ''.join(random.choices(string.punctuation, k=64))
        with pytest.raises(
            binascii.Error,
            match=r'Non-hexadecimal digit found'
        ):
            enc_data = encrypt_aes256gcm(key, data, iv)
            dec_data = decrypt_aes256gcm(key, enc_data)
            self.assertEqual(dec_data, data)

        # invalid key: invalid length
        key = ''.join(random.choices(string.hexdigits, k=63))
        with pytest.raises(
            ValueError,
            match=r'invalid key'
        ):
            enc_data = encrypt_aes256gcm(key, data, iv)
            dec_data = decrypt_aes256gcm(key, enc_data)
            self.assertEqual(dec_data, data)
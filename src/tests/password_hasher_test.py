from typing import Union
import unittest
from ..password_hasher import Argon2PasswordHasher, GenerateSalt


class TestArgon2Hasher(unittest.TestCase):

    def test_create_password_hash(self):
        result: Union[str, Exception] = Argon2PasswordHasher().hash_password('ola', 'ola')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        verify_password_result = Argon2PasswordHasher().verify_password('ola', 'ola', result)
        self.assertIsNotNone(verify_password_result)
        self.assertIsInstance(verify_password_result, bool)

class TestGenerateSalt(unittest.TestCase):
    def test_generate_salt(self):
        result: str = GenerateSalt(9)
        self.assertIsNotNone(result.salt)
        self.assertIsInstance(result.salt, str)
        result_encoded = result.encode()
        self.assertIsNotNone(result_encoded)
        self.assertIsInstance(result_encoded, bytes)


if __name__ == '__main__':
    unittest.main()

import unittest
from . import password_hasher_test

def run() -> None:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(password_hasher_test)
    unittest.TextTestRunner(verbosity=2).run(suite)

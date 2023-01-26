"""The collections of the tests for protection module."""
from cryptography.fernet import Fernet

from tools.protection import Protection


def test_encrypt_data(mocker):
    """Check the data is encrypted correctly.

    Args:
        mocker (pytest_mock): mock called methods
    """
    excepted_result = 'gAAAAABj0YLPHaoW=='
    mocker.patch.object(Fernet, 'encrypt', return_value=bytes(excepted_result, 'utf-8'))
    protection = Protection('pass word')

    result = protection.encrypt(' data to encrypt')

    assert result == excepted_result
    Fernet.encrypt.assert_called_once()


def test_decrypt_data(mocker):
    """Check the encrypted data is decrypted correctly.

    Args:
        mocker (pytest_mock): mock called methods
    """
    excepted_result = 'decrypted data '
    mocker.patch.object(Fernet, 'decrypt', return_value=bytes(excepted_result, 'utf-8'))
    protection = Protection('Password!@#12 ')

    result = protection.decrypt('gAAAAABj0YLPHaoW==')

    assert result == excepted_result
    Fernet.decrypt.assert_called_once()

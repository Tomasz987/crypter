"""The collections of the tests for the crypter.py module"""
import builtins
import os

from tools.crypter import Crypter
from tools.file_management import File
from tools.protection import Protection


class SideEffect:
    """Implemented to call to the different function in any call when use side_effect attribute"""
    def __init__(self, *functions: callable):
        """Construct all the necessary attributes for the sideeffect object

        Args:
            *functions (callable): functions that are returned after any call
        """
        self.functions = iter(functions)

    def __call__(self, *args, **kwargs):
        """After any call return next function"""
        function = next(self.functions)
        return function(*args, **kwargs)


def test_encrypt_file(mocker):
    """Check that the data from the unencrypted file is encrypted and saved correctly"""
    example_file_path = 'example_folder/file.txt'
    fake_encrypted_data = 'gAABj0YLPHaoW=='
    example_read_data = ' data1@./? '
    crypter = Crypter('password')

    open_mock = mocker.mock_open(read_data=example_read_data)
    mocker.patch.object(builtins, 'open', new=open_mock)
    mocker.patch.object(Protection, 'encrypt', return_value=fake_encrypted_data)
    mocker.patch.object(File, 'save')

    crypter.encrypt(example_file_path)

    builtins.open.assert_called_once_with(example_file_path, 'r', encoding='utf-8')
    Protection.encrypt.assert_called_once_with(example_read_data)
    File.save.assert_called_once_with(fake_encrypted_data)


def test_file_extension_after_encrypt(mocker):
    """Check that the extension file is changed to '.cr' after encrypt"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password')

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'encrypt')

    crypter.encrypt(example_file_path)

    assert crypter.file_path == example_file_path + '.cr'


def test_file_extension_after_decrypt(mocker):
    """Check that the '.cr' extension is removed after decrypt"""
    example_file_path = 'example_folder/file.txt.cr'
    crypter = Crypter('password')

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'decrypt')

    crypter.decrypt(example_file_path)

    assert crypter.file_path == example_file_path[:-3]


def test_append_new_data_to_encrypted_file(mocker):
    """Check that the data from the encrypted file is decrypted,
    append new data, encrypt again and save to the encrypted file"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('pAss12@;!')

    encrypted_file_open_mock = mocker.mock_open(read_data='gAABPHaoW==')
    unencrypted_file_open_mock = mocker.mock_open(read_data='some text')
    open_mock = mocker.mock_open()
    mocker.patch.object(builtins, 'open', side_effect=SideEffect(
        encrypted_file_open_mock,
        unencrypted_file_open_mock,
        open_mock,
    ))
    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(Protection, 'decrypt', return_value='decrypted data')

    crypter.append(example_encrypted_file, example_unencrypted_file)

    assert builtins.open.call_count == 3
    Protection.decrypt.assert_called_once_with('gAABPHaoW==')
    Protection.encrypt.assert_called_once_with('decrypted data' + 'some text')


def test_parent_file_has_been_removed_after_encrypt(mocker):
    """Check that the parent file is removed after encrypting
    when the remove option is chosen"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=True)

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(os, 'remove')

    crypter.encrypt(example_file_path)

    os.remove.assert_called_once_with(example_file_path)


def test_parent_file_has_been_removed_after_decrypt(mocker):
    """Check that the parent file is removed after decrypting
    when the remove option is chosen"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=True)

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(os, 'remove')

    crypter.decrypt(example_file_path)

    os.remove.assert_called_once_with(example_file_path)


def test_parent_file_has_been_removed_after_append(mocker):
    """Check that the unencrypted file is removed after append new data
    when the remove option is chosen"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('password', remove_parent_file=True)

    open_mock = mocker.mock_open()
    mocker.patch.object(builtins, 'open', new=open_mock)
    mocker.patch.object(os, 'remove')
    mocker.patch.object(File, 'load', return_data='some text')
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(Protection, 'encrypt')
    crypter.append(example_encrypted_file, example_unencrypted_file)

    os.remove.assert_called_once_with(example_unencrypted_file)


def test_parent_file_has_not_been_removed_after_encrypt(mocker):
    """Check that the parent file isn't removed after encrypting
    when the remove option is chosen as False"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=False)

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'encrypt')
    mocker.patch.object(os, 'remove')

    crypter.encrypt(example_file_path)

    os.remove.assert_not_called()


def test_parent_file_has_not_been_removed_after_decrypt(mocker):
    """Check that the parent file isn't removed after decrypting
    when the remove option is chosen as False"""
    example_file_path = 'example_folder/file.txt'
    crypter = Crypter('password', remove_parent_file=False)

    mocker.patch.object(builtins, 'open')
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(os, 'remove')

    crypter.decrypt(example_file_path)

    os.remove.assert_not_called()


def test_parent_file_has_not_been_removed_after_append(mocker):
    """Check that the unencrypted file isn't removed after append new data
    when the remove option is chosen as False"""
    example_encrypted_file = 'encrypted.txt.cr'
    example_unencrypted_file = 'unencrypted.txt'
    crypter = Crypter('password', remove_parent_file=False)

    open_mock = mocker.mock_open()
    mocker.patch.object(builtins, 'open', new=open_mock)
    mocker.patch.object(os, 'remove')
    mocker.patch.object(File, 'load', return_data='some text')
    mocker.patch.object(Protection, 'decrypt')
    mocker.patch.object(Protection, 'encrypt')
    crypter.append(example_encrypted_file, example_unencrypted_file)

    os.remove.assert_not_called()
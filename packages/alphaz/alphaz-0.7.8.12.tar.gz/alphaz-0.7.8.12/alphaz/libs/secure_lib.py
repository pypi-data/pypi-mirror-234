import secrets
from html import entities
from bcrypt import hashpw, gensalt, checkpw
from random import randint

from base64 import (
    b64decode,
    b64encode,
    urlsafe_b64encode as b64e,
    urlsafe_b64decode as b64d,
)

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def secure_password(password: str) -> str:
    """
    Hash the given password using the bcrypt algorithm.

    Args:
        password: The password to be hashed.

    Returns:
        The hashed password as a string.
    """
    password_hashed = hashpw(password.encode("utf-8"), gensalt())
    return password_hashed.decode("utf-8")


def compare_passwords(password: str | None, hash_saved: str) -> bool:
    """
    Compare a password to a saved hash to see if they match.

    Args:
        password: The password to compare.
        hash_saved: The saved hash to compare the password to.

    Returns:
        True if the password matches the saved hash, False otherwise.
    """
    try:
        valid = checkpw(str(password).encode("utf-8"), str(hash_saved).encode("utf-8"))
    except ValueError:
        valid = False
    return valid


def get_token() -> str:
    """
    Generate a URL-safe token.

    Returns:
        A URL-safe token as a string.
    """
    return secrets.token_urlsafe(45)


def get_keys_numbers(key: str) -> list[str]:
    """
    Get a list of the numbers that make up the sum of the ASCII values of the characters in the given key.

    Args:
        key: The key to process.

    Returns:
        A list of integers representing the sum of the ASCII values of the characters in the key.
    """
    key_numbers = [ord(x) for x in key]
    keys_numbers = [x for x in str(sum(key_numbers))[:3]]
    return keys_numbers


def get_cry_operation_code(key: str) -> str:
    """
    Generate a cry operation code.

    The code is generated using the key provided and a random sequence of numbers.

    Args:
        key: A string representing the key to use for generating the cry operation code.

    Returns:
        A string representing the cry operation code.
    """
    keys_numbers = get_keys_numbers(key)

    values: list[str] = []
    for _ in range(5):
        value = "".join([str(randint(100, 999)) + x for x in keys_numbers])
        complement = "".join([str(9 - int(x)) for x in value[3:]])
        values.append(value + complement)

    return "-".join(values)


def check_cry_operation_code(code: str, key: str) -> bool:
    """
    Check if a cry operation code is valid.

    A cry operation code is valid if it has the correct format and is consistent with the provided key.

    Args:
        code: A string representing the cry operation code to check.
        key: A string representing the key to use for checking the cry operation code.

    Returns:
        A boolean value indicating whether the cry operation code is valid or not.
    """
    numbers = code.split("-")
    if len(numbers) != 5:
        return False
    try:
        numbers = [int(x) for x in numbers]
    except ValueError:
        return False
    first = numbers[0]
    summed = sum(numbers)
    operation_valid = first - 2 == int(str(summed)[1:])

    keys_numbers = get_keys_numbers(key)
    sequence = [str(numbers[i])[-1] for i in range(3)]

    return operation_valid and keys_numbers == sequence


backend = default_backend()
iterations = 100_000


def _derive_key(password: bytes, salt: bytes, iterations: int = 100_000) -> bytes:
    """
    Derive a secret key from a given password and salt.

    Args:
        password: A byte string representing the password.
        salt: A byte string representing the salt.
        iterations: An integer representing the number of iterations.

    Returns:
        A byte string representing the secret key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(password)


"""def password_encrypt(
    message: str | bytes, password: str, iterations: int = iterations
) -> str:
    if type(message) == str:
        message = message.encode("utf-8")
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b"%b%b%b"
        % (salt, iterations.to_bytes(4, "big"), b64d(Fernet(key).encrypt(message)),)
    ).decode("utf-8")"""


def password_encrypt(
    message: str | bytes, password: str, iterations: int = 100_000
) -> str:
    """
    Encrypt a message with a password.

    Args:
        message: A byte string or a string to be encrypted.
        password: A string representing the password.
        iterations: An integer representing the number of iterations.

    Returns:
        A string representing the encrypted message.
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    f = Fernet(b64encode(key))
    token = f.encrypt(message)
    encoded_token = b64encode(token).decode("utf-8")
    return f"{salt.hex()}:{iterations}:{encoded_token}"


"""def password_decrypt(token: str | bytes, password: str) -> bytes:
    if type(token) == bytes:
        token = token.decode("utf-8")
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, "big")
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token).decode("utf-8")
"""


def password_decrypt(token: str | bytes, password: str) -> bytes:
    """
    Decrypt a message with a password.

    Args:
        token: A byte string or a string representing the encrypted message.
        password: A string representing the password.

    Returns:
        A byte string representing the decrypted message.
    """
    if isinstance(token, str):
        token = token.encode("utf-8")
    salt, iter_str, encoded_token = token.split(b":")
    iterations = int(iter_str)
    key = _derive_key(password.encode(), bytes.fromhex(salt), iterations)
    f = Fernet(key)
    token = b64decode(encoded_token)
    return f.decrypt(token)

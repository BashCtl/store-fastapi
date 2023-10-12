from passlib.context import CryptContext

passwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def hashing_password(password: str):
    return passwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return passwd_context.verify(password, hashed_password)

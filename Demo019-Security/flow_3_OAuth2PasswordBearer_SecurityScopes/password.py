import passlib
import passlib.context
import passlib.hash

from .auth import APP_SECRET_KEY


PASSWORD_CONTEXT: passlib.context.CryptContext = passlib.context.CryptContext(
    schemes=[
        passlib.hash.argon2(rounds=100, salt=APP_SECRET_KEY.encode()),
        passlib.hash.bcrypt,
        passlib.hash.sha512_crypt,
        passlib.hash.sha256_crypt,
        passlib.hash.pbkdf2_sha512,
        passlib.hash.pbkdf2_sha256,
        passlib.hash.bcrypt_sha256,
        passlib.hash.des_crypt,
    ],
    deprecated='auto',
)


async def hash_password(plain_password: str) -> str:
    return PASSWORD_CONTEXT.hash(plain_password)


async def verify_password(plain_password: str, password_hash: str) -> bool:
    return PASSWORD_CONTEXT.verify(plain_password, password_hash)

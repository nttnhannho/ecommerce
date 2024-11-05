import bcrypt

from exceptions.exception import HashBcryptException


class Hash:
    @staticmethod
    async def bcrypt(password):
        try:
            byte = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(byte, salt)
        except Exception:
            raise HashBcryptException

        return hashed_password

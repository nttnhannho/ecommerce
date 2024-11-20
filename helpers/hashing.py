import bcrypt

from exceptions.misc import HashPasswordException, HashCheckMatchedException


class Hash:
    @staticmethod
    async def hash_password(password):
        try:
            byte = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(byte, salt)
        except Exception:
            raise HashPasswordException

        return hashed_password

    @staticmethod
    async def is_password_matched(password, hashed_password):
        try:
            password_bytes = password.encode('utf-8')
            hashed_password_bytes = hashed_password.encode('utf-8')
            is_matched = bcrypt.checkpw(password_bytes, hashed_password_bytes)
        except Exception:
            raise HashCheckMatchedException

        return is_matched

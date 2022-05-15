from passlib.context import CryptContext
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_content.hash(password)

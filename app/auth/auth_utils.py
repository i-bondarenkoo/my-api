import bcrypt

# функции для работы с паролем, библиотека bcrept


# функция для хэширования паролей
def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


# функция для проверки введенного пароля
# с тем , что есть в базе
def verify_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)

from app.auth.auth_utils import hash_password

fake_users = {
    "john": {
        "username": "john",
        "password": hash_password("secret"),
        "email": "john@mail.ru",
        "full_name": "John Smith",
    },
    "alice": {
        "username": "alice",
        "password": hash_password("qwerty"),
        "email": "alice@mail.ru",
        "full_name": "Alice Johnson",
    },
}

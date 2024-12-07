import requests

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_server_is_up():
    try:
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        print("Le serveur est accessible.")
    except requests.exceptions.ConnectionError:
        raise AssertionError("Le serveur n'est pas accessible.")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = "$2b$12$RiRwPDEqvM8FFrMsT/Ahte6c2NQdDHXsbczjMENwQ/ib.htFXgff."
print(pwd_context.verify("lucas", hashed_password))  # Doit afficher True


# url = "http://127.0.0.1:8000/auth/token"
# data = {"username": "nico", "password": "nico"}
# response = requests.post(url, data=data)
# print(response.status_code)
# print(response.json())

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("nico")
print(pwd_context.verify("nico", hashed_password))  # Doit afficher True

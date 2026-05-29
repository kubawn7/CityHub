from data_store import users
from models.user import User
from utils.generator import generate_id


class AuthService:

    @staticmethod
    def register(first_name, last_name, email, password, role):
        user = User(
            generate_id(),
            first_name,
            last_name,
            email,
            password,
            role
        )

        users.append(user)

        print("Użytkownik został zarejestrowany")
        return user

    @staticmethod
    def login(email, password):
        for user in users:
            if user.email == email and user.password == password:
                print("Logowanie zakończone sukcesem")
                return user

        print("Nieprawidłowe dane logowania")
        return None
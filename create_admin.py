from getpass import getpass
from webapp import db, create_app
from webapp.model import db, User

app = create_app()


def create_admin(user_name: str, password: str, email: str) -> None:
    # c какой-то версии алхимия перестала принимать app в create_all() 
    with app.app_context():
        if User.query.filter(User.username == user_name).count():
            print("Пользователь с таким именем существует!")
            return

        new_user = User(username=user_name, role="Admin", email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        print(f"Создан пользователь с ID {new_user.id}")


if __name__ == "__main__":
    username = input("Введите имя: ")
    email = input("Введите почту: ")
    getpass1 = getpass("Введите пароль: ")
    getpass2 = getpass("Повторите ввод пароля: ")
    if getpass1 == getpass2:
        create_admin(username, getpass1, email)
    else:
        print("Пароли не одинаковые! Попробуйте снова")

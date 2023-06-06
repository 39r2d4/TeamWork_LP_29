from getpass import getpass
import sys
from webapp import db, create_app
from webapp.model import db, User



app = create_app()


# c какой-то версии алхимия перестала принимать app в create_all() 
with app.app_context():
    username = input("Введите имя: ")

    if User.query.filter(User.username == username).count():
        print("Пользователь с таким именем существует!")
        sys.exit(0)
    

    getpass1 = getpass("Введите пароль: ")
    getpass2 = getpass("Повторите ввод пароля: ")

    if not getpass1 == getpass2:
        print("Пароли не одинаковые!")
        sys.exit(0)
    
    new_user = User(username = username, role= "Admin")
    new_user.set_password(getpass1)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан пользователь с {new_user.id}")
    
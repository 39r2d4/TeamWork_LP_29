from webapp import db, create_app
from webapp.model import User


app = create_app()

test_user = User(name = "First User")

# c какой-то версии алхимия перестала принимать app в reate_all() 
with app.app_context():
    db.create_all() 
    db.session.add(test_user)
    db.session.commit()


from webapp import db, create_app
#from webapp.model import User


app = create_app()

# c какой-то версии алхимия перестала принимать app в create_all() 
with app.app_context():
    db.create_all() 
    db.session.commit()

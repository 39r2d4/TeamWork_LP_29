from webapp import db, create_app


app = create_app()

# c какой-то версии алхимия перестала принимать app в create_all()
# нужно запускать через with
with app.app_context():
    db.create_all() 
    db.session.commit()

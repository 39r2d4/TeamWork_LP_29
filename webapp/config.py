from webapp.settings import DATABASE_URI

SQLALCHEMY_DATABASE_URI = DATABASE_URI
SECRET_KEY = "this_is_secret_key_you_must_change_it"
OPERATIONALERROR_TEXT = "БД недоступна, повторите попытку позже"
from application import db
from application.models import User
from werkzeug.security import generate_password_hash,check_password_hash


def create_admin():
    admin = User.query.filter_by(is_admin=1).first()
    if admin:
        print("Admin Already Exists")
        return False
    else:
        new_user = User(email="theadmin@gmail.com",password=generate_password_hash("Games587"),is_admin=1)
        db.session.add(new_user)
        db.session.commit()
        print("Admin Created")
        return True

create_admin()
from config import app,db
from controller import *
from model import *


if __name__ == '__main__':
    try:
        db.create_all()
        a1 = Admin(ausername= 'a1',apassword = 'b1')
        u1 = User(username = 'user1' , password = 'password1')
        u2 = User(username='user2', password='password2')
        u3 = User(username = 'user3' , password = 'password3')
        db.session.add(a1)
        db.session.add_all([u1,u2,u3])
        db.session.commit()
    except:
        pass
    app.run(debug=True)
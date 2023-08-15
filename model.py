from config import db

class Admin(db.Model):
    id = db.Column('aid',db.Integer(),primary_key=True)
    ausername = db.Column('ausername',db.String(100),unique=True)
    apassword = db.Column('apassword',db.String(100))

class User(db.Model):
    uid = db.Column('uid',db.Integer(),primary_key=True)
    username = db.Column('username',db.String(100),unique=True)
    password = db.Column('password',db.String(100))
    carrefs = db.relationship('Car' , uselist = True ,lazy = False, backref ='useref')

class Car(db.Model):
    __tablename__ = 'Contact_Info'
    cid = db.Column('cid', db.Integer(), primary_key=True)
    manu = db.Column('manu', db.String(100))
    model = db.Column('model', db.String(100))
    milage = db.Column('milage', db.Integer())
    pdate = db.Column('pdate', db.Date())
    user_id = db.Column('user_id',db.ForeignKey('user.uid' ),unique= False,nullable = True)

if __name__ == '__main__':
    import datetime as dt
    a = "2021-01-01"
    b =dt.datetime.fromisoformat(a).date()
    print(b)
    print(type(b))
    




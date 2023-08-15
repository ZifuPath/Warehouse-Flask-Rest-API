from flask import request,redirect,url_for,flash,jsonify
from config import app,db
from service_impl import CarServiceImpl
from model import Car ,User,Admin
import json
import datetime as dt

from functools import wraps
service = CarServiceImpl()

def user_auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if auth and request.authorization.username and request.authorization.password:
            username = request.authorization.username
            password = request.authorization.password
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    return f(user,*args,**kwargs)
                return jsonify({'Error': 'wrong password'})
            return jsonify({'Error': 'wrong username'})
    return decorated

def admin_auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if auth and request.authorization.username and request.authorization.password:
            username = request.authorization.username
            password = request.authorization.password
            admin = Admin.query.filter_by(ausername=username).first()
            if admin:
                if admin.apassword == password:
                    return f(admin,*args,**kwargs)
                return jsonify({'Error': 'wrong password'})
            return jsonify({'Error': 'wrong username'})
        else:
            return jsonify({'Error': 'NO USERNAME/PASSWORD'})
    return decorated

def serialize(carinfo,uid):
    car = carinfo.__dict__
    car_dict = {'cid': car.get('cid'),
                'manu': car.get('manu'),
                'model': car.get('model'),
                'pdate': str(car.get('pdate')),
                'milage': car.get('milage'),
                'user_id': uid }
    return car_dict

def deserialize(jsondata,uid):
    pdate = jsondata.get('pdate')
    pdate =dt.datetime.fromisoformat(pdate).date()
    car =Car(cid=jsondata.get('cid'),
        manu=jsondata.get('manu'),
        model=jsondata.get('model'),
        milage=jsondata.get('model'),
        pdate=pdate,
             user_id = uid )
    return car


@app.route('/car' ,methods = ['GET'])  #127:0.0.1/car    --- GET
@user_auth_required
def get_all_car(user):
    cars = service.get_all_car()
    car_list = []
    uid= user.uid
    if cars:
        for car in cars:
            car_dict = serialize(car,uid)
            car_list.append(car_dict)
        return json.dumps(car_list)
    return json.dumps({"Error" : "No Data"})


@app.route('/car' ,methods = ['POST'])
@user_auth_required
def add_car(user):
    jsondata = request.get_json()
    uid = user.uid
    if jsondata:
        if jsondata.get('cid') and jsondata.get('manu') and jsondata.get('model') and jsondata.get('milage') and jsondata.get('pdate'):
            cid = jsondata.get('cid')
            if service.get_car(cid):
                return {'Error'  : 'Car already present'}
            else:
                car = deserialize(jsondata,uid)
                service.add_car(car)
                return json.dumps({"succuss" : "Record Inserted Succussfuly"})
        else:
            return json.dumps({"Error " : "Mandatory Fields are not given"})
    return json.dumps({"Error " : "Empty Data Not Allowed"})

@app.route('/car/<int:cid>' ,methods = ['PUT'])  #127:0.0.1/car/1    --- GET
@user_auth_required
def update_car(cid,user):
    car = service.get_car(cid)
    uid = user.uid
    if car:
        jsondata=request.get_json()
        if jsondata:
            if jsondata.get('cid') and jsondata.get('manu') and jsondata.get('model') and jsondata.get('milage') and jsondata.get('pdate'):
                dbcar = deserialize(jsondata,uid)
                service.update_car(dbcar,car)
                return json.dumps({"succuss": "Record Updated Succussfuly"})
            return json.dumps({"error ": "Mandatory Fields are not given"})
        return json.dumps({"Error " : "Empty Data Not Allowed"})
    return json.dumps({"Error"  : f"Car {cid} Not Present"})


@app.route('/car/<int:cid>' ,methods = ['DELETE'])
@user_auth_required
def delete_car(cid,user):
    car = service.get_car(cid)
    if car:
        return json.dumps({"succuss": "Record Deleted Succussfuly"})
    return json.dumps({"Error"  : f"Contact ID {cid} Not Present"})

@app.route('/car/transfer/<int:cid>' ,methods = ['PUT'])
@user_auth_required
def transfer_car(cid,user):
    car = service.get_car(cid)
    if car:
        jsondata=request.get_json()
        uid = jsondata.get('uid')
        if User.query.filter_by(uid= uid).first():
            service.transfer_car(cid,uid)
            return json.dumps({"succuss": "Record transfereed Succussfuly"})
        return json.dumps({"Error": f"user ID {uid} Not Present"})
    return json.dumps({"Error"  : f"Car ID {cid} Not Present"})

@app.route('/user',methods = ['GET'])
@admin_auth_required
def get_all_user(admin):
    users= User.query.all()
    if users:
        user_list = []
        for user in users:
            user = user.__dict__
            cars = user.carrefs
            car_list= []
            for car in cars:
                car_dict = serialize(car)
                car_list.append(car_dict)
            user_dict = {user.uid : car_list}
            user_list.append(user_dict)
        return user_list
    return json.dumps({'Error' : 'No user Present'})

@app.route('/user/<int:uid>',methods = ['GET'])
@admin_auth_required
def get_user(uid,admin):
    user = User.query.filter_by(uid = uid).first()
    if user:
        cars = user.carrefs
        car_list = []
        for car in cars:
            car_dict = serialize(car)
            car_list.append(car_dict)
        user_dict = {user.uid: car_list}
        return json.dumps(user_dict)
    return json.dumps({'Error': 'No user Present'})

@app.route('/user/car/<int:cid>',methods = ['DELETE'])
@admin_auth_required
def delete_car_user(cid,admin):
    car = Car.query.filter_by(cid = cid).first()
    if car:
        car.user_id =None
        db.session.commit()
        return json.dumps({'succuss': 'car deleted from user'})
    return json.dumps({'Error': 'No car Present'})


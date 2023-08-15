from service import CarService
from config import db
from model import Car

class CarServiceImpl(CarService):

    def __init__(self):
        db.create_all()

    def add_car(self,car):
        db.session.add(car)
        db.session.commit()
        return "Record added succussfuly"

    def update_car(self, dbcar, car):
        dbcar.manu = car.manu
        dbcar.milage = car.milage
        dbcar.model = car.model
        dbcar.pdate = car.pdate
        db.session.commit()

    def get_car(self, cid):
        return Car.query.filter_by(cid=cid).first()

    def get_all_car(self):
        return Car.query.all()

    def delete_car(self, cid):
        dbcar = self.get_car(cid)
        print(dbcar)
        if dbcar:
            db.session.delete(dbcar)
            db.session.commit()
            return 'record deleted'
        return "No record with given id"

    def transfer_car(self, cid,uid):
        car = self.get_car(cid)
        if car:
            car.user_id = uid
            db.session.commit()
            return 'record transfer'
        return "No record with given id"


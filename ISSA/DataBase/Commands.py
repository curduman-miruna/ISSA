import logging
from sqlalchemy.exc import SQLAlchemyError
from DataBase.Models import connect, Car, Owner, Renter

def create_owner(owner):
    print("Creating owner")
    try:
        session, engine = connect()
        new_owner = Owner(
            name=owner.name,
            email=owner.email,
            phone=owner.phone,
            password=owner.password
        )
        session.add(new_owner)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        logging.error(f"Failed to create owner: {str(e)}")

def create_renter(renter):
    print("Creating renter")
    try:
        session, engine = connect()
        new_renter = Renter(
            name=renter.name,
            email=renter.email,
            phone=renter.phone,
            password=renter.password,
            car_id=renter.car_id
        )
        session.add(new_renter)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        logging.error(f"Failed to create renter: {str(e)}")

def create_car(car):
    print("Creating car")
    try:
        session, engine = connect()
        new_car = Car(
            brand=car.brand,
            model=car.model,
            year=car.year,
            owner_id=car.owner_id,
            current_renter=car.current_renter,
            available=car.available
        )
        print(car)
        session.add(new_car)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        logging.error(f"Failed to create car: {str(e)}")
    except Exception as e:
        logging.error(f"Failed to create car: {str(e)}")


def login_owner(email, password):
    print("Logging in owner")
    try:
        session, engine = connect()
        owner = session.query(Owner).filter(Owner.email == email, Owner.password == password).first()
        session.close()
        return owner
    except SQLAlchemyError as e:
        logging.error(f"Failed to login owner: {str(e)}")

def login_renter(email, password):
    print("Logging in renter")
    try:
        session, engine = connect()
        renter = session.query(Renter).filter(Renter.email == email, Renter.password == password).first()
        session.close()
        return renter
    except SQLAlchemyError as e:
        logging.error(f"Failed to login renter: {str(e)}")

def get_available_car_ids():
    print("Getting available car IDs")
    try:
        session, engine = connect()
        car_ids = [car.car_id for car in session.query(Car).filter(Car.available == True).all()]
        session.close()
        return car_ids
    except SQLAlchemyError as e:
        logging.error(f"Failed to get available car IDs: {str(e)}")
        return []


def exist_car(car_id):
    print("Checking if car exists")
    try:
        session, engine = connect()
        car = session.query(Car).filter(Car.car_id == car_id).first()
        session.close()
        return car
    except SQLAlchemyError as e:
        logging.error(f"Failed to check if car exists: {str(e)}")

def change_car_availability(car_id, availability):
    print("Changing car availability")
    try:
        session, engine = connect()
        car = session.query(Car).filter(Car.car_id == car_id).first()
        car.available = availability
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        logging.error(f"Failed to change car availability: {str(e)}")



class Renter:
    def __init__(self, name, email, phone, password, car_id,renter_id=None):
        if renter_id:
            self.renter_id = renter_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.car_id = car_id

    def __str__(self):
        return f"Renter ID: {self.renter_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Car ID: {self.car_id}"

    def __repr__(self):
        return f"Renter ID: {self.renter_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Car ID: {self.car_id}"
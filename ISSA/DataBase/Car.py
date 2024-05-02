class Car:
    def __init__(self, car_id, brand, model, year, owner_id, current_renter, available):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.year = year
        self.owner_id = owner_id
        self.current_renter = current_renter
        self.available = available

    def __str__(self):
        return f"Car ID: {self.car_id}, Brand: {self.brand}, Model: {self.model}, Year: {self.year}, Owner ID: {self.owner_id}, Current Renter: {self.current_renter}, Available: {self.available}"

    def __repr__(self):
        return f"Car ID: {self.car_id}, Brand: {self.brand}, Model: {self.model}, Year: {self.year}, Owner ID: {self.owner_id}, Current Renter: {self.current_renter}, Available: {self.available}"
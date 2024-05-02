class Owner:
    def __init__(self, name, email, phone, password, owner_id=None):
        if owner_id:
            self.owner_id = owner_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

    def __str__(self):
        return f"Owner ID: {self.owner_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Password: {self.password}"

    def __repr__(self):
        return f"Owner ID: {self.owner_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Password: {self.password}"
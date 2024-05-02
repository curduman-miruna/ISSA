class Client_Message:
    def __init__(self, client_id, client_type, message_id, payload):
        self.client_id = client_id
        self.client_type = client_type
        self.message_id = message_id
        self.payload = payload

    def __str__(self):
        return f"Client Id: {self.client_id}, Client Type: {self.client_type}, Message Id: {self.message_id}, Payload: {self.payload}"

    def to_string(self):

        return f"Client Id: {self.client_id}, Client Type: {self.client_type}, Message Id: {self.message_id}, Payload: {self.payload}"

class Car_Message:
    def __init__(self, car_id, message_id, payload):
        self.car_id = car_id
        self.message_id = message_id
        self.payload = payload

    def __str__(self):
        return f"Car Id: {self.car_id}, Message Id: {self.message_id}, Payload: {self.payload}"

    def to_string(self):
        return f"Car Id: {self.car_id}, Message Id: {self.message_id}, Payload: {self.payload}"

    @classmethod
    def from_string(cls, message_str):
        try:
            parts = message_str.split(',')
            car_id = int(parts[0].split(':')[1].strip())
            message_id = int(parts[1].split(':')[1].strip())
            payload = parts[2].split(':')[1].strip()
            return cls(car_id, message_id, payload)
        except Exception as e:
            print("Error parsing message:", e)
            return None

class Server_Message:
    def __init__(self, message_id, payload):
        self.message_id = message_id
        self.payload = payload

    def __str__(self):
        return f"Message Id: {self.message_id}, Payload: {self.payload}"

    def to_string(self):
        return f"Message Id: {self.message_id}, Payload: {self.payload}"

    @classmethod
    def from_string(cls, message_str):
        try:
            parts = message_str.split(',')
            message_id = int(parts[0].split(':')[1].strip())
            payload = parts[1].split(':')[1].strip()
            return cls(message_id, payload)
        except Exception as e:
            print("Error parsing message:", e)
            return None
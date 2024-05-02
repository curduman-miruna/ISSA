import logging
import socket

from message import Client_Message, Server_Message

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

class Client:
    def __init__(self, client_id, client_type):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 12352))
        self.client_id = client_id
        self.client_type = client_type

    def close_connection(self):
        self.client_socket.close()

    def construct_message(self,message_id, payload):
        return Client_Message(self.client_id, self.client_type, message_id, payload)

    def validate_message(self, message):
        return int(message.message_id) in range(6,10)

    def send_message(self, message):
        if not self.validate_message(message):
            print("[-] Invalid message format. Please check message_id.")
            return

        self.client_socket.sendall(message.to_string().encode())
        response = self.client_socket.recv(10000000)

        received_message_str = response.decode().strip()
        received_message = Server_Message.from_string(received_message_str)

        if isinstance(received_message, Server_Message):
            print("[+] Received valid message from server:")
            print(received_message)
        else:
            logging.error("Invalid message received from server: %s", received_message_str)
            print("[-] Invalid message received from server")

if __name__ == "__main__":
    command = input("Command 6-check cars, 7-start-rental, 8-end-rental")
    while command:
        client_id= input("Enter renter id: ")
        client = Client("1","1")
        if command == "6":
            client_message = client.construct_message("6", "1 1 1 1 1 1 1")
            client.send_message(client_message)
        elif command=="7":
            car_id = input("Enter car id: ")
            client_message = client.construct_message("7", car_id)
            client.send_message(client_message)
        elif command == "8":
            client_message = client.construct_message("8", "1 1 1 1 1 1 1")
            client.send_message(client_message)
        command = input("Command 6-check cars, 7-start-rental, 8-end-rental")
    client.close_connection()
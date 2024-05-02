import logging
import socket

from DataBase.Commands import exist_car
from message import Server_Message, Car_Message

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

def validate_message(message):
    return int(message.message_id) in range(6,9)
def construct_message(car_id, message_id, payload):
    return Car_Message(car_id, message_id, payload)

def main():
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 12352

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[*] Connected to the server")
        car_id = input("Enter Car Id: ")
        while(exist_car(car_id)==False):
            print("Car not found")
            car_id = input("Enter Car Id: ")

        while True:
            message_id = input("Enter Message Id (6-9): ")
            payload = input("Enter Payload: ")

            message = construct_message(car_id, message_id, payload)

            if validate_message(message):
                client_socket.sendall(message.to_string().encode())
                response = client_socket.recv(2048)

                received_message_str = response.decode().strip()
                received_message = Server_Message.from_string(received_message_str)

                if isinstance(received_message, Server_Message):
                    print("[+] Received valid message from server:")
                    print(received_message)
                else:
                    logging.error("Invalid message received from server: %s", received_message_str)
                    print("[-] Invalid message received from server")
            else:
                print("[-] Invalid message format. Please check message_id.")

    except Exception as e:
        print("[-] An error occurred:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()

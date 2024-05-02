import logging
import socket
import threading
from message import Server_Message, Client_Message, Car_Message
from DataBase.Commands import create_owner, create_renter, create_car, login_owner, get_available_car_ids, \
    change_car_availability
from DataBase.Models import Owner, Renter, Car
from DataBase.Car import Car

logging.basicConfig(filename='server_error.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

connected_clients = {}
connected_cars = {}

def handle_owner(received_message, client_socket):
    if (received_message.message_id==2):
        split_message = received_message.payload.split(' ')
        car = Car(car_id=split_message[0],brand=split_message[1], model=split_message[2],year=split_message[3], owner_id=received_message.client_id, current_renter=split_message[5], available=True)
        create_car(car)
        response = Server_Message(1, "Valid message")
        client_socket.sendall(response.to_string().encode())
    return None


def handle_renter(received_message, client_socket):
    if (received_message.message_id==6):
        cars = get_available_car_ids()
        response = Server_Message(1,cars )
        client_socket.sendall(response.to_string().encode())
    elif (received_message.message_id==7):
        cars = get_available_car_ids()
        if received_message.payload in cars:
            change_car_availability(received_message.payload, False)
            response = Server_Message(1, "Rented started")
            connected_cars[received_message.payload].sendall(response.to_string().encode())
            client_socket.sendall(response.to_string().encode())
    elif (received_message.message_id==8):\
        cars = get_available_car_ids()
        if received_message.payload not in cars:
            change_car_availability(received_message.payload, True)
            response = Server_Message(1, "Rented ended")
            connected_cars[received_message.payload].sendall(response.to_string().encode())
            client_socket.sendall(response.to_string().encode()

def handle_client(client_socket, address):
    print(f"[+] Accepted connection from {address}")

    while True:
        data = client_socket.recv(10000000)
        if not data:
            break

        message_str = data.decode().strip()
        received_message = parse_message(message_str)

        #client message
        if isinstance(received_message, Client_Message):
            connected_clients[received_message.client_id] = client_socket
            print(connected_clients)
            print("[+] Received valid message from client:")
            print(received_message)
            print(received_message.client_type)
            print(received_message.message_id)
            if received_message.client_type == 0 and (received_message.message_id in [0,3,4,5]):
                print("[-] Error: Owners cannot post,register as renter, start or end rental")
                logging.error("Invalid message received from client: %s", message_str)
                response = Server_Message(0, "Owners cannot post,register as renter, start or end rental")
                client_socket.sendall(response.to_string().encode())
            elif received_message.client_type == 1 and (received_message.message_id == 2 or received_message.message_id == 1):
                print("[-] Error: Renters can only post cars")
                logging.error("Invalid message received from client: %s", message_str)
                response = Server_Message(0, "Renters can only post cars")
                client_socket.sendall(response.to_string().encode())
            else:
                if received_message.client_type == 0:
                    print("Handling owner")
                    handle_owner(received_message, client_socket)
                if received_message.client_type == 1:
                    print("Handling renter")
                    handle_renter(received_message, client_socket)

        elif isinstance(received_message, Car_Message):
            connected_cars[received_message.car_id] = client_socket
            print(connected_cars)
            print("[+] Received valid message from car:")
            print(received_message)
            response = Server_Message(1, "Valid message")
            client_socket.sendall(response.to_string().encode())
        else:
            logging.error("Invalid message received from client: %s", message_str)
            print("[-] Received invalid message from client")
            response = Server_Message(0, "Invalid message")
            client_socket.sendall(response.to_string().encode())


    client_socket.close()
    print(f"[-] Connection with {address} closed")

def parse_message(message_str):
    try:
        parts = message_str.split(',')
        client_id = int(parts[0].split(':')[1].strip())
        client_type = int(parts[1].split(':')[1].strip())
        message_id = int(parts[2].split(':')[1].strip())
        payload = parts[3].split(':')[1].strip()
        return Client_Message(client_id, client_type, message_id, payload)
    except Exception:
        try:
            parts = message_str.split(',')
            car_id = int(parts[0].split(':')[1].strip())
            message_id = int(parts[1].split(':')[1].strip())
            payload = parts[2].split(':')[1].strip()
            return Car_Message(car_id, message_id, payload)
        except Exception as e:
            logging.error("Error parsing message: %s", e)
            print("Error parsing message:", e)
            return None


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[*] Accepted connection from {address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12352

    start_server(HOST, PORT)

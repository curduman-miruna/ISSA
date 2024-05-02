import tkinter as tk
from tkinter import messagebox
from sqlalchemy.exc import SQLAlchemyError
from DataBase.Models import connect, Owner, Renter
from DataBase.Commands import login_owner, login_renter
from client_back import Client


def create_owner(name, email, phone, password):
    print("Creating owner")
    try:
        session, engine = connect()
        new_owner = Owner(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        session.add(new_owner)
        session.commit()
        session.close()
        messagebox.showinfo("Success", "Owner registered successfully!")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Failed to create owner: {str(e)}")

def create_renter(name, email, phone, password):
    print("Creating renter")
    try:
        session, engine = connect()
        new_renter = Renter(
            name=name,
            email=email,
            phone=phone,
            password=password
        )
        session.add(new_renter)
        session.commit()
        session.close()
        messagebox.showinfo("Success", "Renter registered successfully!")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Failed to create renter: {str(e)}")

def register_owner_window():
    register_window = tk.Toplevel(root)
    register_window.title("Register Owner")

    label_name = tk.Label(register_window, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(register_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_email = tk.Label(register_window, text="Email:")
    label_email.grid(row=1, column=0, padx=10, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    label_phone = tk.Label(register_window, text="Phone:")
    label_phone.grid(row=2, column=0, padx=10, pady=5)
    entry_phone = tk.Entry(register_window)
    entry_phone.grid(row=2, column=1, padx=10, pady=5)

    label_password = tk.Label(register_window, text="Password:")
    label_password.grid(row=3, column=0, padx=10, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=3, column=1, padx=10, pady=5)

    register_button = tk.Button(register_window, text="Register", command=lambda: create_owner(
        name=entry_name.get(),
        email=entry_email.get(),
        phone=entry_phone.get(),
        password=entry_password.get()
    ))
    register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def register_renter_window():
    register_window = tk.Toplevel(root)
    register_window.title("Register Renter")

    label_name = tk.Label(register_window, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(register_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_email = tk.Label(register_window, text="Email:")
    label_email.grid(row=1, column=0, padx=10, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    label_phone = tk.Label(register_window, text="Phone:")
    label_phone.grid(row=2, column=0, padx=10, pady=5)
    entry_phone = tk.Entry(register_window)
    entry_phone.grid(row=2, column=1, padx=10, pady=5)

    label_password = tk.Label(register_window, text="Password:")
    label_password.grid(row=3, column=0, padx=10, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=3, column=1, padx=10, pady=5)

    register_button = tk.Button(register_window, text="Register", command=lambda: create_renter(
        name=entry_name.get(),
        email=entry_email.get(),
        phone=entry_phone.get(),
        password=entry_password.get()
    ))
    register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def login_owner_window():
    def handle_login():
        email = entry_email.get()
        password = entry_password.get()
        owner = login_owner(email, password)
        if owner:
            messagebox.showinfo("Success", "Owner logged in successfully!")
            display_register_cars_window()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    register_window = tk.Toplevel(root)
    register_window.title("Login Owner")

    label_email = tk.Label(register_window, text="Email:")
    label_email.grid(row=1, column=0, padx=10, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    label_password = tk.Label(register_window, text="Password:")
    label_password.grid(row=3, column=0, padx=10, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(register_window, text="Login", command=handle_login)
    login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def login_renter_window():
    def handle_login():
        email = entry_email.get()
        password = entry_password.get()
        renter = login_renter(email, password)
        if renter:
            messagebox.showinfo("Success", "Renter logged in successfully!")
            display_available_cars_window()
        else:
            messagebox.showerror("Error", "Invalid email or password")


    register_window = tk.Toplevel(root)
    register_window.title("Login Renter")

    label_email = tk.Label(register_window, text="Email:")
    label_email.grid(row=1, column=0, padx=10, pady=5)
    entry_email = tk.Entry(register_window)
    entry_email.grid(row=1, column=1, padx=10, pady=5)

    label_password = tk.Label(register_window, text="Password:")
    label_password.grid(row=3, column=0, padx=10, pady=5)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(register_window, text="Login", command=handle_login)
    login_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

def display_register_cars_window():
    # Funcția pentru afișarea mașinilor disponibile
    register_cars_window = tk.Toplevel(root)
    register_cars_window.title("Register Cars")

    # Label și câmp pentru brand
    label_brand = tk.Label(register_cars_window, text="Brand:")
    label_brand.grid(row=0, column=0, padx=10, pady=5)
    entry_brand = tk.Entry(register_cars_window)
    entry_brand.grid(row=0, column=1, padx=10, pady=5)

    # Label și câmp pentru model
    label_model = tk.Label(register_cars_window, text="Model:")
    label_model.grid(row=1, column=0, padx=10, pady=5)
    entry_model = tk.Entry(register_cars_window)
    entry_model.grid(row=1, column=1, padx=10, pady=5)

    # Label și câmp pentru an
    label_year = tk.Label(register_cars_window, text="An:")
    label_year.grid(row=2, column=0, padx=10, pady=5)
    entry_year = tk.Entry(register_cars_window)
    entry_year.grid(row=2, column=1, padx=10, pady=5)
    # Buton pentru a înregistra mașina cu informațiile introduse
    register_car_button = tk.Button(register_cars_window, text="Înregistrează mașina", command=lambda: register_car(entry_brand.get(), entry_model.get(), entry_year.get()))
    register_car_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def register_car(car_id, brand, model, year, owner_id):
    # Concatenăm datele într-un șir de caractere
    car_data_str = (f"{car_id} {brand} {model} {year} {owner_id} {current_renter} {available}")
    client = Client(owner_id, "0")
    client_message = client.construct_message("2", car_data_str)
    client.send_message(client_message)
    # Afișăm mesajul cu datele mașinii
    messagebox.showinfo("Car Data", car_data_str)



def display_available_cars_window():
    available_cars_window = tk.Toplevel(root)
    available_cars_window.title("Available Cars")

root = tk.Tk()
root.title("Login and Registration")

# Setarea dimensiunilor butoanelor
button_width = 15
button_height = 2

# Butonul pentru register owner
register_owner_btn = tk.Button(root, text="Register Owner", command=register_owner_window, width=button_width,
                               height=button_height)
register_owner_btn.grid(row=0, column=1, padx=10, pady=10)

# Butonul pentru register renter
register_renter_btn = tk.Button(root, text="Register Renter", command=register_renter_window, width=button_width,
                                height=button_height)
register_renter_btn.grid(row=1, column=1, padx=10, pady=10)

# Butonul pentru login owner
login_owner_btn = tk.Button(root, text="Login Owner", command=login_owner_window, width=button_width,
                            height=button_height)
login_owner_btn.grid(row=0, column=0, padx=10, pady=10)

# Butonul pentru login renter
login_renter_btn = tk.Button(root, text="Login Renter", command=login_renter_window, width=button_width,
                             height=button_height)
login_renter_btn.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
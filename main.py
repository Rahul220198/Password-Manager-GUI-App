from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- CONSTANTS ---------------------------- #
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y',
           'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    password_letters = [random.choice(LETTERS) for _ in range(nr_letters)]
    password_symbols = [random.choice(NUMBERS) for _ in range(nr_numbers)]
    password_numbers = [random.choice(SYMBOLS) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    record_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }

    if len(website) == 0:
        messagebox.showinfo(title="Error", message=f"please Enter Website!!")
        website_entry.focus()
    elif len(email) == 0:
        messagebox.showinfo(title="Error", message=f"please Enter Email!!")
        email_entry.focus()
    elif len(password) == 0:
        messagebox.showinfo(title="Error", message="Please Enter Password!!")
        password_entry.focus()
    else:
        messagebox.askokcancel(title=website, message=f"Email:{email} \nPassword:{password}")

        try:
            with open("record.json", "r") as data_files:
                # Reading the Old Data
                data = json.load(data_files)
        except FileNotFoundError:
            with open("record.json", "w") as data_files:
                json.dump(record_data, data_files, indent=4)
        else:
            # Updating old data with new data
            data.update(record_data)

            with open("record.json", "w") as data_files:
                # Saving Updated data
                json.dump(data, data_files, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- SEARCH RECORD ------------------------------- #
def find_record():
    search_website = website_entry.get()
    try:
        with open("record.json", "r") as data_files:
            data = json.load(data_files)
    except FileNotFoundError:
        messagebox.showinfo(title="File Not Found", message="File Not Exist")
    else:
        if search_website in data:
            email_name = data[search_website]["email"]
            password = data[search_website]["password"]
            messagebox.showinfo(title=search_website, message=f"Email:{email_name} \nPassword:{password}")
        elif search_website not in data:
            messagebox.showinfo(title=search_website, message="The Record you are searching is not Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="grey")

canvas = Canvas(height=189, width=200, highlightthickness=0, bg="grey")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=logo_img)
canvas.grid(row=0, column=1)

# --------------- Labels --------------- #
website_label = Label(text="Website:", bg="grey")
website_label.grid(row=1, column=0)

user_label = Label(text="Email/Username:", bg="grey")
user_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg="grey")
password_label.grid(row=3, column=0)

# --------------- Entries --------------- #
website_entry = Entry(width=34, fg="black")
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=53, fg="black")
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "rahul@gmail.com")

password_entry = Entry(width=34, fg="black")
password_entry.grid(row=3, column=1)

# --------------- Buttons --------------- #
generate_button = Button(text="Generate Password", command=generate_password, bg="grey")
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=45, command=save, bg="grey")
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=int(14.75), command=find_record, bg="grey")
search_button.grid(row=1, column=2)

window.mainloop()

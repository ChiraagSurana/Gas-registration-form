import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry  # Import the DateEntry widget
import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gas_registration"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error: ", err)

# Function to create the gas registration table
def create_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS registration (id INT AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), adhaarcard_no VARCHAR(255), address TEXT, dob DATE, phone_no VARCHAR(255), gas_type VARCHAR(255))")
    conn.commit()
    conn.close()

# Function to insert data into the gas registration table
def submit_record():
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    adhaarcard_no = entry_adhaarcard_no.get()
    address = entry_address.get("1.0", tk.END)
    dob = dob_calendar.get()
    phone_no = entry_phone_no.get()
    gas_type = entry_gas_type_var.get()

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registration (firstname, lastname, adhaarcard_no, address, dob, phone_no, gas_type) VALUES (%s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, adhaarcard_no, address, dob, phone_no, gas_type))
    conn.commit()
    messagebox.showinfo("Success", "Record submitted successfully! Your ID is: " + str(cursor.lastrowid))
    conn.close()

# Function to fetch records from the gas registration table
def fetch_record():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration")
    records = cursor.fetchall()
    conn.close()

    listbox_records.delete(0, tk.END)  # Clear previous entries
    for record in records:
        listbox_records.insert(tk.END, record)

# Function to delete a record from the gas registration table
def delete_record():
    id = entry_id.get()
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registration WHERE id = %s", (id,))
    conn.commit()
    messagebox.showinfo("Success", "Record deleted successfully!")
    conn.close()

# Function to clear all entry fields
def clear_fields():
    entry_firstname.delete(0, tk.END)
    entry_lastname.delete(0, tk.END)
    entry_adhaarcard_no.delete(0, tk.END)
    entry_address.delete("1.0", tk.END)
    dob_calendar.delete(0, tk.END)
    entry_phone_no.delete(0, tk.END)
    entry_gas_type_var.delete(0, tk.END)

# Function to update a record in the gas registration table
def update_record():
    id_to_update = simpledialog.askinteger("Update Record", "Enter ID of the record you want to update:")
    if id_to_update is None:
        return

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registration WHERE id = %s", (id_to_update,))
    record = cursor.fetchone()
    conn.close()

    if record is None:
        messagebox.showerror("Error", f"No record found with ID {id_to_update}.")
        return
        # Create a new window for updating record
    update_window = tk.Toplevel(root)
    update_window.title("Update Record")

        # Labels
    label_firstname = tk.Label(update_window, text="First Name:")
    label_firstname.grid(row=0, column=2, padx=10, pady=5)
    label_lastname = tk.Label(update_window, text="Last Name:")
    label_lastname.grid(row=1, column=2, padx=10, pady=5)
    label_adhaarcard_no = tk.Label(update_window, text="Adhaar Card No:")
    label_adhaarcard_no.grid(row=2, column=2, padx=10, pady=5, sticky="e")
    label_address = tk.Label(update_window, text="Address:")
    label_address.grid(row=3, column=2, padx=10, pady=5, sticky="e")
    label_phone_no = tk.Label(update_window, text="Phone No:")
    label_phone_no.grid(row=4, column=2, padx=10, pady=5, sticky="e")
    label_gas_type = tk.Label(update_window, text="Gas Type:")
    label_gas_type.grid(row=5, column=2, padx=10, pady=5, sticky="e")
    # Add labels for other fields...

    # Entry fields with current values
    entry_firstname = tk.Entry(update_window)
    entry_firstname.insert(0, record[1])
    entry_firstname.grid(row=0, column=3, padx=10, pady=5)
    entry_lastname = tk.Entry(update_window)
    entry_lastname.insert(0, record[2])
    entry_lastname.grid(row=1, column=3, padx=10, pady=5)
    entry_adhaarcard_no = tk.Entry(update_window)
    entry_adhaarcard_no.insert(0, record[3])
    entry_adhaarcard_no.grid(row=2, column=3, padx=10, pady=5, sticky="w")
    entry_address = tk.Entry(update_window)
    entry_address.insert(0, record[4])
    entry_address.grid(row=3, column=3, padx=10, pady=5, sticky="w")
    entry_phone_no = tk.Entry(update_window)
    entry_phone_no.insert(0, record[6])
    entry_phone_no.grid(row=4, column=3, padx=10, pady=5, sticky="w")
    entry_gas_type = tk.Entry(update_window)
    entry_gas_type.insert(0, record[7])
    entry_gas_type.grid(row=5, column=3, padx=10, pady=5, sticky="w")


    # Add entry fields for other fields...

    # Update button
    def perform_update():
        updated_firstname = entry_firstname.get()
        updated_lastname = entry_lastname.get()
        updated_adhaarcard_no = entry_adhaarcard_no.get()
        updated_address = entry_address.get()
        updated_phone_no = entry_phone_no.get()


        # Get updated values from other entry fields...

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE registration SET firstname = %s, lastname = %s, adhaarcard_no = %s, address = %s, phone_no = %s WHERE id = %s",(updated_firstname, updated_lastname, updated_adhaarcard_no, updated_address, updated_phone_no, id_to_update))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record updated successfully!")
        update_window.destroy()

    button_update = tk.Button(update_window, text="Update", command=perform_update)
    button_update.grid(row=8, column=2, columnspan=2, padx=10, pady=5)


# GUI
root = tk.Tk()
root.title("Gas Registration Form")

# Labels
label_firstname = tk.Label(root, text="First Name:")
label_firstname.grid(row=0, column=2, pady=5, sticky="e")
label_lastname = tk.Label(root, text="Last Name:")
label_lastname.grid(row=1, column=2, padx=10, pady=5, sticky="e")
label_adhaarcard_no = tk.Label(root, text="Adhaar Card No:")
label_adhaarcard_no.grid(row=2, column=2, padx=10, pady=5, sticky="e")
label_address = tk.Label(root, text="Address:")
label_address.grid(row=3, column=2, padx=10, pady=5, sticky="e")
label_dob = tk.Label(root, text="Date of Birth:")
label_dob.grid(row=4, column=2, padx=10, pady=5, sticky="e")
label_phone_no = tk.Label(root, text="Phone No:")
label_phone_no.grid(row=5, column=2, padx=10, pady=5, sticky="e")
label_gas_type = tk.Label(root, text="Gas Type:")
label_gas_type.grid(row=6, column=2, padx=10, pady=5, sticky="e")


# Entry fields
entry_firstname = tk.Entry(root)
entry_firstname.grid(row=0, column=3, padx=10, pady=5, sticky="w")
entry_lastname = tk.Entry(root)
entry_lastname.grid(row=1, column=3, padx=10, pady=5, sticky="w")
entry_adhaarcard_no = tk.Entry(root)
entry_adhaarcard_no.grid(row=2, column=3, padx=10, pady=5, sticky="w")
entry_address = tk.Text(root, height=4, width=20)
entry_address.grid(row=3, column=3, padx=10, pady=5, sticky="w")
dob_calendar = DateEntry(root, width=12, background='darkblue',
                         foreground='white', borderwidth=2)
dob_calendar.grid(row=4, column=3, padx=10, pady=5, sticky="w")
entry_phone_no = tk.Entry(root)
entry_phone_no.grid(row=5, column=3, padx=10, pady=5, sticky="w")
entry_gas_type_var = tk.StringVar(root)
entry_gas_type_var.set("Select Gas Type")
entry_gas_type_options = ["LPG", "CNG", "Propane"]
entry_gas_type_dropdown = tk.OptionMenu(root,entry_gas_type_var, *entry_gas_type_options)
entry_gas_type_dropdown.grid(row=6, column=3, padx=5, pady=5, sticky="w")



# Buttons
button_submit = tk.Button(root, text="Submit", command=submit_record)
button_submit.grid(row=8, column=2, padx=10, pady=5, sticky="e")
button_clear = tk.Button(root, text="Clear", command=clear_fields)
button_clear.grid(row=8, column=3, padx=10, pady=5, sticky="w")
button_fetch_record = tk.Button(root, text="Fetch Record", command=fetch_record)
button_fetch_record.grid(row=9, column=2, padx=10, pady=5, sticky="e")
button_delete_record = tk.Button(root, text="Delete Record", command=delete_record)
button_delete_record.grid(row=10, column=2, padx=10, pady=5, sticky="e")
label_id = tk.Label(root, text="ID:")
label_id.grid(row=10, column=3, padx=10, pady=5, sticky="w")
entry_id = tk.Entry(root)
entry_id.grid(row=10, column=3, padx=10, pady=5)

button_update_record = tk.Button(root, text="Update Record", command=update_record)
button_update_record.grid(row=9, column=3, padx=10, pady=5, sticky="w")

# Listbox to display fetched records
listbox_records = tk.Listbox(root, width=80)
listbox_records.grid(row=18, column=0, columnspan=5, padx=10, pady=5)

# Create the gas registration table if it doesn't exist
create_table()

root.mainloop()

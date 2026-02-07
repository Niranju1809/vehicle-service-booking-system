import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql


# Database Connection 
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Niranju001",
        database="service"
    )
#____________GUI______________________________
root = tk.Tk()
root.title("Vehicle Service Booking System")
root.geometry("500x500")


login_frame = tk.Frame(root)
booking_frame = tk.Frame(root)


for frame in (login_frame, booking_frame):
    frame.place(x=0, y=0, relwidth=1, relheight=1)



# -------------------- LOGIN ---------------------
def login():
    if username.get() == "admin" and password.get() == "1234":
        login_frame.pack_forget()
        show_frame(booking_frame)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

username = tk.StringVar()
password = tk.StringVar()

center_frame = tk.Frame(login_frame)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(center_frame, text="Username").grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(center_frame, textvariable=username).grid(row=0, column=1, padx=10)

tk.Label(center_frame, text="Password").grid(row=1, column=0, padx=5)
tk.Entry(center_frame, textvariable=password, show='*').grid(row=1, column=1, padx=10)

tk.Button(center_frame, text="Login", command=login).grid(row=4, column=1, padx=10)


# --- Function to Show Frames ---
def show_frame(frame):
    frame.tkraise()

# Start with login
show_frame(login_frame)


# Variables
id = tk.StringVar()
name = tk.StringVar()
contact = tk.StringVar()
model = tk.StringVar()
reg = tk.StringVar()
service_type = tk.StringVar()
service_date = tk.StringVar()
mechanic = tk.StringVar()
status = tk.StringVar()

# -------------------- Functions ---------------------


def add_booking():
    try:
        con = connect_db()
        cur = con.cursor()
        query = """INSERT INTO booking (customer_name, contact_number, vehicle_model,
                    registration_number, service_type, service_date,
                    assigned_mechanic, service_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (
            name.get(),
            contact.get(),
            model.get(),
            reg.get(),
            service_type.get(),
            service_date.get(),
            mechanic.get(),
            status.get()
        )
        cur.execute(query, values)
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Booking Added Successfully!")
        clear_fields()
        view_bookings()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    id.set("")
    name.set("")
    contact.set("")
    model.set("")
    reg.set("")
    service_type.set("")
    service_date.set("")
    mechanic.set("")
    status.set("")

def view_bookings():
    for item in tree.get_children():
        tree.delete(item)
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM booking")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load_selected(event):
    selected = tree.focus()
    data = tree.item(selected, "values")
    if data:
        id.set(data[0])
        name.set(data[1])
        contact.set(data[2])
        model.set(data[3])
        reg.set(data[4])
        service_type.set(data[5])
        service_date.set(data[6])
        mechanic.set(data[7])
        status.set(data[8])

def update_booking():
    if id.get() == "":
        messagebox.showwarning("Select Record", "Please select a record to update.")
        return
    try:
        con = connect_db()
        cur = con.cursor()
        query = """UPDATE booking SET customer_name=%s, contact_number=%s, vehicle_model=%s,
                   registration_number=%s, service_type=%s, service_date=%s,
                   assigned_mechanic=%s, service_status=%s WHERE id=%s"""
        values = (
            name.get(),
            contact.get(),
            model.get(),
            reg.get(),
            service_type.get(),
            service_date.get(),
            mechanic.get(),
            status.get(),
            id.get()
        )
        cur.execute(query, values)
        con.commit()
        con.close()
        messagebox.showinfo("Updated", "Booking Updated Successfully!")
        clear_fields()
        view_bookings()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_booking():
    if id.get() == "":
        messagebox.showwarning("Select Record", "Please select a record to delete.")
        return
    try:
        con = connect_db()
        cur = con.cursor()
        cur.execute("DELETE FROM booking WHERE id=%s", (id.get(),))
        con.commit()
        con.close()
        messagebox.showinfo("Deleted", "Booking Deleted Successfully!")
        clear_fields()
        view_bookings()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------- Form ---------------------
form_frame = tk.Frame(booking_frame)
form_frame.place(x=20, y=20)

tk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=name, width=30).grid(row=0, column=1, padx=10)

tk.Label(form_frame, text="Contact Number:").grid(row=1, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=contact, width=30).grid(row=1, column=1)

tk.Label(form_frame, text="Vehicle Model:").grid(row=2, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=model, width=30).grid(row=2, column=1)

tk.Label(form_frame, text="Registration Number:").grid(row=3, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=reg, width=30).grid(row=3, column=1)

tk.Label(form_frame, text="Service Type:").grid(row=4, column=0, sticky="e", pady=5)
ttk.Combobox(form_frame, textvariable=service_type, values=["Oil Change", "Engine Check", "Full Service"], width=28).grid(row=4, column=1)

tk.Label(form_frame, text="Service Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=service_date, width=30).grid(row=5, column=1)

tk.Label(form_frame, text="Assigned Mechanic:").grid(row=6, column=0, sticky="e", pady=5)
tk.Entry(form_frame, textvariable=mechanic, width=30).grid(row=6, column=1)

tk.Label(form_frame, text="Service Status:").grid(row=7, column=0, sticky="e", pady=5)
ttk.Combobox(form_frame, textvariable=status, values=["Pending", "In Progress", "Completed"], width=28).grid(row=7, column=1)

# Buttons
tk.Button(form_frame, text="Add", command=add_booking, width=12).grid(row=8, column=0, pady=15)
tk.Button(form_frame, text="Update", command=update_booking, width=12).grid(row=8, column=1)
tk.Button(form_frame, text="Delete", command=delete_booking, width=12).grid(row=9, column=0)
tk.Button(form_frame, text="Clear", command=clear_fields, width=12).grid(row=9, column=1)

# -------------------- Treeview Table ---------------------
tree_frame = tk.Frame(booking_frame)
tree_frame.place(x=420, y=20)

cols = ("ID", "Name", "Contact", "Model", "Reg No", "Type", "Date", "Mechanic", "Status")
tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=22)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()
tree.bind("<ButtonRelease-1>", load_selected)

view_bookings()

root.mainloop()

import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS users
(username TEXT PRIMARY KEY, password TEXT NOT NULL, phoneno TEXT NOT NULL);
''')
con.commit()


def signup_window():
    sign = Tk()
    sign.title("Sign up Page")
    sign.geometry("300x400")
    Label(sign,text="NOTE: \n All fields are require. \n length of password should be greater than 8 \n length of phone no =10",font=("Arial",10),fg="red").pack(pady=5)
    Label(sign, text="Username:").pack(pady=5)
    username_entry = Entry(sign)
    username_entry.pack()

    Label(sign, text="Password:").pack(pady=5)
    password_entry = Entry(sign, show="*")
    password_entry.pack()

    Label(sign, text="Confirm Password:").pack(pady=5)
    confirmpassword_entry = Entry(sign, show="*")
    confirmpassword_entry.pack()

    Label(sign, text="Contact Number:").pack(pady=5)
    phone_entry = Entry(sign)
    phone_entry.pack()

    def register():
        uname = username_entry.get()
        pwd = password_entry.get()
        cpwd = confirmpassword_entry.get()
        phone = phone_entry.get()

        if not uname or not pwd or not cpwd or not phone:
            messagebox.showwarning("Error", "All fields are required.")
            return
        if len(pwd) < 8:
            messagebox.showerror("Length Error", "Password length should be at least 8 characters.")
            return
        if pwd != cpwd:
            messagebox.showerror("Error", "Password and Confirm Password should be same.")
            return
        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Phone number should be 10 digits.")
            return
        try:
            cur.execute("INSERT INTO users VALUES(?,?,?)", (uname, pwd, phone))
            con.commit()
            messagebox.showinfo("Success", "Signup Successful")
            sign.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "User already exists.")

    Button(sign, text="Register", command=register, bg="green", fg="white").pack(pady=15)
    sign.mainloop()

# login
def login_window():
    login = Tk()
    login.title("Login Page")
    login.geometry("300x200")

    Label(login, text="Username").pack(pady=5)
    username_entry = Entry(login)
    username_entry.pack()

    Label(login, text="Password").pack(pady=5)
    password_entry = Entry(login, show="*")
    password_entry.pack()

    def do_login():
        uname = username_entry.get()
        pwd = password_entry.get()

        if not uname or not pwd:
            messagebox.showwarning("Error", "All fields are required.")
            return

        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (uname, pwd))
        if cur.fetchone():
            messagebox.showinfo("Success", "Login Successful")
            login.destroy()
            dashboard()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    Button(login, text="Login", command=do_login, bg="blue", fg="white", width=15).pack(pady=10)
    Button(login, text="Sign up", command=signup_window, width=15).pack()
    login.mainloop()

# donor
def blood_donor():
    conn = sqlite3.connect("bloods.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bloods 
        (blood_group TEXT PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL, phoneno TEXT NOT NULL);
    ''')
    conn.commit()

    def add_data():
        blood = blood_entry.get()
        name = name_entry.get()
        city = city_entry.get()
        phoneno = phone_entry.get()

        if not blood or not name or not city or not phoneno:
            messagebox.showwarning("Error", "All fields are required.")
            return
        if len(phoneno) != 10 or not phoneno.isdigit():
            messagebox.showerror("Error", "Invalid Phone Number")
            return
        try:
            cur.execute("INSERT INTO bloods VALUES(?,?,?,?)", (blood, name, city, phoneno))
            conn.commit()
            status_label.config(text="Record Added", fg='green')
            view_all()
            clear_entries()
        except sqlite3.IntegrityError:
            status_label.config(text="Blood Group already exists!", fg='red')

    def view_all():
        for row in tree.get_children():
            tree.delete(row)
        cur.execute("SELECT * FROM bloods")
        for row in cur.fetchall():
            tree.insert("", END, values=row)

    def clear_entries():
        blood_entry.delete(0, END)
        name_entry.delete(0, END)
        city_entry.delete(0, END)
        phone_entry.delete(0, END)

    def select_record(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            clear_entries()
            blood_entry.insert(0, values[0])
            name_entry.insert(0, values[1])
            city_entry.insert(0, values[2])
            phone_entry.insert(0, values[3])

    def update_record():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Select", "Select a record to update.")
            return
        blood = blood_entry.get()
        name = name_entry.get()
        city = city_entry.get()
        phone = phone_entry.get()
        if blood and name and city and phone:
            cur.execute("UPDATE bloods SET name=?, city=?, phoneno=? WHERE blood_group=?", (name, city, phone, blood))
            conn.commit()
            status_label.config(text="Record Updated", fg='green')
            view_all()
            clear_entries()
        else:
            status_label.config(text="All fields required!", fg='red')

    def delete_record():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Select", "Select a record to delete.")
            return
        values = tree.item(selected, 'values')
        confirm = messagebox.askyesno("Confirm", "Delete this record?")
        if confirm:
            cur.execute("DELETE FROM bloods WHERE blood_group=?", (values[0],))
            conn.commit()
            status_label.config(text="Deleted", fg='green')
            view_all()
            clear_entries()

    root = Tk()
    root.title("Blood Donor Data")
    root.geometry("600x500")
    font12 = ('Arial', 11)
    # Label(root,text="blood group should be capital. (A+,A-,B+,B-,AB+,AB-,O+,O-)",fg="red").pack(pady=8)
    Label(root, text="Blood Group", font=font12).grid(row=0, column=0, padx=30, pady=5, sticky=W)
    blood_entry = Entry(root, font=font12)
    blood_entry.grid(row=0, column=1)

    Label(root, text="Name", font=font12).grid(row=1, column=0, padx=30, pady=5, sticky=W)
    name_entry = Entry(root, font=font12)
    name_entry.grid(row=1, column=1)

    Label(root, text="City", font=font12).grid(row=2, column=0, padx=30, pady=5, sticky=W)
    city_entry = Entry(root, font=font12)
    city_entry.grid(row=2, column=1)

    Label(root, text="Phone No", font=font12).grid(row=3, column=0, padx=30, pady=5, sticky=W)
    phone_entry = Entry(root, font=font12)
    phone_entry.grid(row=3, column=1)

    btn_width = 16
    Button(root, text="Add Data", command=add_data, font=font12, bg='green', fg='white', width=btn_width).grid(row=4, column=0, padx=10, pady=5, sticky=E)
    Button(root, text="View All", command=view_all, font=font12, bg='purple', fg='white', width=btn_width).grid(row=4, column=1, padx=10, pady=5, sticky=W)
    Button(root, text="Update Selected", command=update_record, font=font12, bg='grey', fg='white', width=btn_width).grid(row=5, column=0, padx=10, pady=5, sticky=E)
    Button(root, text="Delete Selected", command=delete_record, font=font12, bg='pink', fg='white', width=btn_width).grid(row=5, column=1, padx=10, pady=5, sticky=W)

    status_label = Label(root, text="", font=font12)
    status_label.grid(row=6, column=0, columnspan=2)

    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 12))
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

    tree = ttk.Treeview(root, columns=("Blood", "Name", "City", "Phone"), show='headings', height=8)
    tree.heading("Blood", text="Blood Group")
    tree.heading("Name", text="Name")
    tree.heading("City", text="City")
    tree.heading("Phone", text="Phone No")
    tree.column("Blood", width=100, anchor=CENTER)
    tree.column("Name", width=150, anchor=CENTER)
    tree.column("City", width=100, anchor=CENTER)
    tree.column("Phone", width=100, anchor=CENTER)
    tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    scrollbar = Scrollbar(root, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=7, column=2, sticky='ns')

    tree.bind("<<TreeviewSelect>>", select_record)

    Button(root, text="Exit", command=root.destroy, font=font12, bg='blue', fg='white', width=btn_width).grid(row=8, column=0, columnspan=2, pady=10)
    root.mainloop()

# search
def search_donor():
    conn = sqlite3.connect("bloods.db")
    cur = conn.cursor()

    search_win = Tk()
    search_win.title("Search Donor")
    search_win.geometry("500x400")
    # Label(search_win,text="blood group should be capital. (A+,A-,B+,B-,AB+,AB-,O+,O-)",fg="red").pack()
    Label(search_win, text="Blood Group").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    blood_entry = Entry(search_win)
    blood_entry.grid(row=0, column=1)

    Label(search_win, text="City").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    city_entry = Entry(search_win)
    city_entry.grid(row=1, column=1)

    style = ttk.Style()
    font12 = ("Arial", 12)
    style.configure("Treeview", font=font12)
    style.configure("Treeview.Heading", font=font12)

    tree = ttk.Treeview(search_win, columns=("Blood", "Name", "City", "Phone"), show="headings")
    tree.heading("Blood", text="Blood Group")
    tree.heading("Name", text="Name")
    tree.heading("City", text="City")
    tree.heading("Phone", text="Phone No")
    tree.column("Blood", width=100, anchor=CENTER)
    tree.column("Name", width=120, anchor=CENTER)
    tree.column("City", width=120, anchor=CENTER)
    tree.column("Phone", width=120, anchor=CENTER)
    tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    scrollbar = Scrollbar(search_win, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=3, column=3, sticky='ns')

    def do_search():
        blood = blood_entry.get()
        city = city_entry.get()
        for row in tree.get_children():
            tree.delete(row)
        if not blood or not city:
            messagebox.showerror("Error", "Please fill all fields")
            return
        cur.execute("SELECT * FROM bloods WHERE blood_group=? AND city=?", (blood, city))
        rows = cur.fetchall()
        if rows:
            for r in rows:
                tree.insert("", END, values=r)
        else:
            messagebox.showinfo("No Results", "No donor found with given details.")

    Button(search_win, text="Search", command=do_search, bg="green", fg="white").grid(row=2, column=0, pady=10)


    search_win.mainloop()

# dasboard
def dashboard():
    dash = Tk()
    dash.title("Blood Bank Dashboard")
    dash.geometry("400x350")
    dash.configure(bg="pink")
    font12 = ("Arial", 14, "bold")
    Label(dash, text="WELCOME TO BLOOD BANK 🩸", font=font12).pack(pady=20)

    Button(dash, text="Blood Donor", command=blood_donor, font=font12, width=25, height=2,bg="green",fg="white").pack(pady=20)
    Button(dash, text="Search Blood", command=search_donor, font=font12, width=25, height=2,bg="red",fg="white").pack(pady=20)

    dash.mainloop()

login_window()

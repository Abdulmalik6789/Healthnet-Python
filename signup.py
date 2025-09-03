import tkinter as tk
from tkinter import ttk, messagebox

class SignupPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.patient_map = {}
        self.doctor_map = {}
        self.staff_map = {}
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        center_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', bd=2)
        center_frame.pack(pady=50, padx=50)

        tk.Label(center_frame, text="Create Account", font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

        form_frame = tk.Frame(center_frame, bg='white')
        form_frame.pack(pady=20, padx=40)

        # Role Selection
        tk.Label(form_frame, text="Role:", font=('Arial', 12, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.role_var = tk.StringVar(value="Patient")
        role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, width=27,
                                 values=["Patient", "Doctor", "Staff"], state="readonly", font=('Arial', 12))
        role_combo.grid(row=0, column=1, pady=5, ipady=5)
        role_combo.bind("<<ComboboxSelected>>", self.load_names)

        # Name dropdown
        tk.Label(form_frame, text="Select Name:", font=('Arial', 12, 'bold'), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        self.name_combo = ttk.Combobox(form_frame, textvariable=self.name_var, width=27, state="readonly", font=('Arial', 12))
        self.name_combo.grid(row=1, column=1, pady=5, ipady=5)

        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 12, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, bg='#f8f9fa')
        self.username_entry.grid(row=2, column=1, pady=5, ipady=5)

        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 12, 'bold'), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*', bg='#f8f9fa')
        self.password_entry.grid(row=3, column=1, pady=5, ipady=5)

        # Confirm Password
        tk.Label(form_frame, text="Confirm Password:", font=('Arial', 12, 'bold'), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        self.confirm_password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*', bg='#f8f9fa')
        self.confirm_password_entry.grid(row=4, column=1, pady=5, ipady=5)

        # Email
        tk.Label(form_frame, text="Email:", font=('Arial', 12, 'bold'), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, bg='#f8f9fa')
        self.email_entry.grid(row=5, column=1, pady=5, ipady=5)

        # Phone
        tk.Label(form_frame, text="Phone:", font=('Arial', 12, 'bold'), bg='white').grid(row=6, column=0, sticky='w', pady=5)
        self.phone_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, bg='#f8f9fa')
        self.phone_entry.grid(row=6, column=1, pady=5, ipady=5)

        # Buttons
        buttons_frame = tk.Frame(center_frame, bg='white')
        buttons_frame.pack(pady=30, fill='x', padx=40)
        
        tk.Button(buttons_frame, text="← Back to Login", font=('Arial', 12),
                  bg='#6c757d', fg='white', relief='flat', command=self.app.show_login).pack(side='left', ipadx=15, ipady=8)

        tk.Button(buttons_frame, text="Create Account", font=('Arial', 12, 'bold'),
                  bg='#4CAF50', fg='white', relief='flat', command=self.handle_signup).pack(side='right', ipadx=15, ipady=8)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_names(self, event=None):
        role = self.role_var.get()
        if role == "Patient":
            patients = self.app.db.get_all_patients()
            self.patient_map = {f"{p['first_name']} {p['last_name']}": p['id'] for p in patients}
            self.name_combo['values'] = list(self.patient_map.keys())
        elif role == "Doctor":
            doctors = self.app.db.get_all_doctors_for_signup()
            self.doctor_map = {f"{d['first_name']} {d['last_name']}": d['id'] for d in doctors}
            self.name_combo['values'] = list(self.doctor_map.keys())
        elif role == "Staff":
           staff = self.app.db.get_all_staff()  # ✅ fetch from DB
           self.staff_map = {s['full_name']: s['id'] for s in staff}
           self.name_combo['values'] = list(self.staff_map.keys())

    def handle_signup(self):
        role = self.role_var.get()
        name = self.name_var.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not username or not password:
            messagebox.showerror("Error", "Please fill all required fields")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if role == "Patient":
            linked_id = self.patient_map.get(name)
        elif role == "Doctor":
            linked_id = self.doctor_map.get(name)
        else:
            linked_id = self.staff_map.get(name)

        if not linked_id:
            messagebox.showerror("Error", "Invalid selection")
            return

        success = self.app.db.create_user(linked_id, role, username, password, email, phone)
        if success:
            messagebox.showinfo("Success", "Account created! You can now log in.")
            self.app.show_login()
        else:
            messagebox.showerror("Error", "Failed to create account")

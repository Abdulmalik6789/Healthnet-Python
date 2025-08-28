"""
Signup Page Class
Simple Tkinter Registration Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class SignupPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create signup page widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Center frame with scrollbar
        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Center the signup form
        center_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', bd=2)
        center_frame.pack(pady=50, padx=50)
        
        # Title
        title_label = tk.Label(center_frame, text="Create Account", 
                              font=('Arial', 20, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(center_frame, bg='white')
        form_frame.pack(pady=20, padx=40, fill='both')
        
        # Full Name
        tk.Label(form_frame, text="Full Name:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=(10, 5))
        
        self.fullname_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                      relief='solid', bd=1, bg='#f8f9fa')
        self.fullname_entry.grid(row=0, column=1, padx=(10, 0), pady=(10, 5), ipady=5)
        
        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
        
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                      relief='solid', bd=1, bg='#f8f9fa')
        self.username_entry.grid(row=1, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=2, column=0, sticky='w', pady=5)
        
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*',
                                      relief='solid', bd=1, bg='#f8f9fa')
        self.password_entry.grid(row=2, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Confirm Password
        tk.Label(form_frame, text="Confirm Password:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=3, column=0, sticky='w', pady=5)
        
        self.confirm_password_entry = tk.Entry(form_frame, font=('Arial', 12), width=30, show='*',
                                              relief='solid', bd=1, bg='#f8f9fa')
        self.confirm_password_entry.grid(row=3, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Email
        tk.Label(form_frame, text="Email:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=4, column=0, sticky='w', pady=5)
        
        self.email_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                   relief='solid', bd=1, bg='#f8f9fa')
        self.email_entry.grid(row=4, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=5, column=0, sticky='w', pady=5)
        
        self.phone_entry = tk.Entry(form_frame, font=('Arial', 12), width=30,
                                   relief='solid', bd=1, bg='#f8f9fa')
        self.phone_entry.grid(row=5, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Role
        tk.Label(form_frame, text="Role:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').grid(row=6, column=0, sticky='w', pady=5)
        
        self.role_var = tk.StringVar(value="Patient")
        role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, width=27,
                                 values=["Admin", "Doctor", "Nurse", "Lab", "Patient"],
                                 state="readonly", font=('Arial', 12))
        role_combo.grid(row=6, column=1, padx=(10, 0), pady=5, ipady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(center_frame, bg='white')
        buttons_frame.pack(pady=30, fill='x', padx=40)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="← Back to Login", font=('Arial', 12),
                            bg='#6c757d', fg='white', relief='flat', cursor='hand2',
                            command=self.app.show_login)
        back_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        # Create Account button
        signup_btn = tk.Button(buttons_frame, text="Create Account", font=('Arial', 12, 'bold'),
                              bg='#4CAF50', fg='white', relief='flat', cursor='hand2',
                              command=self.handle_signup)
        signup_btn.pack(side='right', ipady=8, ipadx=15)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Focus on first entry
        self.fullname_entry.focus()
    
    def handle_signup(self):
        """Handle signup form submission"""
        # Get form data
        full_name = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        role = self.role_var.get()
        
        # Validation
        if not all([full_name, username, password, confirm_password]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return
        
        # Create account
        success = self.app.db.create_user(username, password, role, full_name, email, phone)
        if success:
            messagebox.showinfo("Success", 
                              f"Account created successfully!\n\nUsername: {username}\nRole: {role}\n\nYou can now login with your credentials.")
            self.app.show_login()
        else:
            messagebox.showerror("Error", "Failed to create account. Username may already exist.")

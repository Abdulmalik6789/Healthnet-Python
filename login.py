"""
Login Page Class
Simple Tkinter Login Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class LoginPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create login page widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Center frame
        center_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # Title
        title_label = tk.Label(center_frame, text="HealthNet Hospital Management", 
                              font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50')
        title_label.pack(pady=30)
        
        # Logo
        logo_label = tk.Label(center_frame, text="🏥", font=('Arial', 48), bg='white')
        logo_label.pack(pady=10)
        
        # Login form
        form_frame = tk.Frame(center_frame, bg='white')
        form_frame.pack(pady=20, padx=40, fill='x')
        
        # Username
        tk.Label(form_frame, text="Username:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), 
                                      relief='solid', bd=1, bg='#f8f9fa')
        self.username_entry.pack(fill='x', ipady=8, pady=(0, 10))
        
        # Password
        tk.Label(form_frame, text="Password:", font=('Arial', 12, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), show='*',
                                      relief='solid', bd=1, bg='#f8f9fa')
        self.password_entry.pack(fill='x', ipady=8, pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(form_frame, text="Login", font=('Arial', 14, 'bold'),
                             bg='#2196F3', fg='white', relief='flat', cursor='hand2',
                             command=self.handle_login)
        login_btn.pack(fill='x', ipady=10, pady=(0, 10))
        
        # Signup button
        signup_btn = tk.Button(form_frame, text="Create Account", font=('Arial', 12),
                              bg='#4CAF50', fg='white', relief='flat', cursor='hand2',
                              command=self.app.show_signup)
        signup_btn.pack(fill='x', ipady=8)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.handle_login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Authenticate user
        user = self.app.db.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
            self.app.login_user(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)

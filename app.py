"""
HealthNet Hospital Management System
Main Application Entry Point - Simple Tkinter Structure
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Import all page classes
from login import LoginPage
from signup import SignupPage
from dashboard import DashboardPage
from patients import PatientsPage
from doctors import DoctorsPage
from appointments import AppointmentsPage
from staff import StaffPage
from db import Database
from admin import AdminPage
from patientdashboard import PatientDashboard
from doctordashboard import DoctorDashboard


class HealthNetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HealthNet Hospital Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.db = Database()
        self.db.connect()
        self.db.create_tables()
        
        # Current user and page tracking
        self.current_user = None
        self.current_page = None
        
        # Configure styles
        self.setup_styles()
        
        # Start with login page
        self.show_login()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background='#2196F3',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10))
        
        style.configure('Success.TButton',
                       background='#4CAF50',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10))
        
        style.configure('Danger.TButton',
                       background='#f44336',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10))
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        """Show login page"""
        self.clear_window()
        self.current_page = LoginPage(self.root, self)
    
    def show_signup(self):
        """Show signup page"""
        self.clear_window()
        self.current_page = SignupPage(self.root, self)
    
    def show_dashboard(self):
        """Show dashboard page (non-patient users)"""
        if not self.current_user:
            messagebox.showerror("Error", "No user logged in")
            self.show_login()
            return
        
        self.clear_window()
        self.current_page = DashboardPage(self.root, self)
    
    def show_patients(self):
        """Show patients page"""
        if not self.current_user:
            self.show_login()
            return
        self.clear_window()
        self.current_page = PatientsPage(self.root, self)
    
    def show_doctors(self):
        """Show doctors page"""
        if not self.current_user:
            self.show_login()
            return
        self.clear_window()
        self.current_page = DoctorsPage(self.root, self)
    
    def show_appointments(self):
        """Show appointments page"""
        if not self.current_user:
            self.show_login()
            return
        self.clear_window()
        self.current_page = AppointmentsPage(self.root, self)
    
    def show_staff(self):
        """Show staff page"""
        if not self.current_user:
            self.show_login()
            return
        self.clear_window()
        self.current_page = StaffPage(self.root, self)
    
    def show_admin(self):
        """Show admin page"""
        if not self.current_user:
            self.show_login()
            return
        if self.current_user.get('role') != 'Admin':
            messagebox.showerror("Access Denied", "Admin access required")
            return
        self.clear_window()
        self.current_page = AdminPage(self.root, self)
    
    def login_user(self, user):
        """Set current user after successful login"""
        self.current_user = user

        # Route based on role
        if user['role'] == "Patient":
            self.show_patient_dashboard()
        elif user['role'] == "Doctor":
            self.show_doctor_dashboard()
        elif user['role'] == "Admin":
            self.show_admin()
        else:
            self.show_dashboard()

    def show_patient_dashboard(self):
        """Show patient dashboard"""
        if not self.current_user:
            self.show_login()
            return
        if self.current_user.get('role') != 'Patient':
            messagebox.showerror("Access Denied", "Patient access required")
            return
        self.clear_window()
        self.current_page = PatientDashboard(self.root, self, self.current_user)

    def show_doctor_dashboard(self):
        """Show doctor dashboard"""
        if not self.current_user:
            self.show_login()
            return
        if self.current_user.get('role') != 'Doctor':
            messagebox.showerror("Access Denied", "Doctor access required")
            return
        self.clear_window()
        self.current_page = DoctorDashboard(self.root, self, self.current_user)

    def logout_user(self):
        """Logout current user"""
        self.current_user = None
        self.show_login()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = HealthNetApp()
    app.run()

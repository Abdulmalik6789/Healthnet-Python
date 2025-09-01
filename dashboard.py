"""
Dashboard Page Class
Main dashboard after login
"""
import tkinter as tk
from tkinter import ttk, messagebox

class DashboardPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.user = app.current_user
        self.create_widgets()
        self.auto_refresh()  # Start auto-refreshing stats

    def create_widgets(self):
        """Create dashboard widgets"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(header_frame, 
                                text=f"Welcome, {self.user['full_name']} ({self.user['role']})",
                                font=('Arial', 18, 'bold'), bg='#2196F3', fg='white')
        welcome_label.pack(side='left', padx=20, pady=20)
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", font=('Arial', 12, 'bold'),
                              bg='#f44336', fg='white', relief='flat', cursor='hand2',
                              command=self.app.logout_user)
        logout_btn.pack(side='right', padx=20, pady=20, ipady=5, ipadx=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(content_frame, bg='#f0f0f0')
        nav_frame.pack(fill='x', pady=(0, 20))
        self.create_navigation_buttons(nav_frame)
        
        # Stats frame
        stats_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        stats_frame.pack(fill='both', expand=True)
        
        stats_title = tk.Label(stats_frame, text="System Overview", 
                              font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50')
        stats_title.pack(pady=20)
        
        self.stats_grid = tk.Frame(stats_frame, bg='white')  # Keep reference for refresh
        self.stats_grid.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.create_stats_cards(self.stats_grid)

    def create_navigation_buttons(self, parent):
        """Create navigation buttons based on user role"""
        buttons = []
        
        # Common buttons for all roles
        if self.user['role'] in ['Admin', 'Doctor', 'Nurse']:
            buttons.extend([
                ("👥 Patients", self.app.show_patients, '#4CAF50'),
                ("📅 Appointments", self.app.show_appointments, '#FF9800'),
            ])
        
        # Admin-specific buttons
        if self.user['role'] == 'Admin':
            buttons.extend([
                ("👨‍⚕️ Doctors", self.app.show_doctors, '#2196F3'),
                ("👩‍💼 Staff", self.app.show_staff, '#9C27B0'),
                ("⚙️ Admin Panel", self.app.show_admin, '#e74c3c'),
            ])
        
        # Doctor-specific buttons
        if self.user['role'] == 'Doctor':
            buttons.append(("📋 My Schedule", self.show_my_schedule, '#607D8B'))
        
        # Patient-specific buttons
        if self.user['role'] == 'Patient':
            buttons.extend([
                ("📅 My Appointments", self.show_my_appointments, '#FF9800'),
                ("📋 Medical Records", self.show_medical_records, '#795548'),
            ])
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(parent, text=text, font=('Arial', 12, 'bold'),
                           bg=color, fg='white', relief='flat', cursor='hand2',
                           command=command, width=15, height=2)
            btn.grid(row=0, column=i, padx=10, pady=10)

    def create_stats_cards(self, parent):
        """Create statistics cards with live counts"""
        stats = self.get_system_stats()
        
        for i, (title, value, color) in enumerate([
            ("Total Patients", stats.get('patients', 0), '#4CAF50'),
            ("Total Doctors", stats.get('doctors', 0), '#2196F3'),
            ("Today's Appointments", stats.get('appointments_today', 0), '#FF9800'),
            ("Total Staff", stats.get('staff', 0), '#9C27B0'),
        ]):
            card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
            card_frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            parent.grid_columnconfigure(i, weight=1)
            parent.grid_rowconfigure(0, weight=1)
            
            value_label = tk.Label(card_frame, text=str(value), 
                                  font=('Arial', 24, 'bold'), bg=color, fg='white')
            value_label.pack(pady=(20, 5))
            
            title_label = tk.Label(card_frame, text=title, 
                                  font=('Arial', 12), bg=color, fg='white')
            title_label.pack(pady=(0, 20))

    def get_system_stats(self):
        """Get live statistics from database (uses db.py helper methods)"""
        stats = {}
        try:
            stats['patients'] = self.app.db.count_patients()
            stats['doctors'] = self.app.db.count_doctors()
            stats['staff'] = self.app.db.count_staff()
            stats['appointments_today'] = self.app.db.count_todays_appointments()
        except Exception as e:
            print(f"Error fetching system stats: {e}")
        return stats

    def refresh_stats(self):
        """Refresh the stats cards with latest counts"""
        for widget in self.stats_grid.winfo_children():
            widget.destroy()
        self.create_stats_cards(self.stats_grid)

    def auto_refresh(self, interval=5000):
        """Automatically refresh stats every interval (ms)"""
        self.refresh_stats()
        self.root.after(interval, self.auto_refresh)

    # ---------------- Extra functions ----------------
    def show_my_schedule(self):
        """Show doctor's schedule count"""
        try:
            count = self.app.db.cursor.execute(
                "SELECT COUNT(*) as count FROM appointments WHERE doctor_id=%s", 
                (self.user['id'],)
            )
            result = self.app.db.cursor.fetchone()
            count = result['count'] if result else 0
            messagebox.showinfo("My Schedule", f"You have {count} appointments scheduled.")
        except:
            messagebox.showinfo("My Schedule", "No appointments found.")

    def show_my_appointments(self):
        """Show patient's appointment count"""
        try:
            self.app.db.cursor.execute(
                "SELECT COUNT(*) as count FROM appointments WHERE patient_id=%s", 
                (self.user['id'],)
            )
            result = self.app.db.cursor.fetchone()
            count = result['count'] if result else 0
            messagebox.showinfo("My Appointments", f"You have {count} upcoming appointments.")
        except:
            messagebox.showinfo("My Appointments", "No appointments found.")

    def show_medical_records(self):
        """Show patient's medical record count"""
        try:
            self.app.db.cursor.execute(
                "SELECT COUNT(*) as count FROM medical_records WHERE patient_id=%s", 
                (self.user['id'],)
            )
            result = self.app.db.cursor.fetchone()
            count = result['count'] if result else 0
            messagebox.showinfo("Medical Records", f"You have {count} medical records available.")
        except:
            messagebox.showinfo("Medical Records", "No medical records found.")

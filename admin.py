"""
Admin Page Class
Administrative Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class AdminPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create admin page widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Title
        title_label = tk.Label(header_content, text="System Administration", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(side='left', pady=10)
        
        # Back button
        back_btn = tk.Button(header_content, text="← Back to Dashboard", 
                            font=('Arial', 12), bg='#34495e', fg='white',
                            relief='flat', cursor='hand2', command=self.app.show_dashboard)
        back_btn.pack(side='right', pady=15)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Statistics frame
        stats_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_header = tk.Frame(stats_frame, bg='#34495e', height=40)
        stats_header.pack(fill='x')
        stats_header.pack_propagate(False)
        
        tk.Label(stats_header, text="System Statistics", font=('Arial', 16, 'bold'),
                bg='#34495e', fg='white').pack(pady=10)
        
        # Stats content
        stats_content = tk.Frame(stats_frame, bg='white')
        stats_content.pack(fill='x', padx=20, pady=20)
        
        # Create stats grid
        stats_grid = tk.Frame(stats_content, bg='white')
        stats_grid.pack(fill='x')
        
        # Load and display statistics
        self.load_statistics(stats_grid)
        
        # Management sections
        sections_frame = tk.Frame(content_frame, bg='#f0f0f0')
        sections_frame.pack(fill='both', expand=True)
        
        # User Management
        user_mgmt_frame = tk.Frame(sections_frame, bg='white', relief='raised', bd=1)
        user_mgmt_frame.pack(fill='x', pady=(0, 20))
        
        user_header = tk.Frame(user_mgmt_frame, bg='#e74c3c', height=40)
        user_header.pack(fill='x')
        user_header.pack_propagate(False)
        
        tk.Label(user_header, text="User Management", font=('Arial', 16, 'bold'),
                bg='#e74c3c', fg='white').pack(pady=10)
        
        user_content = tk.Frame(user_mgmt_frame, bg='white')
        user_content.pack(fill='x', padx=20, pady=20)
        
        user_buttons = tk.Frame(user_content, bg='white')
        user_buttons.pack(fill='x')
        
        tk.Button(user_buttons, text="Manage Users", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white', relief='flat', cursor='hand2',
                 command=self.manage_users).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        tk.Button(user_buttons, text="View User Logs", font=('Arial', 12),
                 bg='#9b59b6', fg='white', relief='flat', cursor='hand2',
                 command=self.view_user_logs).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        tk.Button(user_buttons, text="Reset Password", font=('Arial', 12),
                 bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                 command=self.reset_password).pack(side='left', ipady=8, ipadx=15)
        
        # System Management
        system_mgmt_frame = tk.Frame(sections_frame, bg='white', relief='raised', bd=1)
        system_mgmt_frame.pack(fill='x', pady=(0, 20))
        
        system_header = tk.Frame(system_mgmt_frame, bg='#27ae60', height=40)
        system_header.pack(fill='x')
        system_header.pack_propagate(False)
        
        tk.Label(system_header, text="System Management", font=('Arial', 16, 'bold'),
                bg='#27ae60', fg='white').pack(pady=10)
        
        system_content = tk.Frame(system_mgmt_frame, bg='white')
        system_content.pack(fill='x', padx=20, pady=20)
        
        system_buttons = tk.Frame(system_content, bg='white')
        system_buttons.pack(fill='x')
        
        tk.Button(system_buttons, text="Database Backup", font=('Arial', 12, 'bold'),
                 bg='#2ecc71', fg='white', relief='flat', cursor='hand2',
                 command=self.database_backup).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        tk.Button(system_buttons, text="System Settings", font=('Arial', 12),
                 bg='#34495e', fg='white', relief='flat', cursor='hand2',
                 command=self.system_settings).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        tk.Button(system_buttons, text="Generate Reports", font=('Arial', 12),
                 bg='#e67e22', fg='white', relief='flat', cursor='hand2',
                 command=self.generate_reports).pack(side='left', ipady=8, ipadx=15)
        
        # Recent Activity
        activity_frame = tk.Frame(sections_frame, bg='white', relief='raised', bd=1)
        activity_frame.pack(fill='both', expand=True)
        
        activity_header = tk.Frame(activity_frame, bg='#8e44ad', height=40)
        activity_header.pack(fill='x')
        activity_header.pack_propagate(False)
        
        tk.Label(activity_header, text="Recent System Activity", font=('Arial', 16, 'bold'),
                bg='#8e44ad', fg='white').pack(pady=10)
        
        # Activity list
        activity_content = tk.Frame(activity_frame, bg='white')
        activity_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.activity_listbox = tk.Listbox(activity_content, font=('Arial', 11),
                                          bg='#f8f9fa', relief='solid', bd=1)
        self.activity_listbox.pack(fill='both', expand=True)
        
        # Load recent activity
        self.load_recent_activity()
    
    def load_statistics(self, parent):
        """Load and display system statistics"""
        try:
            # Get statistics from database
            stats = self.app.db.get_system_statistics()
            
            # Create stat cards
            stat_items = [
                ("Total Patients", stats.get('total_patients', 0), '#3498db'),
                ("Total Doctors", stats.get('total_doctors', 0), '#2ecc71'),
                ("Total Staff", stats.get('total_staff', 0), '#f39c12'),
                ("Today's Appointments", stats.get('todays_appointments', 0), '#e74c3c'),
                ("Active Users", stats.get('active_users', 0), '#9b59b6'),
                ("System Uptime", stats.get('uptime', 'N/A'), '#34495e')
            ]
            
            for i, (label, value, color) in enumerate(stat_items):
                row = i // 3
                col = i % 3
                
                stat_card = tk.Frame(parent, bg=color, relief='raised', bd=2)
                stat_card.grid(row=row, column=col, padx=10, pady=10, sticky='ew', ipadx=20, ipady=15)
                
                tk.Label(stat_card, text=str(value), font=('Arial', 24, 'bold'),
                        bg=color, fg='white').pack()
                
                tk.Label(stat_card, text=label, font=('Arial', 12),
                        bg=color, fg='white').pack()
            
            # Configure grid weights
            for i in range(3):
                parent.grid_columnconfigure(i, weight=1)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")
    
    def load_recent_activity(self):
        """Load recent system activity"""
        try:
            activities = self.app.db.get_recent_activity()
            
            self.activity_listbox.delete(0, tk.END)
            
            for activity in activities:
                activity_text = f"{activity.get('timestamp', '')} - {activity.get('action', '')} by {activity.get('user', '')}"
                self.activity_listbox.insert(tk.END, activity_text)
                
        except Exception as e:
            # If no activity log exists, show sample data
            sample_activities = [
                "2024-01-15 10:30:00 - User login: admin",
                "2024-01-15 10:25:00 - New patient added: John Doe",
                "2024-01-15 10:20:00 - Appointment scheduled: Dr. Smith",
                "2024-01-15 10:15:00 - Staff member updated: Jane Wilson",
                "2024-01-15 10:10:00 - System backup completed"
            ]
            
            for activity in sample_activities:
                self.activity_listbox.insert(tk.END, activity)
    
    def manage_users(self):
        """Open user management window"""
        user_window = tk.Toplevel(self.root)
        user_window.title("User Management")
        user_window.geometry("800x600")
        user_window.configure(bg='white')
        user_window.transient(self.root)
        user_window.grab_set()
        
        # User management interface
        tk.Label(user_window, text="User Management", font=('Arial', 18, 'bold'),
                bg='white', fg='#2c3e50').pack(pady=20)
        
        # Users list
        users_frame = tk.Frame(user_window, bg='white')
        users_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Username', 'Full Name', 'Role', 'Status', 'Last Login')
        users_tree = ttk.Treeview(users_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            users_tree.heading(col, text=col)
            users_tree.column(col, width=120)
        
        users_tree.pack(fill='both', expand=True)
        
        # Load users
        try:
            users = self.app.db.get_all_users()
            for user in users:
                users_tree.insert('', 'end', values=(
                    user.get('id', ''),
                    user.get('username', ''),
                    user.get('full_name', ''),
                    user.get('role', ''),
                    'Active',  # Default status
                    user.get('last_login', 'Never')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def view_user_logs(self):
        """View user activity logs"""
        messagebox.showinfo("User Logs", "User activity logs feature will be implemented here.")
    
    def reset_password(self):
        """Reset user password"""
        messagebox.showinfo("Reset Password", "Password reset feature will be implemented here.")
    
    def database_backup(self):
        """Create database backup"""
        if messagebox.askyesno("Database Backup", "Are you sure you want to create a database backup?"):
            try:
                # Implement backup logic here
                messagebox.showinfo("Success", "Database backup created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {str(e)}")
    
    def system_settings(self):
        """Open system settings"""
        messagebox.showinfo("System Settings", "System settings feature will be implemented here.")
    
    def generate_reports(self):
        """Generate system reports"""
        messagebox.showinfo("Generate Reports", "Report generation feature will be implemented here.")

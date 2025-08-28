"""
Staff Page Class
Staff Management Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class StaffPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create staff page widgets"""
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
        title_label = tk.Label(header_content, text="Staff Management", 
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
        
        # Control panel
        control_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        control_frame.pack(fill='x', pady=(0, 20))
        
        control_inner = tk.Frame(control_frame, bg='white')
        control_inner.pack(fill='x', padx=20, pady=15)
        
        # Search frame
        search_frame = tk.Frame(control_inner, bg='white')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search Staff:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30,
                                    relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', relief='flat', cursor='hand2',
                              command=self.search_staff)
        search_btn.pack(side='left', padx=(10, 0), ipady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(control_inner, bg='white')
        buttons_frame.pack(fill='x')
        
        add_btn = tk.Button(buttons_frame, text="Add New Staff", font=('Arial', 12, 'bold'),
                           bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                           command=self.add_staff)
        add_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        edit_btn = tk.Button(buttons_frame, text="Edit Staff", font=('Arial', 12),
                            bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                            command=self.edit_staff)
        edit_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        delete_btn = tk.Button(buttons_frame, text="Delete Staff", font=('Arial', 12),
                              bg='#e74c3c', fg='white', relief='flat', cursor='hand2',
                              command=self.delete_staff)
        delete_btn.pack(side='left', ipady=8, ipadx=15)
        
        # Staff table
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Table header
        table_header = tk.Frame(table_frame, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(table_header, text="Staff List", font=('Arial', 16, 'bold'),
                bg='#34495e', fg='white').pack(pady=10)
        
        # Treeview for staff
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Name', 'Role', 'Department', 'Phone', 'Email', 'Hire Date', 'Salary')
        self.staff_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=120, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.staff_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.staff_tree.xview)
        self.staff_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.staff_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load staff data
        self.load_staff()
    
    def load_staff(self):
        """Load staff from database"""
        try:
            staff_members = self.app.db.get_all_staff()
            
            # Clear existing data
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)
            
            # Insert staff data
            for staff in staff_members:
                self.staff_tree.insert('', 'end', values=(
                    staff.get('id', ''),
                    staff.get('full_name', ''),
                    staff.get('role', ''),
                    staff.get('department', ''),
                    staff.get('phone', ''),
                    staff.get('email', ''),
                    staff.get('hire_date', ''),
                    staff.get('salary', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load staff: {str(e)}")
    
    def search_staff(self):
        """Search staff by name or role"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_staff()
            return
        
        try:
            staff_members = self.app.db.search_staff(search_term)
            
            # Clear existing data
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)
            
            # Insert search results
            for staff in staff_members:
                self.staff_tree.insert('', 'end', values=(
                    staff.get('id', ''),
                    staff.get('full_name', ''),
                    staff.get('role', ''),
                    staff.get('department', ''),
                    staff.get('phone', ''),
                    staff.get('email', ''),
                    staff.get('hire_date', ''),
                    staff.get('salary', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def add_staff(self):
        """Add new staff member"""
        self.staff_form_window("Add New Staff Member")
    
    def edit_staff(self):
        """Edit selected staff member"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to edit")
            return
        
        staff_data = self.staff_tree.item(selected[0])['values']
        self.staff_form_window("Edit Staff Member", staff_data)
    
    def delete_staff(self):
        """Delete selected staff member"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return
        
        staff_data = self.staff_tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete staff member '{staff_data[1]}'?"):
            try:
                self.app.db.delete_staff(staff_data[0])
                messagebox.showinfo("Success", "Staff member deleted successfully")
                self.load_staff()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete staff member: {str(e)}")
    
    def staff_form_window(self, title, staff_data=None):
        """Open staff form window"""
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("500x700")
        form_window.configure(bg='white')
        form_window.transient(self.root)
        form_window.grab_set()
        
        # Form frame
        form_frame = tk.Frame(form_window, bg='white')
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title
        tk.Label(form_frame, text=title, font=('Arial', 18, 'bold'),
                bg='white', fg='#2c3e50').pack(pady=(0, 20))
        
        # Form fields
        fields = {}
        field_names = ['full_name', 'role', 'department', 'phone', 'email', 'hire_date', 'salary']
        field_labels = ['Full Name', 'Role', 'Department', 'Phone', 'Email', 'Hire Date (YYYY-MM-DD)', 'Salary']
        
        for i, (field, label) in enumerate(zip(field_names, field_labels)):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 12, 'bold'),
                    bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
            
            if field == 'role':
                fields[field] = ttk.Combobox(form_frame, font=('Arial', 12), 
                                           values=['Nurse', 'Lab Technician', 'Receptionist', 'Administrator', 
                                                  'Pharmacist', 'Cleaner', 'Security', 'IT Support'], 
                                           state='readonly')
            elif field == 'department':
                fields[field] = ttk.Combobox(form_frame, font=('Arial', 12), 
                                           values=['Emergency', 'ICU', 'Surgery', 'Pediatrics', 'Cardiology',
                                                  'Neurology', 'Orthopedics', 'Laboratory', 'Pharmacy', 
                                                  'Administration', 'IT', 'Security'], 
                                           state='readonly')
            else:
                fields[field] = tk.Entry(form_frame, font=('Arial', 12),
                                       relief='solid', bd=1)
            
            fields[field].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Pre-fill data if editing
        if staff_data:
            field_values = staff_data[1:]  # Skip ID
            for field, value in zip(field_names, field_values):
                if hasattr(fields[field], 'set'):
                    fields[field].set(str(value))
                else:
                    fields[field].insert(0, str(value))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = tk.Button(button_frame, text="Save", font=('Arial', 12, 'bold'),
                            bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                            command=lambda: self.save_staff(form_window, fields, staff_data))
        save_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                              command=form_window.destroy)
        cancel_btn.pack(side='left', ipady=8, ipadx=20)
    
    def save_staff(self, window, fields, staff_data=None):
        """Save staff data"""
        try:
            # Get form data
            data = {}
            for field, widget in fields.items():
                data[field] = widget.get().strip()
            
            # Validate required fields
            required_fields = ['full_name', 'role', 'department', 'phone', 'email']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                    return
            
            # Save to database
            if staff_data:  # Edit existing
                data['id'] = staff_data[0]
                self.app.db.update_staff(data)
                messagebox.showinfo("Success", "Staff member updated successfully")
            else:  # Add new
                self.app.db.add_staff(data)
                messagebox.showinfo("Success", "Staff member added successfully")
            
            window.destroy()
            self.load_staff()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save staff member: {str(e)}")

"""
Doctors Page Class
Doctor Management Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox

class DoctorsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create doctors page widgets"""
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
        title_label = tk.Label(header_content, text="Doctor Management", 
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
        
        tk.Label(search_frame, text="Search Doctors:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30,
                                    relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', relief='flat', cursor='hand2',
                              command=self.search_doctors)
        search_btn.pack(side='left', padx=(10, 0), ipady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(control_inner, bg='white')
        buttons_frame.pack(fill='x')
        
        add_btn = tk.Button(buttons_frame, text="Add New Doctor", font=('Arial', 12, 'bold'),
                           bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                           command=self.add_doctor)
        add_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        edit_btn = tk.Button(buttons_frame, text="Edit Doctor", font=('Arial', 12),
                            bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                            command=self.edit_doctor)
        edit_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        delete_btn = tk.Button(buttons_frame, text="Delete Doctor", font=('Arial', 12),
                              bg='#e74c3c', fg='white', relief='flat', cursor='hand2',
                              command=self.delete_doctor)
        delete_btn.pack(side='left', ipady=8, ipadx=15)
        
        # Doctors table
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Table header
        table_header = tk.Frame(table_frame, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(table_header, text="Doctors List", font=('Arial', 16, 'bold'),
                bg='#34495e', fg='white').pack(pady=10)
        
        # Treeview for doctors
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Name', 'Specialization', 'Phone', 'Email', 'Experience', 'Schedule')
        self.doctors_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.doctors_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.doctors_tree.xview)
        self.doctors_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.doctors_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load doctors data
        self.load_doctors()
    
    def load_doctors(self):
        """Load doctors from database"""
        try:
            doctors = self.app.db.get_all_doctors()
            
            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)
            
            # Insert doctors data
            for doctor in doctors:
                self.doctors_tree.insert('', 'end', values=(
                    doctor.get('id', ''),
                    doctor.get('full_name', ''),
                    doctor.get('specialization', ''),
                    doctor.get('phone', ''),
                    doctor.get('email', ''),
                    doctor.get('experience_years', ''),
                    doctor.get('schedule', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")
    
    def search_doctors(self):
        """Search doctors by name or specialization"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_doctors()
            return
        
        try:
            doctors = self.app.db.search_doctors(search_term)
            
            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)
            
            # Insert search results
            for doctor in doctors:
                self.doctors_tree.insert('', 'end', values=(
                    doctor.get('id', ''),
                    doctor.get('full_name', ''),
                    doctor.get('specialization', ''),
                    doctor.get('phone', ''),
                    doctor.get('email', ''),
                    doctor.get('experience_years', ''),
                    doctor.get('schedule', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def add_doctor(self):
        """Add new doctor"""
        self.doctor_form_window("Add New Doctor")
    
    def edit_doctor(self):
        """Edit selected doctor"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to edit")
            return
        
        doctor_data = self.doctors_tree.item(selected[0])['values']
        self.doctor_form_window("Edit Doctor", doctor_data)
    
    def delete_doctor(self):
        """Delete selected doctor"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        doctor_data = self.doctors_tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete doctor '{doctor_data[1]}'?"):
            try:
                self.app.db.delete_doctor(doctor_data[0])
                messagebox.showinfo("Success", "Doctor deleted successfully")
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {str(e)}")
    
    def doctor_form_window(self, title, doctor_data=None):
        """Open doctor form window"""
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("500x600")
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
        field_names = ['full_name', 'specialization', 'phone', 'email', 'experience_years', 'schedule']
        field_labels = ['Full Name', 'Specialization', 'Phone', 'Email', 'Experience (Years)', 'Schedule']
        
        for i, (field, label) in enumerate(zip(field_names, field_labels)):
            tk.Label(form_frame, text=f"{label}:", font=('Arial', 12, 'bold'),
                    bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
            
            if field == 'specialization':
                fields[field] = ttk.Combobox(form_frame, font=('Arial', 12), 
                                           values=['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 
                                                  'Dermatology', 'Psychiatry', 'General Medicine', 'Surgery'], 
                                           state='readonly')
            elif field == 'schedule':
                fields[field] = tk.Text(form_frame, font=('Arial', 12), height=4,
                                      relief='solid', bd=1)
            else:
                fields[field] = tk.Entry(form_frame, font=('Arial', 12),
                                       relief='solid', bd=1)
            
            if field == 'schedule':
                fields[field].pack(fill='x', pady=(0, 10))
            else:
                fields[field].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Pre-fill data if editing
        if doctor_data:
            field_values = doctor_data[1:]  # Skip ID
            for field, value in zip(field_names, field_values):
                if field == 'schedule':
                    fields[field].insert('1.0', str(value))
                else:
                    if hasattr(fields[field], 'set'):
                        fields[field].set(str(value))
                    else:
                        fields[field].insert(0, str(value))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = tk.Button(button_frame, text="Save", font=('Arial', 12, 'bold'),
                            bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                            command=lambda: self.save_doctor(form_window, fields, doctor_data))
        save_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                              command=form_window.destroy)
        cancel_btn.pack(side='left', ipady=8, ipadx=20)
    
    def save_doctor(self, window, fields, doctor_data=None):
        """Save doctor data"""
        try:
            # Get form data
            data = {}
            for field, widget in fields.items():
                if field == 'schedule':
                    data[field] = widget.get('1.0', tk.END).strip()
                else:
                    data[field] = widget.get().strip()
            
            # Validate required fields
            required_fields = ['full_name', 'specialization', 'phone', 'email']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                    return
            
            # Save to database
            if doctor_data:  # Edit existing
                data['id'] = doctor_data[0]
                self.app.db.update_doctor(data)
                messagebox.showinfo("Success", "Doctor updated successfully")
            else:  # Add new
                self.app.db.add_doctor(data)
                messagebox.showinfo("Success", "Doctor added successfully")
            
            window.destroy()
            self.load_doctors()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save doctor: {str(e)}")

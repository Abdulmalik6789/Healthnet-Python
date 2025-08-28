"""
Appointments Page Class
Appointment Management Interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

class AppointmentsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create appointments page widgets"""
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
        title_label = tk.Label(header_content, text="Appointment Management", 
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
        
        tk.Label(search_frame, text="Search Appointments:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30,
                                    relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', relief='flat', cursor='hand2',
                              command=self.search_appointments)
        search_btn.pack(side='left', padx=(10, 0), ipady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(control_inner, bg='white')
        buttons_frame.pack(fill='x')
        
        add_btn = tk.Button(buttons_frame, text="Schedule Appointment", font=('Arial', 12, 'bold'),
                           bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                           command=self.add_appointment)
        add_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        edit_btn = tk.Button(buttons_frame, text="Edit Appointment", font=('Arial', 12),
                            bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                            command=self.edit_appointment)
        edit_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel Appointment", font=('Arial', 12),
                              bg='#e74c3c', fg='white', relief='flat', cursor='hand2',
                              command=self.cancel_appointment)
        cancel_btn.pack(side='left', ipady=8, ipadx=15)
        
        # Appointments table
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        # Table header
        table_header = tk.Frame(table_frame, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(table_header, text="Appointments List", font=('Arial', 16, 'bold'),
                bg='#34495e', fg='white').pack(pady=10)
        
        # Treeview for appointments
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status', 'Notes')
        self.appointments_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.appointments_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.appointments_tree.xview)
        self.appointments_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Load appointments data
        self.load_appointments()
    
    def load_appointments(self):
        """Load appointments from database"""
        try:
            appointments = self.app.db.get_all_appointments()
            
            # Clear existing data
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)
            
            # Insert appointments data
            for appointment in appointments:
                self.appointments_tree.insert('', 'end', values=(
                    appointment.get('id', ''),
                    appointment.get('patient_name', ''),
                    appointment.get('doctor_name', ''),
                    appointment.get('appointment_date', ''),
                    appointment.get('appointment_time', ''),
                    appointment.get('status', ''),
                    appointment.get('notes', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")
    
    def search_appointments(self):
        """Search appointments by patient or doctor name"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_appointments()
            return
        
        try:
            appointments = self.app.db.search_appointments(search_term)
            
            # Clear existing data
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)
            
            # Insert search results
            for appointment in appointments:
                self.appointments_tree.insert('', 'end', values=(
                    appointment.get('id', ''),
                    appointment.get('patient_name', ''),
                    appointment.get('doctor_name', ''),
                    appointment.get('appointment_date', ''),
                    appointment.get('appointment_time', ''),
                    appointment.get('status', ''),
                    appointment.get('notes', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def add_appointment(self):
        """Add new appointment"""
        self.appointment_form_window("Schedule New Appointment")
    
    def edit_appointment(self):
        """Edit selected appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to edit")
            return
        
        appointment_data = self.appointments_tree.item(selected[0])['values']
        self.appointment_form_window("Edit Appointment", appointment_data)
    
    def cancel_appointment(self):
        """Cancel selected appointment"""
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        appointment_data = self.appointments_tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel this appointment?"):
            try:
                self.app.db.update_appointment_status(appointment_data[0], 'Cancelled')
                messagebox.showinfo("Success", "Appointment cancelled successfully")
                self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")
    
    def appointment_form_window(self, title, appointment_data=None):
        """Open appointment form window"""
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
        
        # Patient selection
        tk.Label(form_frame, text="Patient:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['patient'] = ttk.Combobox(form_frame, font=('Arial', 12), state='readonly')
        fields['patient'].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Doctor selection
        tk.Label(form_frame, text="Doctor:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['doctor'] = ttk.Combobox(form_frame, font=('Arial', 12), state='readonly')
        fields['doctor'].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Date
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['date'] = tk.Entry(form_frame, font=('Arial', 12), relief='solid', bd=1)
        fields['date'].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Time
        tk.Label(form_frame, text="Time (HH:MM):", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['time'] = tk.Entry(form_frame, font=('Arial', 12), relief='solid', bd=1)
        fields['time'].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Status
        tk.Label(form_frame, text="Status:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['status'] = ttk.Combobox(form_frame, font=('Arial', 12), 
                                       values=['Scheduled', 'Confirmed', 'Completed', 'Cancelled'], 
                                       state='readonly')
        fields['status'].pack(fill='x', ipady=8, pady=(0, 10))
        
        # Notes
        tk.Label(form_frame, text="Notes:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        fields['notes'] = tk.Text(form_frame, font=('Arial', 12), height=4, relief='solid', bd=1)
        fields['notes'].pack(fill='x', pady=(0, 10))
        
        # Load patients and doctors
        try:
            patients = self.app.db.get_all_patients()
            patient_names = [f"{p['id']} - {p['full_name']}" for p in patients]
            fields['patient']['values'] = patient_names
            
            doctors = self.app.db.get_all_doctors()
            doctor_names = [f"{d['id']} - {d['full_name']}" for d in doctors]
            fields['doctor']['values'] = doctor_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        
        # Pre-fill data if editing
        if appointment_data:
            # This would need more complex logic to match patient/doctor names
            fields['date'].insert(0, str(appointment_data[3]))
            fields['time'].insert(0, str(appointment_data[4]))
            if hasattr(fields['status'], 'set'):
                fields['status'].set(str(appointment_data[5]))
            fields['notes'].insert('1.0', str(appointment_data[6]))
        else:
            # Set default values for new appointment
            fields['date'].insert(0, date.today().strftime('%Y-%m-%d'))
            fields['status'].set('Scheduled')
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = tk.Button(button_frame, text="Save", font=('Arial', 12, 'bold'),
                            bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                            command=lambda: self.save_appointment(form_window, fields, appointment_data))
        save_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=20)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Arial', 12),
                              bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                              command=form_window.destroy)
        cancel_btn.pack(side='left', ipady=8, ipadx=20)
    
    def save_appointment(self, window, fields, appointment_data=None):
        """Save appointment data"""
        try:
            # Get form data
            data = {}
            
            # Extract patient and doctor IDs
            patient_selection = fields['patient'].get()
            doctor_selection = fields['doctor'].get()
            
            if not patient_selection or not doctor_selection:
                messagebox.showerror("Error", "Please select both patient and doctor")
                return
            
            data['patient_id'] = patient_selection.split(' - ')[0]
            data['doctor_id'] = doctor_selection.split(' - ')[0]
            data['appointment_date'] = fields['date'].get().strip()
            data['appointment_time'] = fields['time'].get().strip()
            data['status'] = fields['status'].get().strip()
            data['notes'] = fields['notes'].get('1.0', tk.END).strip()
            
            # Validate required fields
            required_fields = ['patient_id', 'doctor_id', 'appointment_date', 'appointment_time', 'status']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"Please fill in {field.replace('_', ' ').title()}")
                    return
            
            # Save to database
            if appointment_data:  # Edit existing
                data['id'] = appointment_data[0]
                self.app.db.update_appointment(data)
                messagebox.showinfo("Success", "Appointment updated successfully")
            else:  # Add new
                self.app.db.add_appointment(data)
                messagebox.showinfo("Success", "Appointment scheduled successfully")
            
            window.destroy()
            self.load_appointments()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save appointment: {str(e)}")

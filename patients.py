
import tkinter as tk
from tkinter import ttk, messagebox

class PatientsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create patients page widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Patient Management", 
                              font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(side='left', padx=20, pady=20)
        
        back_btn = tk.Button(header_frame, text="← Back to Dashboard", 
                            font=('Arial', 12), bg='#34495e', fg='white',
                            relief='flat', cursor='hand2', command=self.app.show_dashboard)
        back_btn.pack(side='right', padx=20, pady=20)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Control panel
        control_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        control_frame.pack(fill='x', pady=(0, 20))
        
        control_inner = tk.Frame(control_frame, bg='white')
        control_inner.pack(fill='x', padx=20, pady=15)
        
        # Search
        search_frame = tk.Frame(control_inner, bg='white')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search Patients:", font=('Arial', 12, 'bold'),
                bg='white', fg='#2c3e50').pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30,
                                    relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)
        
        search_btn = tk.Button(search_frame, text="Search", font=('Arial', 10),
                              bg='#3498db', fg='white', relief='flat', cursor='hand2',
                              command=self.search_patients)
        search_btn.pack(side='left', padx=(10, 0), ipady=5)
        
        # Buttons
        buttons_frame = tk.Frame(control_inner, bg='white')
        buttons_frame.pack(fill='x')
        
        add_btn = tk.Button(buttons_frame, text="Add New Patient", font=('Arial', 12, 'bold'),
                           bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                           command=self.add_patient)
        add_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        edit_btn = tk.Button(buttons_frame, text="Edit Patient", font=('Arial', 12),
                            bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                            command=self.edit_patient)
        edit_btn.pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        
        delete_btn = tk.Button(buttons_frame, text="Delete Patient", font=('Arial', 12),
                              bg='#e74c3c', fg='white', relief='flat', cursor='hand2',
                              command=self.delete_patient)
        delete_btn.pack(side='left', ipady=8, ipadx=15)
        
        # Table
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True)
        
        table_header = tk.Frame(table_frame, bg='#34495e', height=40)
        table_header.pack(fill='x')
        table_header.pack_propagate(False)
        
        tk.Label(table_header, text="Patients List", font=('Arial', 16, 'bold'),
                bg='#34495e', fg='white').pack(pady=10)
        
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = (
            'ID', 'Name', 'Age', 'Gender', 'Phone', 'Email', 
            'Address', 'Medical History', 'Emergency Contact', 'Emergency Phone'
        )
        self.patients_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120, minwidth=80)
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.patients_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.patients_tree.xview)
        self.patients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        self.load_patients()
    
    # ------------------- Database actions -------------------
    def load_patients(self):
        for row in self.patients_tree.get_children():
            self.patients_tree.delete(row)

        patients = self.db.get_all_patients()
        if patients:
            for patient in patients:
                self.tree.insert("", "end", values=patient)

        self.patients_tree.delete(*self.patients_tree.get_children())
        for patient in patients:
            self.patients_tree.insert('', 'end', values=(
                patient.get('id', ''),
                patient.get('full_name', ''),
                patient.get('age', ''),
                patient.get('gender', ''),
                patient.get('phone', ''),
                patient.get('email', ''),
                patient.get('address', ''),
                patient.get('medical_history', ''),
                patient.get('emergency_contact', ''),
                patient.get('emergency_phone', '')
            ))
    
    def search_patients(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_patients()
            return
        try:
            patients = self.app.db.search_patients(search_term)
            self.patients_tree.delete(*self.patients_tree.get_children())
            for patient in patients:
                self.patients_tree.insert('', 'end', values=(
                    patient.get('id', ''),
                    patient.get('full_name', ''),
                    patient.get('age', ''),
                    patient.get('gender', ''),
                    patient.get('phone', ''),
                    patient.get('email', ''),
                    patient.get('address', ''),
                    patient.get('medical_history', ''),
                    patient.get('emergency_contact', ''),
                    patient.get('emergency_phone', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def add_patient(self):
        self.patient_form_window("Add New Patient")
    
    def edit_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to edit")
            return
        patient_data = self.patients_tree.item(selected[0])['values']
        self.patient_form_window("Edit Patient", patient_data)
    
    def delete_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        patient_data = self.patients_tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm Delete", f"Delete patient '{patient_data[1]}'?"):
            try:
                self.app.db.delete_patient(patient_data[0])
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
    
   # ------------------- Patient Form -------------------
    def patient_form_window(self, title, patient_data=None):
        """Open patient form window with scrollable form"""
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("800x600")
        form_window.configure(bg="white")
        form_window.transient(self.root)
        form_window.grab_set()

        # ===== Scrollable Frame =====
        container = tk.Frame(form_window, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== Title =====
        tk.Label(scroll_frame, text=title, font=("Arial", 18, "bold"),
                 bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # ===== Form Fields =====
        self.form_fields = {}
        field_names = [
            "full_name", "age", "gender", "phone", "email",
            "address", "medical_history", "emergency_contact", "emergency_phone"
        ]
        field_labels = [
            "Full Name", "Age", "Gender", "Phone", "Email",
            "Address", "Medical History", "Emergency Contact", "Emergency Phone"
        ]

        for field, label in zip(field_names, field_labels):
            tk.Label(scroll_frame, text=f"{label}:", font=("Arial", 12, "bold"),
                     bg="white", fg="#2c3e50").pack(anchor="w", pady=(10, 5))

            if field == "gender":
                self.form_fields[field] = ttk.Combobox(scroll_frame, font=("Arial", 12),
                                             values=["Male", "Female", "Other"], state="readonly")
                self.form_fields[field].pack(fill="x", ipady=5, pady=(0, 10))

            elif field in ("medical_history", "address"):
                self.form_fields[field] = tk.Text(scroll_frame, font=("Arial", 12), height=4,
                                        relief="solid", bd=1, wrap="word")
                self.form_fields[field].pack(fill="x", pady=(0, 10))
            else:
                self.form_fields[field] = tk.Entry(scroll_frame, font=("Arial", 12),
                                        relief="solid", bd=1)
                self.form_fields[field].pack(fill="x", ipady=8, pady=(0, 10))

        # ===== Pre-fill if editing =====
        if patient_data:
            field_values = patient_data[1:]  # skip ID
            for field, value in zip(field_names, field_values):
                if field in ("medical_history", "address"):
                    self.form_fields[field].insert("1.0", str(value))
                else:
                    if hasattr(self.form_fields[field], "set"):
                        self.form_fields[field].set(str(value))
                    else:
                        self.form_fields[field].insert(0, str(value))

        # ===== Buttons =====
        button_frame = tk.Frame(scroll_frame, bg="white")
        button_frame.pack(fill="x", pady=(20, 0))

        save_btn = tk.Button(button_frame, text="Save Patient", font=("Arial", 12, "bold"),
                             bg="#27ae60", fg="white", relief="flat", cursor="hand2",
                             command=lambda: self.save_patient(form_window, patient_data))
        save_btn.pack(side="left", padx=(0, 10), ipady=8, ipadx=20)

        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Arial", 12),
                               bg="#95a5a6", fg="white", relief="flat", cursor="hand2",
                               command=form_window.destroy)
        cancel_btn.pack(side="left", ipady=8, ipadx=20)

    # ------------------- Save Patient -------------------
def save_patient(self, form_window, patient_data=None):
    """Save or update a patient record"""
    try:
        # Collect data from form entries
        data = {field: entry.get() for field, entry in self.entries.items()}

        if patient_data is not None:  # Update existing patient
            success = self.db.update_patient(data)
        else:  # Add new patient
            success = self.db.add_patient(data)

        if success:
            messagebox.showinfo("Success", "Patient saved successfully!")
            form_window.destroy()
            self.load_patients()  # Refresh table after save
        else:
            messagebox.showerror("Error", "Failed to save patient.")

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


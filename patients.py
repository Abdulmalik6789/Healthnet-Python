import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

class PatientsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Patient Management", font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        tk.Button(header_frame, text="← Back to Dashboard", font=('Arial', 12), bg='#34495e', fg='white', relief='flat', cursor='hand2', command=self.app.show_dashboard).pack(side='right', padx=20, pady=20)
        
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
        tk.Label(search_frame, text="Search Patients:", font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(side='left')
        self.search_entry = tk.Entry(search_frame, font=('Arial', 12), width=30, relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)
        tk.Button(search_frame, text="Search", font=('Arial', 10), bg='#3498db', fg='white', relief='flat', cursor='hand2', command=self.search_patients).pack(side='left', padx=(10, 0), ipady=5)
        
        # Buttons
        buttons_frame = tk.Frame(control_inner, bg='white')
        buttons_frame.pack(fill='x')
        tk.Button(buttons_frame, text="Add New Patient", font=('Arial', 12, 'bold'), bg='#27ae60', fg='white', relief='flat', cursor='hand2', command=self.add_patient).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        tk.Button(buttons_frame, text="Edit Patient", font=('Arial', 12), bg='#f39c12', fg='white', relief='flat', cursor='hand2', command=self.edit_patient).pack(side='left', padx=(0, 10), ipady=8, ipadx=15)
        tk.Button(buttons_frame, text="Delete Patient", font=('Arial', 12), bg='#e74c3c', fg='white', relief='flat', cursor='hand2', command=self.delete_patient).pack(side='left', ipady=8, ipadx=15)
        
        # Table
        table_frame = tk.Frame(content_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True)
        tk.Label(table_frame, text="Patients List", font=('Arial', 16, 'bold'), bg='#34495e', fg='white').pack(fill='x')
        
        tree_frame = tk.Frame(table_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        columns = ('ID', 'Name', 'Age', 'DOB', 'Gender', 'Phone', 'Email', 'Address', 'Medical History', 'Emergency Contact')
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
    
    # ----------------- Database Actions -----------------
    def load_patients(self):
        for row in self.patients_tree.get_children():
            self.patients_tree.delete(row)
        patients = self.app.db.get_all_patients()
        for p in patients:
            full_name = f"{p.get('first_name','')} {p.get('last_name','')}"
            # Calculate age if not stored
            dob = p.get('date_of_birth')
            age = p.get('age') or self.calculate_age(dob)
            self.patients_tree.insert('', 'end', values=(
                p.get('id',''),
                full_name,
                age,
                dob,
                p.get('gender',''),
                p.get('phone',''),
                p.get('email',''),
                p.get('address',''),
                p.get('medical_history',''),
                p.get('emergency_contact','')
            ))
    
    def calculate_age(self, dob):
        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d")
            today = datetime.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except:
            return ""
    
    def search_patients(self):
        term = self.search_entry.get().strip()
        if not term:
            self.load_patients()
            return
        patients = self.app.db.search_patients(term)
        self.patients_tree.delete(*self.patients_tree.get_children())
        for p in patients:
            full_name = f"{p.get('first_name','')} {p.get('last_name','')}"
            dob = p.get('date_of_birth')
            age = p.get('age') or self.calculate_age(dob)
            self.patients_tree.insert('', 'end', values=(
                p.get('id',''),
                full_name,
                age,
                dob,
                p.get('gender',''),
                p.get('phone',''),
                p.get('email',''),
                p.get('address',''),
                p.get('medical_history',''),
                p.get('emergency_contact','')
            ))
    
    # ----------------- Add/Edit/Delete -----------------
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
            self.app.db.delete_patient(patient_data[0])
            self.load_patients()
            if hasattr(self.app, "dashboard_page"):
                self.app.dashboard_page.refresh_stats()
    
    # ----------------- Patient Form -----------------
    def patient_form_window(self, title, patient_data=None):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("800x600")
        form_window.configure(bg="white")
        form_window.transient(self.root)
        form_window.grab_set()

        container = tk.Frame(form_window, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text=title, font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Form fields
        self.form_fields = {}
        field_names = ["first_name","last_name", "date_of_birth","age","gender","phone","email","address","medical_history","emergency_contact"]
        field_labels = ["First Name","Last Name", "Date of Birth (YYYY-MM-DD)","Age","Gender","Phone","Email","Address","Medical History","Emergency Contact"]

        for field, label in zip(field_names, field_labels):
            tk.Label(scroll_frame, text=f"{label}:", font=("Arial",12,"bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(10,5))
            if field=="gender":
                self.form_fields[field] = ttk.Combobox(scroll_frame, font=("Arial",12), values=["Male","Female","Other"], state="readonly")
                self.form_fields[field].pack(fill="x", ipady=5, pady=(0,10))
            elif field in ("medical_history","address"):
                self.form_fields[field] = tk.Text(scroll_frame, font=("Arial",12), height=4, relief="solid", bd=1, wrap="word")
                self.form_fields[field].pack(fill="x", pady=(0,10))
            else:
                self.form_fields[field] = tk.Entry(scroll_frame, font=("Arial",12), relief="solid", bd=1)
                self.form_fields[field].pack(fill="x", ipady=8, pady=(0,10))
        
        # Pre-fill for editing
        if patient_data:
            field_values = patient_data[1:]  # Skip ID
            for field, value in zip(field_names, field_values):
                if field in ("medical_history","address"):
                    self.form_fields[field].insert("1.0", str(value))
                else:
                    self.form_fields[field].insert(0, str(value))

        # Buttons
        button_frame = tk.Frame(scroll_frame, bg="white")
        button_frame.pack(fill="x", pady=(20,0))
        tk.Button(button_frame, text="Save Patient", font=("Arial",12,"bold"), bg="#27ae60", fg="white", relief="flat", cursor="hand2",
                  command=lambda: self.save_patient(form_window, patient_data)).pack(side="left", padx=(0,10), ipady=8, ipadx=20)
        tk.Button(button_frame, text="Cancel", font=("Arial",12), bg="#95a5a6", fg="white", relief="flat", cursor="hand2", command=form_window.destroy).pack(side="left", ipady=8, ipadx=20)
    
    # ----------------- Save Patient -----------------
    def save_patient(self, form_window, patient_data=None):
        try:
            data = {}
            for field, widget in self.form_fields.items():
                if isinstance(widget, tk.Text):
                    data[field] = widget.get("1.0","end").strip()
                else:
                    data[field] = widget.get().strip()
            # Auto-calculate age from DOB
            if data.get("date_of_birth"):
                data["age"] = self.calculate_age(data["date_of_birth"])
            # Auto-generate patient_id
            if not patient_data:
                data['patient_id'] = 'PAT' + ''.join(random.choices("0123456789", k=6))
                data['user_id'] = None
                success = self.app.db.add_patient(data)
            else:
                data['patient_id'] = patient_data[0]  # patient_id stored in ID column
                success = self.app.db.update_patient(data)
            if success:
                messagebox.showinfo("Success","Patient saved successfully!")
                form_window.destroy()
                self.load_patients()
                # Refresh dashboard stats if loaded
                if hasattr(self.app, "dashboard_page"):
                    self.app.dashboard_page.refresh_stats()
            else:
                messagebox.showerror("Error","Failed to save patient.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

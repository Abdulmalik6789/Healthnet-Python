import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class AppointmentsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Appointment Management",
                 font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20, pady=20)
        tk.Button(header_frame, text="← Back to Dashboard", font=('Arial', 12),
                  bg='#34495e', fg='white', relief='flat', cursor='hand2',
                  command=self.app.show_dashboard).pack(side='right', padx=20, pady=20)

        # Control Panel
        control_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        control_frame.pack(fill='x', padx=20, pady=10)

        self.search_entry = tk.Entry(control_frame, font=('Arial', 12), width=30, relief='solid', bd=1)
        self.search_entry.pack(side='left', padx=(10, 0), ipady=5)

        tk.Button(control_frame, text="Search", font=('Arial', 10),
                  bg='#3498db', fg='white', relief='flat', cursor='hand2',
                  command=self.search_appointments).pack(side='left', padx=(10, 0))
        tk.Button(control_frame, text="Schedule Appointment", font=('Arial', 12, 'bold'),
                  bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                  command=self.add_appointment).pack(side='left', padx=5)
        tk.Button(control_frame, text="Edit Appointment", font=('Arial', 12),
                  bg='#f39c12', fg='white', relief='flat', cursor='hand2',
                  command=self.edit_appointment).pack(side='left', padx=5)
        tk.Button(control_frame, text="Cancel Appointment", font=('Arial', 12),
                  bg='#e74c3c', fg='white', relief='flat', cursor='hand2',
                  command=self.cancel_appointment).pack(side='left', padx=5)

        # Table
        table_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status', 'Notes')
        self.appointments_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=150, minwidth=100)

        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.appointments_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.appointments_tree.xview)
        self.appointments_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')

        self.load_appointments()

    # ---------------- Load Appointments ----------------
    def load_appointments(self):
        try:
            appointments = self.app.db.get_all_appointments()
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)

            for appt in appointments:
                patient_name = f"{appt['patient_first']} {appt['patient_last']}"
                doctor_name = f"{appt['doctor_first']} {appt['doctor_last']}"
                self.appointments_tree.insert('', 'end', values=(
                    appt['id'],
                    f"{appt['patient_id']} - {patient_name}",
                    f"{appt['doctor_id']} - {doctor_name}",
                    appt.get('appointment_date', ''),
                    appt.get('appointment_time', ''),
                    appt.get('status', ''),
                    appt.get('notes', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- Search ----------------
    def search_appointments(self):
        term = self.search_entry.get().strip()
        if not term:
            self.load_appointments()
            return
        try:
            appointments = self.app.db.search_appointments(term)
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)
            for appt in appointments:
                patient_name = f"{appt['patient_first']} {appt['patient_last']}"
                doctor_name = f"{appt['doctor_first']} {appt['doctor_last']}"
                self.appointments_tree.insert('', 'end', values=(
                    appt['id'], f"{appt['patient_id']} - {patient_name}",
                    f"{appt['doctor_id']} - {doctor_name}",
                    appt.get('appointment_date', ''),
                    appt.get('appointment_time', ''),
                    appt.get('status', ''),
                    appt.get('notes', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- Appointment Actions ----------------
    def add_appointment(self):
        self.appointment_form_window("Schedule New Appointment")

    def edit_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment to edit")
            return
        data = self.appointments_tree.item(selected[0])['values']
        self.appointment_form_window("Edit Appointment", data)

    def cancel_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an appointment to cancel")
            return
        data = self.appointments_tree.item(selected[0])['values']
        if messagebox.askyesno("Confirm Cancel", "Cancel this appointment?"):
            try:
                self.app.db.update_appointment_status(data[0], 'Cancelled')
                messagebox.showinfo("Success", "Appointment cancelled")
                self.load_appointments()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # ---------------- Appointment Form ----------------
    def appointment_form_window(self, title, appointment_data=None):
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("500x500")
        form_window.transient(self.root)
        form_window.grab_set()

        canvas = tk.Canvas(form_window, bg='white')
        scrollbar = ttk.Scrollbar(form_window, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg='white')
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # --- Fields ---
        fields = {}
        tk.Label(scroll_frame, text=title, font=('Arial', 18, 'bold'),
                 bg='white', fg='#2c3e50').pack(pady=10)

        for label, key, widget in [
            ("Patient:", "patient", ttk.Combobox),
            ("Doctor:", "doctor", ttk.Combobox),
            ("Date (YYYY-MM-DD):", "date", tk.Entry),
            ("Time (HH:MM):", "time", tk.Entry),
            ("Status:", "status", ttk.Combobox),
            ("Notes:", "notes", tk.Text)
        ]:
            tk.Label(scroll_frame, text=label, font=('Arial', 12, 'bold'),
                     bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 5))
            if widget == tk.Text:
                fields[key] = widget(scroll_frame, height=4, font=('Arial', 12))
            else:
                fields[key] = widget(scroll_frame, font=('Arial', 12))
            fields[key].pack(fill='x', ipady=8, pady=(0, 10))

        fields['status']['values'] = ['Scheduled', 'Confirmed', 'Completed', 'Cancelled']

        # --- Load Patients and Doctors ---
        try:
            patients = self.app.db.get_all_patients_combobox()
            self.patient_map = {f"{p['id']} - {p['first_name']} {p['last_name']}": p['id'] for p in patients}
            fields['patient']['values'] = list(self.patient_map.keys())

            doctors = self.app.db.get_all_doctors_combobox()
            self.doctor_map = {f"{d['id']} - {d['first_name']} {d['last_name']}": d['id'] for d in doctors}
            fields['doctor']['values'] = list(self.doctor_map.keys())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patients or doctors:\n{e}")

        # --- Prefill for Edit ---
        if appointment_data:
            fields['date'].insert(0, appointment_data[3])
            fields['time'].insert(0, appointment_data[4])
            fields['status'].set(appointment_data[5])
            fields['notes'].insert('1.0', appointment_data[6])

            patient_id = int(str(appointment_data[1]).split(' - ')[0])
            doctor_id = int(str(appointment_data[2]).split(' - ')[0])

            patient_key = next((k for k, v in self.patient_map.items() if v == patient_id), None)
            doctor_key = next((k for k, v in self.doctor_map.items() if v == doctor_id), None)

            if patient_key:
                fields['patient'].set(patient_key)
            if doctor_key:
                fields['doctor'].set(doctor_key)
        else:
            fields['date'].insert(0, date.today().strftime('%Y-%m-%d'))
            fields['status'].set('Scheduled')

        # --- Buttons ---
        btn_frame = tk.Frame(scroll_frame, bg='white')
        btn_frame.pack(fill='x', pady=20)
        tk.Button(btn_frame, text="Save", font=('Arial', 12, 'bold'),
                  bg='#27ae60', fg='white', relief='flat', cursor='hand2',
                  command=lambda: self.save_appointment(form_window, fields, appointment_data)).pack(side='left', padx=10, ipadx=20, ipady=8)
        tk.Button(btn_frame, text="Cancel", font=('Arial', 12),
                  bg='#95a5a6', fg='white', relief='flat', cursor='hand2',
                  command=form_window.destroy).pack(side='left', ipadx=20, ipady=8)

    # ---------------- Save Appointment ----------------
    def save_appointment(self, window, fields, appointment_data=None):
        try:
            patient_selection = fields['patient'].get()
            doctor_selection = fields['doctor'].get()
            if not patient_selection or not doctor_selection:
                messagebox.showerror("Error", "Select patient and doctor")
                return

            patient_id = self.patient_map.get(patient_selection)
            doctor_id = self.doctor_map.get(doctor_selection)
            appointment_date = fields['date'].get().strip()
            appointment_time = fields['time'].get().strip()
            status = fields['status'].get().strip()
            notes = fields['notes'].get('1.0', 'end').strip()

            required_fields = [patient_id, doctor_id, appointment_date, appointment_time, status]
            if any(not f for f in required_fields):
                messagebox.showerror("Error", "Fill all required fields")
                return

            if appointment_data:  # Edit
                data = {
                    'id': appointment_data[0],
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'appointment_date': appointment_date,
                    'appointment_time': appointment_time,
                    'status': status,
                    'notes': notes
                }
                self.app.db.update_appointment(data)
                messagebox.showinfo("Success", "Appointment updated")
            else:  # New
                self.app.db.add_appointment(patient_id, doctor_id, appointment_date, appointment_time, status, notes)
                messagebox.showinfo("Success", "Appointment scheduled")

            window.destroy()
            self.load_appointments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

import tkinter as tk
from tkinter import ttk

class PatientDashboard:
    def __init__(self, root, app, user):
        self.root = root
        self.app = app
        self.user = user
        self.build_ui()

    def build_ui(self):
        # Clear old widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # ---------- Header ----------
        header = tk.Frame(self.root, bg="#2196F3", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text=f"Patient Dashboard - {self.user['full_name']}",
            font=("Arial", 16, "bold"),
            bg="#2196F3", fg="white"
        )
        title.pack(pady=10)

        # ---------- Buttons ----------
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(side="left", fill="y", padx=10, pady=10)

        btn_appointments = tk.Button(
            button_frame, text="📅 View Appointments", width=20, height=2,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
            command=self.view_appointments
        )
        btn_appointments.pack(pady=10)

        btn_doctor = tk.Button(
            button_frame, text="👨‍⚕️ View Doctor", width=20, height=2,
            bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
            command=self.view_doctor
        )
        btn_doctor.pack(pady=10)

        btn_history = tk.Button(
            button_frame, text="📋 Medical History", width=20, height=2,
            bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
            command=self.view_history
        )
        btn_history.pack(pady=10)

        btn_logout = tk.Button(
            button_frame, text="🚪 Logout", width=20, height=2,
            bg="#f44336", fg="white", font=("Arial", 12, "bold"),
            command=self.app.logout_user
        )
        btn_logout.pack(pady=10)

        # ---------- Display Area ----------
        self.display_frame = tk.Frame(self.root, bg="white", relief="groove", bd=2)
        self.display_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def view_appointments(self):
        self.clear_display()
        label = tk.Label(self.display_frame, text="My Appointments", font=("Arial", 14, "bold"), bg="white")
        label.pack(pady=10)
        print("DEBUG - self.user contents:", self.user) 
        appointments = self.app.db.get_patient_appointments(self.user["id"])
        if appointments:
            for a in appointments:
                tk.Label(
                    self.display_frame,
                    text=f"Date: {a['appointment_date']} | Time: {a['appointment_time']}",
                    font=("Arial", 12), bg="white"
                ).pack(anchor="w", padx=20, pady=5)
        else:
            tk.Label(self.display_frame, text="❌ No appointments found", bg="white").pack(pady=10)

    def view_doctor(self):
        self.clear_display()
        label = tk.Label(self.display_frame, text="Doctor In Charge", font=("Arial", 14, "bold"), bg="white")
        label.pack(pady=10)

        appointments = self.app.db.get_patient_appointments(self.user["id"])
        if appointments:
            doctor_id = appointments[0]["doctor_id"]   # take first appointment
            doctor = self.app.db.get_doctor_by_id(doctor_id)
            if doctor:
                tk.Label(
                    self.display_frame,
                    text=f"Dr. {doctor['full_name']} ({doctor['specialization']})",
                    font=("Arial", 12), bg="white"
                ).pack(pady=20)
            else:
                tk.Label(self.display_frame, text="❌ Doctor not found", bg="white").pack(pady=10)
        else:
            tk.Label(self.display_frame, text="❌ No doctor assigned", bg="white").pack(pady=10)

    def view_history(self):
        self.clear_display()
        label = tk.Label(self.display_frame, text="Medical History", font=("Arial", 14, "bold"), bg="white")
        label.pack(pady=10)

        history = self.app.db.get_patient_medical_history(self.user["id"])
        if history:
            cols = ("Date", "Medical History")
            tree = ttk.Treeview(self.display_frame, columns=cols, show="headings", height=10)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=250)
            tree.pack(fill="both", expand=True)

            for h in history:
                tree.insert("", "end", values=(h["record_date"], h["medical_history"]))
        else:
            tk.Label(self.display_frame, text="❌ No medical history found", bg="white").pack(pady=10)

    def clear_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

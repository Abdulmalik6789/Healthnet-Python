import tkinter as tk
from tkinter import ttk

class DoctorDashboard:
    def __init__(self, root, app, user):
        self.root = root
        self.app = app
        self.user = user  # doctor user info (contains linked_id to doctors table)
        self.build_ui()

    def build_ui(self):
        # Clear old widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # ---------- Header ----------
        header = tk.Frame(self.root, bg="#673AB7", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text=f"Doctor Dashboard - {self.user['full_name']}",
            font=("Arial", 16, "bold"),
            bg="#673AB7", fg="white"
        )
        title.pack(pady=10)

        # ---------- Buttons ----------
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(side="left", fill="y", padx=10, pady=10)

        btn_schedule = tk.Button(
            button_frame, text="📅 View Schedule", width=20, height=2,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
            command=self.view_schedule
        )
        btn_schedule.pack(pady=10)

        btn_specialization = tk.Button(
            button_frame, text="🩺 View Specialization", width=20, height=2,
            bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
            command=self.view_specialization
        )
        btn_specialization.pack(pady=10)

        btn_logout = tk.Button(
            button_frame, text="🚪 Logout", width=20, height=2,
            bg="#f44336", fg="white", font=("Arial", 12, "bold"),
            command=self.app.logout_user
        )
        btn_logout.pack(pady=10)

        # ---------- Display Area ----------
        self.display_frame = tk.Frame(self.root, bg="white", relief="groove", bd=2)
        self.display_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # ---------- Show Doctor's Schedule ----------
    def view_schedule(self):
        self.clear_display()
        label = tk.Label(self.display_frame, text="📅 My Schedule", font=("Arial", 14, "bold"), bg="white")
        label.pack(pady=10)

        schedule = self.app.db.get_doctor_schedule(self.user["linked_id"])  # Fetch from DB
        if schedule:
            cols = ("Patient Name", "Date", "Time", "Status")
            tree = ttk.Treeview(self.display_frame, columns=cols, show="headings", height=10)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            tree.pack(fill="both", expand=True)

            for s in schedule:
                tree.insert("", "end", values=(s["patient_name"], s["appointment_date"], s["appointment_time"], s["status"]))
        else:
            tk.Label(self.display_frame, text="❌ No appointments scheduled", bg="white").pack(pady=10)

    # ---------- Show Doctor's Specialization ----------
    def view_specialization(self):
        self.clear_display()
        label = tk.Label(self.display_frame, text="🩺 My Specialization", font=("Arial", 14, "bold"), bg="white")
        label.pack(pady=10)

        doctor = self.app.db.get_doctor_by_id(self.user["linked_id"])
        if doctor:
            tk.Label(
                self.display_frame,
                text=f"Specialization: {doctor['specialization']}",
                font=("Arial", 12), bg="white"
            ).pack(pady=20)
        else:
            tk.Label(self.display_frame, text="❌ Specialization not found", bg="white").pack(pady=10)

    # ---------- Clear Display Area ----------
    def clear_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

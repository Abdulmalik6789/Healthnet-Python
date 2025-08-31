

import tkinter as tk
from tkinter import ttk, messagebox
import uuid

# -----------------------------
# DoctorsPage UI
# -----------------------------
class DoctorsPage:
    def __init__(self, root, app):
        self.root = root
        self.app = app  #
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg="#2c3e50")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            header_content,
            text="Doctor Management",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", pady=10)

        tk.Button(
            header_content,
            text="← Back to Dashboard",
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.app.show_dashboard,
        ).pack(side="right", pady=15)

        # Content
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Controls
        control_frame = tk.Frame(content_frame, bg="white", relief="raised", bd=1)
        control_frame.pack(fill="x", pady=(0, 20))
        control_inner = tk.Frame(control_frame, bg="white")
        control_inner.pack(fill="x", padx=20, pady=15)

        search_frame = tk.Frame(control_inner, bg="white")
        search_frame.pack(fill="x", pady=(0, 10))
        tk.Label(search_frame, text="Search Doctors:", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30, relief="solid", bd=1)
        self.search_entry.pack(side="left", padx=(10, 0), ipady=5)
        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.search_doctors,
        ).pack(side="left", padx=(10, 0), ipady=5)

        buttons_frame = tk.Frame(control_inner, bg="white")
        buttons_frame.pack(fill="x")
        tk.Button(
            buttons_frame,
            text="Add New Doctor",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.add_doctor,
        ).pack(side="left", padx=(0, 10), ipady=8, ipadx=15)
        tk.Button(
            buttons_frame,
            text="Edit Doctor",
            font=("Arial", 12),
            bg="#f39c12",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.edit_doctor,
        ).pack(side="left", padx=(0, 10), ipady=8, ipadx=15)
        tk.Button(
            buttons_frame,
            text="Delete Doctor",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.delete_doctor,
        ).pack(side="left", ipady=8, ipadx=15)

        # Table
        table_frame = tk.Frame(content_frame, bg="white", relief="raised", bd=1)
        table_frame.pack(fill="both", expand=True)

        table_header = tk.Frame(table_frame, bg="#34495e", height=40)
        table_header.pack(fill="x")
        table_header.pack_propagate(False)
        tk.Label(table_header, text="Doctors List", font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(pady=10)

        tree_frame = tk.Frame(table_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("ID", "First Name", "Last Name", "Specialization", "Phone", "Email", "Schedule")
        self.doctors_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150, minwidth=100)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.doctors_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.doctors_tree.xview)
        self.doctors_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.doctors_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        self.load_doctors()

    # --------------- Data ops ---------------
    def load_doctors(self):
        try:
            doctors = self.app.db.get_all_doctors()
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)
            for d in doctors:
                self.doctors_tree.insert(
                    "",
                    "end",
                    values=(
                        d.get("id", ""),
                        d.get("first_name", ""),
                        d.get("last_name", ""),
                        d.get("specialization", ""),
                        d.get("phone", ""),
                        d.get("email", ""),
                        d.get("schedule", ""),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load doctors: {e}")

    def search_doctors(self):
        term = self.search_entry.get().strip()
        if not term:
            self.load_doctors()
            return
        try:
            results = self.app.db.search_doctors(term)
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)
            for d in results:
                self.doctors_tree.insert(
                    "",
                    "end",
                    values=(
                        d.get("id", ""),
                        d.get("first_name", ""),
                        d.get("last_name", ""),
                        d.get("specialization", ""),
                        d.get("phone", ""),
                        d.get("email", ""),
                        d.get("schedule", ""),
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    # --------------- UI actions ---------------
    def add_doctor(self):
        self.doctor_form_window("Add New Doctor")

    def edit_doctor(self):
        sel = self.doctors_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a doctor to edit")
            return
        values = self.doctors_tree.item(sel[0])["values"]
        self.doctor_form_window("Edit Doctor", values)

    def delete_doctor(self):
        sel = self.doctors_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        values = self.doctors_tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirm Delete", f"Delete doctor '{values[1]} {values[2]}'?"):
            try:
                self.app.db.delete_doctor(values[0])
                messagebox.showinfo("Success", "Doctor deleted successfully")
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete doctor: {e}")

    # --------------- Form window (scrollable) ---------------
    def doctor_form_window(self, title, doctor_data=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("640x520")  # compact but comfortable; scrollbar ensures full access
        win.configure(bg="white")
        win.transient(self.root)
        win.grab_set()

        # Canvas + vertical scrollbar layout
        canvas = tk.Canvas(win, bg="white", highlightthickness=0)
        vbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        form = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=form, anchor="nw")

        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Keep canvas width in sync so widgets fill horizontally
            canvas_width = event.width
            canvas.itemconfig(1, width=canvas_width)  # item 1 is the created window above
        form.bind("<Configure>", _on_configure)

        # Mouse wheel support
        def _on_mousewheel(event):
            # Windows / Linux
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Title
        tk.Label(form, text=title, font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(10, 20))

        # Fields
        self._fields = {}
        field_names = ["first_name", "last_name", "specialization", "phone", "email", "schedule"]
        field_labels = ["First Name", "Last Name", "Specialization", "Phone", "Email", "Schedule"]

        for field, label in zip(field_names, field_labels):
            tk.Label(form, text=f"{label}:", font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(8, 5))
            if field == "specialization":
                w = ttk.Combobox(form, font=("Arial", 12), state="readonly",
                                 values=[
                                     "Cardiology", "Neurology", "Orthopedics", "Pediatrics",
                                     "Dermatology", "Psychiatry", "General Medicine", "Surgery",
                                 ])
            elif field == "schedule":
                w = tk.Text(form, font=("Arial", 12), height=5, relief="solid", bd=1)
            else:
                w = tk.Entry(form, font=("Arial", 12), relief="solid", bd=1)
            self._fields[field] = w
            if field == "schedule":
                w.pack(fill="x", pady=(0, 10))
            else:
                w.pack(fill="x", ipady=8, pady=(0, 10))

        # Prefill if editing (doctor_data order: ID, First, Last, Specialization, Phone, Email, Schedule)
        if doctor_data:
            mapped = {
                "id": doctor_data[0],
                "first_name": doctor_data[1],
                "last_name": doctor_data[2],
                "specialization": doctor_data[3],
                "phone": doctor_data[4],
                "email": doctor_data[5],
                "schedule": doctor_data[6],
            }
            for k, w in self._fields.items():
                val = mapped.get(k, "")
                if k == "schedule":
                    w.delete("1.0", tk.END)
                    w.insert("1.0", str(val))
                elif hasattr(w, "set"):
                    w.set(str(val))
                else:
                    w.delete(0, tk.END)
                    w.insert(0, str(val))

        # Buttons
        btn_row = tk.Frame(form, bg="white")
        btn_row.pack(fill="x", pady=(16, 30))
        tk.Button(
            btn_row,
            text="Save",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.save_doctor(win, self._fields, doctor_data),
        ).pack(side="left", padx=(0, 10), ipady=8, ipadx=24)
        tk.Button(
            btn_row,
            text="Cancel",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=win.destroy,
        ).pack(side="left", ipady=8, ipadx=24)

    # --------------- Save ---------------
    def save_doctor(self, window, fields, doctor_data=None):
        try:
            # Guard: ensure the db has required methods
            for m in ("add_doctor", "update_doctor"):
                if not hasattr(self.app.db, m):
                    messagebox.showerror("Configuration error", f"Your Database class is missing `{m}()`")
                    return

            # Collect data
            data = {}
            for field, widget in fields.items():
                if field == "schedule":
                    data[field] = widget.get("1.0", tk.END).strip()
                else:
                    data[field] = widget.get().strip() if hasattr(widget, "get") else ""

            # Basic validation
            for rf in ("first_name", "last_name", "specialization", "phone", "email"):
                if not data.get(rf):
                    messagebox.showerror("Error", f"Please fill in {rf.replace('_', ' ').title()}")
                    return

            # Optional: capture current user id if your app provides it
            data["user_id"] = getattr(self.app, "current_user_id", None)

            if doctor_data:  # edit existing; doctor_data[0] is primary key id
                data["id"] = doctor_data[0]
                self.app.db.update_doctor(data)
                messagebox.showinfo("Success", "Doctor updated successfully and added to list")
            else:
                new_code = self.app.db.add_doctor(data)
                messagebox.showinfo("Success", f"Doctor added successfully (ID: {new_code}) and added to list")

            window.destroy()
            self.load_doctors()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save doctor: {e}")



"""
Database Connection and Operations
MySQL (XAMPP) Integration
"""
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, date

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'healthnethlm_db'
        }
    
    def connect(self):
        try:
            temp_config = self.config.copy()
            temp_config.pop('database')
            temp_connection = mysql.connector.connect(**temp_config)
            temp_cursor = temp_connection.cursor()
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS healthnet_db")
            temp_cursor.close()
            temp_connection.close()
            
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL database successfully")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        return True
    
    def create_tables(self):
        try:
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('Admin', 'Doctor', 'Nurse', 'Patient') NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            patients_table = """
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                patient_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                age INT,
                date_of_birth DATE,
                gender ENUM('Male', 'Female', 'Other'),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                medical_history TEXT,
                emergency_contact VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            # Doctors table
            doctors_table = """
    CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        specialization VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(150) NOT NULL,
        schedule TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
          """

          # Staff Table
            staff_table = """
           CREATE TABLE IF NOT EXISTS staff (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            role VARCHAR(100) NOT NULL,
            department VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(150),
            hire_date DATE,
            salary DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          )
            """

             # Appointment Table
            appointments_table = """
               CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('Scheduled','Confirmed','Completed','Cancelled') DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
"""


            self.cursor.execute(users_table)
            self.cursor.execute(patients_table)
            self.cursor.execute(doctors_table)
            self.cursor.execute(staff_table)
            self.cursor.execute(appointments_table)
            self.connection.commit()
            self.create_default_admin()
            print("Database tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def create_default_admin(self):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if self.cursor.fetchone():
                return
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            query = """
            INSERT INTO users (username, password, role, full_name, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, ('admin', password_hash, 'Admin', 'System Administrator',
                                        'admin@healthnet.com', '1234567890'))
            self.connection.commit()
            print("Default admin user created: admin/admin123")
        except Error as e:
            print(f"Error creating default admin: {e}")
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        try:
            password_hash = self.hash_password(password)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password_hash))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Authentication error: {e}")
            return None
    
    def create_user(self, username, password, role, full_name, email=None, phone=None):
        try:
            password_hash = self.hash_password(password)
            query = """
            INSERT INTO users (username, password, role, full_name, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (username, password_hash, role, full_name, email, phone))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating user: {e}")
            return False

    # ----------------------
    # ✅ PATIENT CRUD METHODS
    # ----------------------
    def add_patient(self, data):
        """Insert new patient"""
        try:
            # Calculate age from DOB
            dob = data.get("date_of_birth")
            if dob:
                birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
                today = date.today()
                data['age'] = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                data['age'] = None

            query = """
            INSERT INTO patients (
                user_id, patient_id, first_name, last_name, age, date_of_birth, gender, phone, email, address,
                medical_history, emergency_contact
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data.get("user_id"),
                data.get("patient_id"),
                data.get("first_name"),
                data.get("last_name"),
                data.get("age"),
                data.get("date_of_birth"),
                data.get("gender"),
                data.get("phone"),
                data.get("email"),
                data.get("address"),
                data.get("medical_history"),
                data.get("emergency_contact"),
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding patient: {e}")
            return False

    def get_all_patients(self):
        try:
            self.cursor.execute("""
                SELECT id, patient_id, first_name, last_name, age, date_of_birth, gender, phone, email, address,
                       medical_history, emergency_contact, created_at
                FROM patients
                ORDER BY created_at DESC
            """)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching patients: {e}")
            return []

    def update_patient(self, data):
        """Update existing patient"""
        try:
            # Calculate age from DOB
            dob = data.get("date_of_birth")
            if dob:
                birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
                today = date.today()
                data['age'] = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                data['age'] = None

            query = """
            UPDATE patients SET 
                first_name=%s, last_name=%s, age=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s,
                address=%s, medical_history=%s, emergency_contact=%s
            WHERE patient_id=%s
            """
            values = (
                data.get("first_name"),
                data.get("last_name"),
                data.get("age"),
                data.get("date_of_birth"),
                data.get("gender"),
                data.get("phone"),
                data.get("email"),
                data.get("address"),
                data.get("medical_history"),
                data.get("emergency_contact"),
                data.get("patient_id")
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating patient: {e}")
            return False

    def delete_patient(self, patient_id):
        try:
            self.cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting patient: {e}")
            return False
        
            # ----------------------
    # ✅ DASHBOARD STATS METHODS
    # ----------------------
    def count_patients(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM patients")
            result = self.cursor.fetchone()
            return result["count"] if result else 0
        except Error as e:
            print("Error counting patients:", e)
            return 0

    def count_doctors(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM doctors")
            result = self.cursor.fetchone()
            return result["count"] if result else 0
        except Error as e:
            print("Error counting doctors:", e)
            return 0

    def count_staff(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM staff")
            result = self.cursor.fetchone()
            return result["count"] if result else 0
        except Error as e:
            print("Error counting staff:", e)
            return 0

    def count_todays_appointments(self):
        try:
            self.cursor.execute(
                "SELECT COUNT(*) as count FROM appointments WHERE DATE(appointment_date) = CURDATE()"
            )
            result = self.cursor.fetchone()
            return result["count"] if result else 0
        except Error as e:
            print("Error counting today's appointments:", e)
            return 0
        
        # ---------------- DOCTORS ----------------
  # ---------------------- Doctor Methods ----------------------

    def add_doctor(self, data):
        query = """
            INSERT INTO doctors (first_name, last_name, specialization, phone, email, schedule)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("specialization"),
            data.get("phone"),
            data.get("email"),
            data.get("schedule"),
        )
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def update_doctor(self, data):
        query = """
            UPDATE doctors 
            SET first_name=%s, last_name=%s, specialization=%s, phone=%s, email=%s, schedule=%s
            WHERE id=%s
        """
        values = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("specialization"),
            data.get("phone"),
            data.get("email"),
            data.get("schedule"),
            data.get("id"),
        )
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_doctor(self, doctor_id):
        query = "DELETE FROM doctors WHERE id=%s"
        self.cursor.execute(query, (doctor_id,))
        self.connection.commit()

    def get_all_doctors(self):
        self.cursor.execute("SELECT * FROM doctors ORDER BY id DESC")
        return self.cursor.fetchall()

    def search_doctors(self, term):
        like_term = f"%{term}%"
        query = """
            SELECT * FROM doctors
            WHERE first_name LIKE %s OR last_name LIKE %s OR specialization LIKE %s 
                  OR phone LIKE %s OR email LIKE %s
        """
        self.cursor.execute(query, (like_term, like_term, like_term, like_term, like_term))
        return self.cursor.fetchall()
    
   # ---------------- STAFF METHODS ----------------
    def add_staff(self, data):
        query = """
            INSERT INTO staff (full_name, role, department, phone, email, hire_date, salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            data['full_name'],
            data['role'],
            data['department'],
            data['phone'],
            data['email'],
            data['hire_date'],
            data['salary']
        ))
        self.connection.commit()

    def update_staff(self, data):
        query = """
            UPDATE staff 
            SET full_name=%s, role=%s, department=%s, phone=%s, email=%s, hire_date=%s, salary=%s
            WHERE id=%s
        """
        self.cursor.execute(query, (
            data['full_name'],
            data['role'],
            data['department'],
            data['phone'],
            data['email'],
            data['hire_date'],
            data['salary'],
            data['id']
        ))
        self.connection.commit()

    def delete_staff(self, staff_id):
        query = "DELETE FROM staff WHERE id=%s"
        self.cursor.execute(query, (staff_id,))
        self.connection.commit()

    def get_all_staff(self):
        self.cursor.execute("SELECT * FROM staff ORDER BY id DESC")
        return self.cursor.fetchall()

    def search_staff(self, term):
        like_term = f"%{term}%"
        query = """
            SELECT * FROM staff 
            WHERE full_name LIKE %s 
               OR role LIKE %s 
               OR department LIKE %s 
               OR email LIKE %s
        """
        self.cursor.execute(query, (like_term, like_term, like_term, like_term))
        return self.cursor.fetchall()
    
# ---------------------- APPOINTMENT METHODS ----------------------
def add_appointment(self, data):
    try:
        query = """
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (
            data['patient_id'],
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time'],
            data.get('status', 'Scheduled'),
            data.get('notes', '')
        ))
        self.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error adding appointment: {e}")
        return False

def get_all_appointments(self):
    try:
        query = """
            SELECT a.id, a.patient_id, a.doctor_id,
                   p.first_name AS patient_first, p.last_name AS patient_last,
                   d.first_name AS doctor_first, d.last_name AS doctor_last,
                   a.appointment_date, a.appointment_time, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date, a.appointment_time
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    except Error as e:
        print(f"Error fetching appointments: {e}")
        return []

def update_appointment(self, data):
    try:
        query = """
            UPDATE appointments
            SET patient_id=%s, doctor_id=%s, appointment_date=%s, appointment_time=%s, status=%s, notes=%s
            WHERE id=%s
        """
        self.cursor.execute(query, (
            data['patient_id'],
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time'],
            data['status'],
            data['notes'],
            data['id']
        ))
        self.connection.commit()
        return True
    except Error as e:
        print(f"Error updating appointment: {e}")
        return False

def update_appointment_status(self, appointment_id, status):
    try:
        query = "UPDATE appointments SET status=%s WHERE id=%s"
        self.cursor.execute(query, (status, appointment_id))
        self.connection.commit()
        return True
    except Error as e:
        print(f"Error updating appointment status: {e}")
        return False

def search_appointments(self, term):
    try:
        query = """
            SELECT a.id, a.patient_id, a.doctor_id,
                   p.first_name AS patient_first, p.last_name AS patient_last,
                   d.first_name AS doctor_first, d.last_name AS doctor_last,
                   a.appointment_date, a.appointment_time, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            WHERE p.first_name LIKE %s OR p.last_name LIKE %s
               OR d.first_name LIKE %s OR d.last_name LIKE %s
            ORDER BY a.appointment_date, a.appointment_time
        """
        term_wild = f"%{term}%"
        self.cursor.execute(query, (term_wild, term_wild, term_wild, term_wild))
        return self.cursor.fetchall()
    except Error as e:
        print(f"Error searching appointments: {e}")
        return []

def get_all_patients_combobox(self):
    """Fetch all patients for combobox"""
    query = "SELECT id, CONCAT(first_name, ' ', last_name) AS full_name FROM patients ORDER BY first_name"
    cursor = self.connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_all_doctors_combobox(self):
    """Fetch all doctors for combobox"""
    query = "SELECT id, CONCAT(first_name, ' ', last_name) AS full_name FROM doctors ORDER BY first_name"
    cursor = self.connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def close(self):
    if self.cursor:
        self.cursor.close()
    if self.connection:
        self.connection.close()
    print("Database connection closed")
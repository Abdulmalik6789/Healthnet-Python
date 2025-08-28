"""
Database Connection and Operations
MySQL (XAMPP) Integration
"""
import mysql.connector
from mysql.connector import Error
import hashlib

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
        # Database configuration for XAMPP
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',  # Default XAMPP password is empty
            'database': 'healthnet_db'
        }
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            # First connect without database to create it if needed
            temp_config = self.config.copy()
            temp_config.pop('database')
            
            temp_connection = mysql.connector.connect(**temp_config)
            temp_cursor = temp_connection.cursor()
            
            # Create database if it doesn't exist
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS healthnet_db")
            temp_cursor.close()
            temp_connection.close()
            
            # Now connect to the database
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("Connected to MySQL database successfully")
            
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
        return True
    
    def create_tables(self):
        """Create all necessary tables"""
        try:
            # Users table
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('Admin', 'Doctor', 'Nurse', 'Lab', 'Patient') NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Patients table
            patients_table = """
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                patient_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                date_of_birth DATE,
                gender ENUM('Male', 'Female', 'Other'),
                phone VARCHAR(20),
                email VARCHAR(100),
                address TEXT,
                medical_history TEXT,
                emergency_contact VARCHAR(100),
                emergency_phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            
            # Doctors table
            doctors_table = """
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                doctor_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                specialization VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                schedule TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            
            # Staff table
            staff_table = """
            CREATE TABLE IF NOT EXISTS staff (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                staff_id VARCHAR(20) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                role VARCHAR(50),
                department VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            
            # Appointments table
            appointments_table = """
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                doctor_id INT,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                reason TEXT,
                status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
            """
            
            # Execute table creation
            tables = [users_table, patients_table, doctors_table, staff_table, appointments_table]
            for table in tables:
                self.cursor.execute(table)
            
            self.connection.commit()
            
            # Create default admin user if not exists
            self.create_default_admin()
            
            print("Database tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    
    def create_default_admin(self):
        """Create default admin user"""
        try:
            # Check if admin exists
            self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if self.cursor.fetchone():
                return
            
            # Create admin user
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            admin_data = {
                'username': 'admin',
                'password': password_hash,
                'role': 'Admin',
                'full_name': 'System Administrator',
                'email': 'admin@healthnet.com',
                'phone': '1234567890'
            }
            
            query = """
            INSERT INTO users (username, password, role, full_name, email, phone)
            VALUES (%(username)s, %(password)s, %(role)s, %(full_name)s, %(email)s, %(phone)s)
            """
            
            self.cursor.execute(query, admin_data)
            self.connection.commit()
            print("Default admin user created: admin/admin123")
            
        except Error as e:
            print(f"Error creating default admin: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            password_hash = self.hash_password(password)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password_hash))
            user = self.cursor.fetchone()
            return user
        except Error as e:
            print(f"Authentication error: {e}")
            return None
    
    def create_user(self, username, password, role, full_name, email=None, phone=None):
        """Create new user"""
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
    
    def execute_query(self, query, params=None):
        """Execute custom query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except Error as e:
            print(f"Query execution error: {e}")
            return None

    # ----------------------
# ✅ PATIENT CRUD METHODS
# ----------------------
def add_patient(self, data):
    """Insert new patient"""
    try:
        query = """
        INSERT INTO patients (
            user_id, patient_id, first_name, last_name, date_of_birth, gender, phone, email, address,
            medical_history, emergency_contact, emergency_phone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get("user_id"),
            data.get("patient_id"),
            data.get("first_name"),
            data.get("last_name"),
            data.get("date_of_birth"),
            data.get("gender"),
            data.get("phone"),
            data.get("email"),
            data.get("address"),
            data.get("medical_history"),
            data.get("emergency_contact"),
            data.get("emergency_phone"),
        )
        self.cursor.execute(query, values)
        self.connection.commit()
        return True
    except Error as e:
        print(f"Error adding patient: {e}")
        return False


def get_all_patients(self):
    """Fetch all patients"""
    try:
        self.cursor.execute("""
            SELECT id, user_id, patient_id, first_name, last_name, date_of_birth, gender, phone, email, address,
                   medical_history, emergency_contact, emergency_phone, created_at
            FROM patients
            ORDER BY created_at DESC
        """)
        return self.cursor.fetchall()
    except Error as e:
        print(f"Error fetching patients: {e}")
        return []


def update_patient(self, patient_data):
    """Update an existing patient"""
    try:
        query = """
        UPDATE patients SET 
            first_name=%s, last_name=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s,
            address=%s, medical_history=%s, emergency_contact=%s, emergency_phone=%s
        WHERE patient_id=%s
        """
        values = (
            patient_data.get("first_name"),
            patient_data.get("last_name"),
            patient_data.get("date_of_birth"),
            patient_data.get("gender"),
            patient_data.get("phone"),
            patient_data.get("email"),
            patient_data.get("address"),
            patient_data.get("medical_history"),
            patient_data.get("emergency_contact"),
            patient_data.get("emergency_phone"),
            patient_data.get("patient_id"),
        )
        self.cursor.execute(query, values)
        self.connection.commit()
        return True
    except Error as e:
        print(f"Error updating patient: {e}")
        return False


def delete_patient(self, patient_id):
    """Delete patient record"""
    try:
        self.cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        self.connection.commit()
        return True
    except Error as e:
        print(f"Error deleting patient: {e}")
        return False


def close(self):
    """Close database connection"""
    if self.cursor:
        self.cursor.close()
    if self.connection:
        self.connection.close()
    print("Database connection closed")

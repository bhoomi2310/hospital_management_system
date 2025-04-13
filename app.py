from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create tables if they don't exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Drop existing tables to avoid conflicts (this is just for debugging, use migrations in production)
    cursor.execute("DROP TABLE IF EXISTS appointments")
    cursor.execute("DROP TABLE IF EXISTS bills")
    cursor.execute("DROP TABLE IF EXISTS patients")
    
    # Create the patients table
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        gender TEXT,
                        disease TEXT)''')
    
    # Create the appointments table with patient_name column
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_name TEXT,
                        doctor TEXT,
                        date TEXT)''')
    
    # Create the bills table with patient_name column
    cursor.execute('''CREATE TABLE IF NOT EXISTS bills (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_name TEXT,
                        amount REAL,
                        status TEXT)''')
    
    conn.commit()
    conn.close()




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)",
                       (name, age, gender, disease))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_patient.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor = request.form['doctor']
        date = request.form['date']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Inserting patient_name, doctor, and date directly
        cursor.execute("INSERT INTO appointments (patient_name, doctor, date) VALUES (?, ?, ?)",
                       (patient_name, doctor, date))
        conn.commit()
        conn.close()
        return redirect('/appointments')
    
    return render_template('appointments.html')


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        amount = request.form['amount']
        status = request.form['status']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Inserting patient_name, amount, and status directly
        cursor.execute("INSERT INTO bills (patient_name, status, amount) VALUES (?, ?, ?)",
                       (patient_name, status, amount))
        conn.commit()
        conn.close()
        return redirect('/billing')
    
    return render_template('billing.html')


@app.route('/view_patients')
def view_patients():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('view_patients.html', patients=patients)

@app.route('/view_appointments')
def view_appointments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Fetching patient_name directly from appointments table
    cursor.execute('''SELECT a.id, a.patient_name, a.doctor, a.date FROM appointments a''')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/view_bills')
def view_bills():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Fetching patient_name directly from bills table
    cursor.execute('''SELECT b.id, b.patient_name, b.status, b.amount FROM bills b''')
    bills = cursor.fetchall()
    conn.close()
    return render_template('view_bills.html', bills=bills)





if __name__ == '__main__':
    init_db()
    app.run(debug=True)


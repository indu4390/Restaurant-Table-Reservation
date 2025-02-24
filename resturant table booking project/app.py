from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup (in-memory database for simplicity)
def init_db():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations
                      (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, date TEXT, time TEXT, people INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        people = request.form['people']
        
        # Save reservation data to the database
        conn = sqlite3.connect('reservations.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO reservations (name, email, phone, date, time, people)
                          VALUES (?, ?, ?, ?, ?, ?)''', (name, email, phone, date, time, people))
        conn.commit()
        conn.close()
        
        return redirect(url_for('confirmation'))
    
    return render_template('reservation_form.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)

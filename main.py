import sqlite3
from flask import Flask, render_template, request,send_from_directory

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('contact.db') #database name where contacts table name
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

@app.route('/')
def home():
    return render_template('index.html', success=None)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()


    # Return the same page with a success message
    return render_template('index.html')

@app.route('/download/resume')
def download_resume():
    return send_from_directory('static/files', 'resume.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

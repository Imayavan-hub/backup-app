from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
import bcrypt
import os
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://hariprasathhari2004:J18amHnFN7XXlH2H@cluster0.3jifg.mongodb.net/")
db = client['backup_system']
users_collection = db['users']
files_collection = db['backups']

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if users_collection.find_one({'username': username}):
            flash('Username already exists!')
        else:
            users_collection.insert_one({'username': username, 'password': hashed_password})
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Backup page
@app.route('/home')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Backup logic
@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    files = request.files.getlist('source_files')
    for file in files:
        files_collection.insert_one({'filename': file.filename, 'file': file.read()})

    flash(f"Backup of {len(files)} files completed successfully.")
    return redirect(url_for('index'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Test route
@app.route('/test')
def test():
    return "Flask is running properly!"

if __name__ == '__main__':
    app.run(debug=True)
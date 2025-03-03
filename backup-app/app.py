from flask import Flask, render_template, request, redirect, url_for, flash
from backup import backup_files
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backup', methods=['POST'])
def backup():
    source_dirs = request.form.getlist('source_dirs')
    backup_dir = request.form.get('backup_dir')

    if not source_dirs or not backup_dir:
        flash("Please select both source and backup directories.")
        return redirect(url_for('index'))

    results = []
    for source_dir in source_dirs:
        result = backup_files(source_dir, backup_dir)
        results.append(result)

    for res in results:
        flash(res)
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return "Flask is running properly!"

if __name__ == '__main__':
    app.run(debug=True)


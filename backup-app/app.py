from flask import Flask, render_template, request, redirect, url_for, flash
from backup import backup_files

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Default directories (modify as needed)
SOURCE_DIR = '/home/imayavan/Downloads/blender-4.3.2-linux-x64'
BACKUP_DIR = '/home/imayavan/backup folder'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/backup', methods=['POST'])
def backup():
    result = backup_files(SOURCE_DIR, BACKUP_DIR)
    flash(result)
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return "Flask is running properly!"

if __name__ == '__main__':
    app.run(debug=True)


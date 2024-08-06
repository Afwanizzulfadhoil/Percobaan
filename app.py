from flask import Flask, request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

# Memuat variabel lingkungan dari file .env
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
name_db = os.getenv("NAME_DB")
db = mongo.cx[name_db]

UPLOAD_FOLDER = 'uplouds/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.files.insert_one({
            'filename': filename,
            'content_type': file.content_type
        })
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

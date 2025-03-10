from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Convert to grayscale
            img = cv2.imread(filepath)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], file.filename)
            cv2.imwrite(processed_path, gray_img)
            
            return render_template('index.html', original=file.filename, processed=file.filename)
    
    return render_template('index.html', original=None, processed=None)

if __name__ == '__main__':
    app.run(debug=True)

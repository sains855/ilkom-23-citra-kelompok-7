from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import cv2

app = Flask(__name__, template_folder='view')
app.secret_key = 'rahasia'  # dibutuhkan untuk menyimpan session

# Konfigurasi folder
app.config['UPLOAD_FOLDER'] = 'img/img_upload/'
app.config['PROCESSED_FOLDER'] = 'img/img_processed/'

# Buat folder jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# 1. Halaman welcome
@app.route('/')
def welcome():
    return render_template('welcome.html')

# 2. Halaman upload gambar (add.html)
@app.route('/add_gambar', methods=['GET'])
def add_gambar():
    return render_template('add.html')

# 3. Proses upload dan konversi gambar
@app.route('/proses_gambar', methods=['POST'])
def proses_gambar():
    if 'image' not in request.files:
        return redirect(url_for('add_gambar'))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('add_gambar'))

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Proses grayscale
        img = cv2.imread(filepath)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        cv2.imwrite(processed_path, gray_img)

        # Simpan nama file di session untuk digunakan di halaman result
        session['original'] = filename
        session['processed'] = filename

        return redirect(url_for('result_gambar'))

# 4. Halaman hasil (result.html)
@app.route('/result_gambar', methods=['GET'])
def result_gambar():
    original = session.get('original')
    processed = session.get('processed')
    return render_template('result.html', original=original, processed=processed)

# Untuk menampilkan gambar di template
@app.route('/img/<folder>/<filename>')
def get_image(folder, filename):
    if folder in ['img_upload', 'img_processed']:
        return send_from_directory(f'img/{folder}', filename)
    return "Folder tidak ditemukan", 404

if __name__ == '__main__':
    app.run(debug=True)

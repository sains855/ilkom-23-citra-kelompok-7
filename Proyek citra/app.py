from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2

app = Flask(__name__, template_folder='view')

# Konfigurasi folder upload dan hasil proses
app.config['UPLOAD_FOLDER'] = os.path.join('img', 'img_upload')
app.config['PROCESSED_FOLDER'] = os.path.join('img', 'img_processed')

# Pastikan folder upload & processed ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# ================= ROUTES STATIC FILE ====================

@app.route('/style/<path:filename>')
def serve_style(filename):
    return send_from_directory('style', filename)

@app.route('/img_upload/<path:filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route untuk gambar hasil proses
@app.route('/img_processed/<path:filename>')
def processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)

# ================= ROUTES HALAMAN ====================

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/add_gambar', methods=['GET', 'POST'])
def add_gambar():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            # Debug
            print("Gambar disimpan di:", upload_path)

            # Proses grayscale
            img = cv2.imread(upload_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            cv2.imwrite(processed_path, gray_img)

            # Debug
            print("Gambar hasil proses disimpan di:", processed_path)

            return redirect(url_for('result_gambar', filename=filename))

    return render_template('add.html')

@app.route('/result_gambar')
def result_gambar():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))

    return render_template('result.html', original=filename, processed=filename)

# ================== JALANKAN SERVER =====================

if __name__ == '__main__':
    app.run(debug=True)

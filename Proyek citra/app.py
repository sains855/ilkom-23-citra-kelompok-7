from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
from rembg import remove
from PIL import Image
import io

# Membaca folder view
app = Flask(__name__, template_folder='view')

# config folder upload dan hasil proses
app.config['UPLOAD_FOLDER'] = os.path.join('img', 'img_upload')
app.config['PROCESSED_FOLDER'] = os.path.join('img', 'img_processed')

# config folder upload dan processed ke folder yang sudah ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Route WEB untuk style dan gambar

@app.route('/style/<path:filename>')
def serve_style(filename):
    return send_from_directory('style', filename)

@app.route('/script/<path:filename>')
def serve_script(filename):
    return send_from_directory('script', filename)


@app.route('/img_upload/<path:filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/img_processed/<path:filename>')
def processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)

# ===============Route untuk halaman WEB===================

@app.route('/') # halaman welcome
def index():
    return render_template('welcome.html')

@app.route('/add_gambar', methods=['GET', 'POST']) #halaman add
def add_gambar():
    # Proses Upload gambar
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

            # Proses grayscale
            img = cv2.imread(upload_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            cv2.imwrite(processed_path, gray_img)

            return redirect(url_for('result_gambar', filename=filename))

    return render_template('add.html')

@app.route('/result_gambar') #halaman result
def result_gambar():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))

    return render_template('result.html', original=filename, processed=filename)

@app.route('/remove_background', methods=['GET', 'POST'])
def remove_background():
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

            # Proses remove background
            input_image = Image.open(upload_path)
            output_image = remove(input_image)
            
            # Simpan sebagai PNG untuk mempertahankan transparansi
            base_filename = os.path.splitext(filename)[0]  # Hilangkan ekstensi
            processed_filename = f"{base_filename}.png"
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            output_image.save(processed_path)

            return redirect(url_for('result_remove_bg', filename=processed_filename))

    return render_template('remove_bg.html')

@app.route('/result_remove_bg')
def result_remove_bg():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))

    return render_template('result_remove_bg.html', original=filename, processed=filename)
# Run server

if __name__ == '__main__':
    app.run(debug=True)

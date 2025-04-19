from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
from rembg import remove
from PIL import Image
import io
from fpdf import FPDF
import img2pdf

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
            # Simpan original dengan ekstensi asli
            original_filename = file.filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(upload_path)

            # Proses remove background
            input_image = Image.open(upload_path)
            output_image = remove(input_image)
            
            # Simpan hasil dengan ekstensi .png
            base_name = os.path.splitext(original_filename)[0]
            processed_filename = f"{base_name}.png"
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            output_image.save(processed_path)

            return redirect(url_for('result_remove_bg', original=original_filename,processed=processed_filename))

    return render_template('remove_bg.html')


@app.route('/result_remove_bg')
def result_remove_bg():
    original = request.args.get('original')
    processed = request.args.get('processed')
    
    if not original or not processed:
        return redirect(url_for('index'))
    
    return render_template('result_remove_bg.html', original=original, processed=processed)




# Add this config for PDF storage
app.config['PDF_FOLDER'] = os.path.join('img', 'pdf_output')
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)

@app.route('/convert_to_pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save original image
            filename = file.filename
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            # Convert to PDF
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
            
            # Using img2pdf (simple method)
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(upload_path))
            
            return redirect(url_for('result_pdf', 
                                 original=filename, 
                                 pdf_file=pdf_filename))
    
    return render_template('convert_pdf.html')

@app.route('/result_pdf')
def result_pdf():
    original = request.args.get('original')
    pdf_file = request.args.get('pdf_file')
    
    if not original or not pdf_file:
        return redirect(url_for('index'))
    
    return render_template('result_pdf.html', 
                         original=original, 
                         pdf_file=pdf_file)

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)


# Run server

if __name__ == '__main__':
    app.run(debug=True)

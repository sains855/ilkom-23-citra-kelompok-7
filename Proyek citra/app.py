from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from rembg import remove
from PIL import Image
import img2pdf
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, template_folder='view')

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join('img', 'img_upload')
app.config['PROCESSED_FOLDER'] = os.path.join('img', 'img_processed')
app.config['PDF_FOLDER'] = os.path.join('img', 'pdf_output')  # Added PDF folder
app.config['MULTI_PDF_FOLDER'] = os.path.join('img', 'multi_pdf_output')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)  # Create PDF folder
os.makedirs(app.config['MULTI_PDF_FOLDER'], exist_ok=True)

# Helper function for allowed file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Static file routes
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

# Main routes
@app.route('/')
def index():
    return render_template('welcome.html')

# Grayscale conversion routes
@app.route('/add_gambar', methods=['GET', 'POST'])
def add_gambar():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            img = cv2.imread(upload_path)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            cv2.imwrite(processed_path, gray_img)

            return redirect(url_for('result_gambar', filename=filename))

    return render_template('add.html')

@app.route('/result_gambar')
def result_gambar():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))
    return render_template('result.html', original=filename, processed=filename)

# Background removal routes
@app.route('/remove_background', methods=['GET', 'POST'])
def remove_background():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(upload_path)

            input_image = Image.open(upload_path)
            output_image = remove(input_image)
            
            base_name = os.path.splitext(original_filename)[0]
            processed_filename = f"{base_name}.png"
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            output_image.save(processed_path)

            return redirect(url_for('result_remove_bg', 
                                 original=original_filename,
                                 processed=processed_filename))

    return render_template('remove_bg.html')

@app.route('/result_remove_bg')
def result_remove_bg():
    original = request.args.get('original')
    processed = request.args.get('processed')
    if not original or not processed:
        return redirect(url_for('index'))
    return render_template('result_remove_bg.html', 
                         original=original, 
                         processed=processed)

# PDF conversion routes
@app.route('/convert_to_pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        files = request.files.getlist('images')
        if not files or files[0].filename == '':
            return redirect(request.url)
        
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                saved_files.append(upload_path)
        
        if saved_files:
            pdf_filename = f"converted_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
            
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(saved_files))
            
            original_filenames = [os.path.basename(f) for f in saved_files]
            return redirect(url_for('result_pdf', 
                                 original_filenames=','.join(original_filenames),
                                 pdf_file=pdf_filename))
    
    return render_template('convert_pdf.html')

@app.route('/result_pdf')
def result_pdf():
    original_filenames = request.args.get('original_filenames', '').split(',')
    pdf_file = request.args.get('pdf_file')
    
    if not original_filenames or not pdf_file:
        return redirect(url_for('index'))
    
    original_filenames = [f for f in original_filenames if f]
    return render_template('result_pdf.html', 
                         original_filenames=original_filenames,
                         pdf_file=pdf_file)

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['PDF_FOLDER'], 
                             filename, 
                             as_attachment=True)

if __name__ == '__main__':
    # Print paths for debugging
    print("PDF_FOLDER path:", os.path.abspath(app.config['PDF_FOLDER']))
    print("UPLOAD_FOLDER path:", os.path.abspath(app.config['UPLOAD_FOLDER']))
    app.run(debug=True)
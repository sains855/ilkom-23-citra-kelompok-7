from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np
from rembg import remove
from PIL import Image
import img2pdf
from datetime import datetime
import cv2

# Initialize Flask app
app = Flask(__name__, template_folder='view')

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join('img', 'img_upload')
app.config['PROCESSED_FOLDER'] = os.path.join('img', 'img_processed')
app.config['PDF_FOLDER'] = os.path.join('img', 'pdf_output')
app.config['MULTI_PDF_FOLDER'] = os.path.join('img', 'multi_pdf_output')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)
os.makedirs(app.config['MULTI_PDF_FOLDER'], exist_ok=True)

# Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# NumPy-based Grayscale Conversion with Multiple Methods
def numpy_grayscale_conversion(img_array, method='weighted'):
    """
    Convert RGB image to grayscale using NumPy with different methods
    """
    if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
        if method == 'weighted':
            # Weighted average (standard luminance)
            gray = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
        elif method == 'average':
            # Simple average
            gray = np.mean(img_array[..., :3], axis=2)
        elif method == 'luminosity':
            # Alternative luminosity formula
            gray = np.dot(img_array[..., :3], [0.21, 0.72, 0.07])
        else:
            # Default to weighted
            gray = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
        
        return gray.astype(np.uint8)
    return img_array

# NumPy-based Background Removal Enhancement
def numpy_background_processing(img_array):
    """
    Enhanced background processing using NumPy operations
    """
    # Convert to float for precise calculations
    img_float = img_array.astype(np.float32) / 255.0
    
    # Apply edge enhancement using NumPy convolution
    if len(img_float.shape) == 3:
        # Sobel edge detection kernel
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        
        # Apply edge detection to each channel
        edges = np.zeros_like(img_float)
        for i in range(img_float.shape[2]):
            # Manual convolution using NumPy
            channel = img_float[:, :, i]
            grad_x = np.zeros_like(channel)
            grad_y = np.zeros_like(channel)
            
            # Apply Sobel filters
            for y in range(1, channel.shape[0] - 1):
                for x in range(1, channel.shape[1] - 1):
                    grad_x[y, x] = np.sum(channel[y-1:y+2, x-1:x+2] * sobel_x)
                    grad_y[y, x] = np.sum(channel[y-1:y+2, x-1:x+2] * sobel_y)
            
            edges[:, :, i] = np.sqrt(grad_x**2 + grad_y**2)
        
        # Enhance edges
        enhanced = img_float + 0.3 * edges
        enhanced = np.clip(enhanced, 0, 1)
        
        return (enhanced * 255).astype(np.uint8)
    
    return img_array

# NumPy-based Image Preprocessing for PDF
def numpy_pdf_preprocessing(img_paths):
    """
    Preprocess images using NumPy before PDF conversion
    """
    processed_paths = []
    
    for img_path in img_paths:
        # Load image as NumPy array
        img = Image.open(img_path).convert('RGB')
        img_array = np.array(img)
        
        # Apply NumPy-based image enhancements
        
        # 1. Brightness and contrast adjustment
        img_float = img_array.astype(np.float32)
        
        # Auto contrast using NumPy percentiles
        for channel in range(3):
            channel_data = img_float[:, :, channel]
            p2, p98 = np.percentile(channel_data, (2, 98))
            if p98 > p2:
                img_float[:, :, channel] = np.clip((channel_data - p2) * 255.0 / (p98 - p2), 0, 255)
        
        # 2. Noise reduction using NumPy (simple box filter)
        kernel_size = 3
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
        
        smoothed = np.zeros_like(img_float)
        pad_size = kernel_size // 2
        
        for channel in range(3):
            padded = np.pad(img_float[:, :, channel], pad_size, mode='edge')
            for y in range(img_float.shape[0]):
                for x in range(img_float.shape[1]):
                    smoothed[y, x, channel] = np.sum(
                        padded[y:y+kernel_size, x:x+kernel_size] * kernel
                    )
        
        # 3. Sharpening using NumPy
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        sharpened = np.zeros_like(smoothed)
        
        for channel in range(3):
            padded = np.pad(smoothed[:, :, channel], 1, mode='edge')
            for y in range(smoothed.shape[0]):
                for x in range(smoothed.shape[1]):
                    sharpened[y, x, channel] = np.sum(
                        padded[y:y+3, x:x+3] * sharpen_kernel
                    )
        
        # Clip values and convert back to uint8
        final_img = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        # Save processed image
        processed_img = Image.fromarray(final_img)
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], f"{base_name}_processed.jpg")
        processed_img.save(processed_path, quality=95)
        processed_paths.append(processed_path)
    
    return processed_paths


# Static file routes
@app.route('/style/<path:filename>')
def serve_style(filename):
    # Mengarahkan ke folder 'style' di Proyek citra
    return send_from_directory(os.path.join(app.root_path, 'style'), filename)

@app.route('/script/<path:filename>')
def serve_script(filename):
    # Mengarahkan ke folder 'script' di Proyek citra
    return send_from_directory(os.path.join(app.root_path, 'script'), filename)

@app.route('/img_upload/<path:filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/img_processed/<path:filename>')
def processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/img/<path:filename>')
def serve_image(filename):
    # Ini mungkin perlu disesuaikan jika gambar contoh ada di 'Proyek citra/img'
    # atau di subfolder lain yang perlu diakses.
    # Untuk saat ini, asumsikan ini merujuk ke folder 'img' di root proyek Flask.
    return send_from_directory(os.path.join(app.root_path, 'img'), filename)


# Home Page
@app.route('/')
def index():
    return render_template('welcome.html')

# Enhanced Grayscale conversion using NumPy
@app.route('/add_gambar', methods=['GET', 'POST'])
def add_gambar():
    if request.method == 'POST':
        file = request.files.get('image')
        method = request.form.get('method', 'weighted')  # Allow method selection
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            img = Image.open(upload_path).convert('RGB')
            img_np = np.array(img)
            gray_np = numpy_grayscale_conversion(img_np, method)
            
            hist, bins = np.histogram(gray_np.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_normalized = cdf * 255 / cdf[-1]
            gray_equalized = np.interp(gray_np.flatten(), bins[:-1], cdf_normalized)
            gray_equalized = gray_equalized.reshape(gray_np.shape).astype(np.uint8)
            
            gray_img = Image.fromarray(gray_equalized)

            processed_filename = f"gray_{method}_{filename}"
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            gray_img.save(processed_path)

            return redirect(url_for('result_gambar', filename=filename, processed=processed_filename))
    
    return render_template('add.html')

@app.route('/result_gambar')
def result_gambar():
    filename = request.args.get('filename')
    processed = request.args.get('processed', filename)
    return render_template('result.html', original=filename, processed=processed)

# Enhanced Remove background using NumPy
@app.route('/remove_background', methods=['GET', 'POST'])
def remove_background():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(upload_path)

            img = Image.open(upload_path)
            img_array = np.array(img)
            enhanced_array = numpy_background_processing(img_array)
            enhanced_img = Image.fromarray(enhanced_array)

            result = remove(enhanced_img)

            result_np = np.array(result)
            
            if result_np.shape[-1] == 4:  # RGBA
                rgb = result_np[..., :3].astype(np.float32)
                alpha = result_np[..., 3].astype(np.float32) / 255.0
                
                white_bg = np.ones_like(rgb) * 255
                blended = rgb * alpha[..., np.newaxis] + white_bg * (1 - alpha[..., np.newaxis])
                
                alpha_smooth = alpha.copy()
                kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16.0
                
                padded_alpha = np.pad(alpha, 1, mode='edge')
                for y in range(alpha.shape[0]):
                    for x in range(alpha.shape[1]):
                        alpha_smooth[y, x] = np.sum(padded_alpha[y:y+3, x:x+3] * kernel)
                
                result_np = np.dstack([rgb.astype(np.uint8), (alpha_smooth * 255).astype(np.uint8)])

            processed_filename = f"nobg_{os.path.splitext(original_filename)[0]}.png"
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            Image.fromarray(result_np).save(processed_path)

            return redirect(url_for('result_remove_bg',
                                    original=original_filename,
                                    processed=processed_filename))
    return render_template('remove_bg.html')

@app.route('/result_remove_bg')
def result_remove_bg():
    return render_template('result_remove_bg.html',
                           original=request.args.get('original'),
                           processed=request.args.get('processed'))

# Enhanced Convert multiple images to PDF with NumPy preprocessing
@app.route('/convert_to_pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        files = request.files.getlist('images')
        enhance_images = request.form.get('enhance', 'on') == 'on'
        
        if not files or files[0].filename == '':
            return redirect(request.url)

        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                saved_files.append(path)

        if saved_files:
            if enhance_images:
                processed_files = numpy_pdf_preprocessing(saved_files)
                files_for_pdf = processed_files
            else:
                files_for_pdf = saved_files
            
            pdf_filename = f"converted_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
            pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
            
            optimized_files = []
            max_size = (1200, 1600)  # A4-like ratio
            
            for img_path in files_for_pdf:
                img = Image.open(img_path)
                img_array = np.array(img)
                
                if img_array.shape[0] > max_size[1] or img_array.shape[1] > max_size[0]:
                    h, w = img_array.shape[:2]
                    scale = min(max_size[0]/w, max_size[1]/h)
                    new_w, new_h = int(w * scale), int(h * scale)
                    
                    y_indices = np.round(np.linspace(0, h-1, new_h)).astype(int)
                    x_indices = np.round(np.linspace(0, w-1, new_w)).astype(int)
                    
                    if len(img_array.shape) == 3:
                        resized = img_array[np.ix_(y_indices, x_indices)]
                    else:
                        resized = img_array[np.ix_(y_indices, x_indices)]
                    
                    resized_img = Image.fromarray(resized)
                    base_name = os.path.splitext(os.path.basename(img_path))[0]
                    resized_path = os.path.join(app.config['PROCESSED_FOLDER'], f"{base_name}_resized.jpg")
                    resized_img.save(resized_path, quality=85)
                    optimized_files.append(resized_path)
                else:
                    optimized_files.append(img_path)
            
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(optimized_files))
                
            return redirect(url_for('result_pdf',
                                    original_filenames=','.join([os.path.basename(f) for f in saved_files]),
                                    pdf_file=pdf_filename))
    return render_template('convert_pdf.html')

@app.route('/result_pdf')
def result_pdf():
    return render_template('result_pdf.html',
                           original_filenames=request.args.get('original_filenames', '').split(','),
                           pdf_file=request.args.get('pdf_file'))

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)

@app.route('/brightnes_adj')
def add_adj():
    return render_template('brightnes_adj.html')

@app.route('/adjust', methods=['POST'])
def adjust_brightness():
    file = request.files.get('image')
    
    if file and allowed_file(file.filename):
        try:
            brightness_factor = float(request.form.get('brightness', 1.0))
        except (TypeError, ValueError):
            brightness_factor = 1.0
        
        original_filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(upload_path)

        img = Image.open(upload_path).convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        adjusted_array = np.clip(img_array * brightness_factor, 0, 255).astype(np.uint8)
        adjusted_img = Image.fromarray(adjusted_array)

        processed_filename = original_filename
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        adjusted_img.save(processed_path)

        return redirect(url_for('result_brightness', 
                                original=original_filename, 
                                processed=processed_filename,
                                brightness=brightness_factor))
    
    return redirect(url_for('add_adj'))

@app.route('/result_brightness')
def result_brightness():
    filename = request.args.get('original')
    processed = request.args.get('processed')
    brightness = request.args.get('brightness')
    return render_template('result_brightness.html', 
                           original=filename, 
                           processed=processed,
                           brightness=brightness)

# --- Rute Baru untuk Efek Negatif (Belum ada logika pemrosesan gambar) ---
@app.route('/negative_effect', methods=['GET', 'POST'])
def negative_effect():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(upload_path)
            
            # Untuk sementara, kita akan langsung redirect ke halaman hasil
            # tanpa memproses gambar, karena logikanya belum ditambahkan.
            # Anda akan melihat gambar asli di tempat gambar 'negative'.
            return redirect(url_for('result_negative_effect',
                                    original=original_filename,
                                    processed=original_filename)) # Menggunakan original sebagai placeholder
    return render_template('negative_effect.html')

@app.route('/result_negative_effect')
def result_negative_effect():
    return render_template('result_negative_effect.html',
                           original=request.args.get('original'),
                           processed=request.args.get('processed')) # Ini akan menampilkan original sebagai negative
# --- Akhir Rute Baru untuk Efek Negatif ---
    
if __name__ == '__main__':
    app.run(debug=True)
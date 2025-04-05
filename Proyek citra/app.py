from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2

app = Flask(__name__, template_folder='view')


app.config['UPLOAD_FOLDER'] = 'img/img_upload/'
app.config['PROCESSED_FOLDER'] = 'img/img_processed/'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)


@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)


@app.route('/style/<path:filename>')
def serve_style(filename):
    return send_from_directory('style', filename)


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
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)


            img = cv2.imread(filepath)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], file.filename)
            cv2.imwrite(processed_path, gray_img)

            return redirect(url_for('result_gambar', filename=file.filename))

    return render_template('add.html')


@app.route('/result_gambar')
def result_gambar():
    filename = request.args.get('filename')
    if not filename:
        return redirect(url_for('index'))

    return render_template('result.html', original=filename, processed=filename)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, send_from_directory
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def restore_image(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Apply a simple restoration (e.g., denoising)
    restored_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    # Save the restored image
    cv2.imwrite(output_path, restored_image)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"
        file = request.files['file']
        if file.filename == '':
            return "No file selected"
        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Restore the image
            restored_image_path = os.path.join(app.config['OUTPUT_FOLDER'], 'restored_image.png')
            restore_image(file_path, restored_image_path)

            return render_template('result.html', original_image=file.filename, restored_image='restored_image.png')
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def send_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/outputs/<filename>')
def send_restored_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
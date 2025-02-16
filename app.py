from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from main import main  # Import the updated main.py file

app = Flask(__name__)

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit file size to 100 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_video_path)

        # Define output video path
        output_video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        
        # Run the main function with the input video path
        main(input_video_path, output_video_path)
        
        return f"Video uploaded and processed successfully! Processed video saved at {output_video_path}"

    return "Invalid file type. Only mp4, mov, avi files are allowed."

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from main import main, call_911

app = Flask(__name__)

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = os.path.join('uploads', 'track')  # Add path for processed videos
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Limit file size to 100 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<path:filename>')
def serve_video(filename):
    """Serve video files from either uploads or uploads/track directory"""
    if filename.startswith('track/'):
        # For processed videos in the track directory
        return send_from_directory('uploads', filename)
    # For original uploaded videos
    return send_from_directory('uploads', filename)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_video_path)

        # Run the main function with the input video path
        fire_detected = main(input_video_path, None)
        
        # The processed video will be in uploads/track/filename
        processed_path = os.path.join('track', filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_path)
        
        # Verify the processed video exists and get its URL
        video_url = None
        if os.path.exists(full_path):
            video_url = url_for('serve_video', filename=processed_path)
            print(f"✅ Processed video available at: {video_url}")
        else:
            print(f"❌ Warning: Processed video not found at {full_path}")
        
        return jsonify({
            'success': True,
            'message': 'Video processed successfully',
            'fire_detected': fire_detected,
            'emergency_call_status': True,  # Since we're simulating the call
            'video_url': video_url,
            'original_video': url_for('serve_video', filename=filename)  # Also return original video URL
        })

    return jsonify({'error': 'Invalid file type. Only mp4, mov, avi files are allowed.'}), 400

if __name__ == '__main__':
    # Create necessary folders if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)

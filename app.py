from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import time
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

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify Railway connectivity"""
    return jsonify({'status': 'Railway backend is working!', 'timestamp': str(time.time())})

@app.route('/test-upload', methods=['POST'])
def test_upload():
    """Test POST requests without files"""
    print(f"🧪 Test upload request received at {time.time()}")
    data = request.get_json() if request.is_json else request.form.to_dict()
    print(f"🧪 Request data: {data}")
    return jsonify({
        'status': 'POST request successful!', 
        'received_data': data,
        'timestamp': str(time.time())
    })

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        print(f"🔍 Upload request received - Form keys: {list(request.files.keys())}")
        print(f"🔍 Request form data: {dict(request.form)}")
        
        if 'file' not in request.files:
            print(f"❌ No 'file' key in request.files: {list(request.files.keys())}")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"🔍 File object: {file}, filename: {file.filename}")
        
        if file.filename == '':
            print(f"❌ Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file size (limit to 50MB for Railway)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > 25 * 1024 * 1024:  # 25MB limit for Railway stability
            return jsonify({'error': 'File too large. Please upload a video smaller than 25MB.'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            print(f"🔍 Secure filename: {filename}")
            
            # Special handling for test files
            if filename == 'test.txt':
                print(f"✅ Test file detected - Railway file uploads are working!")
                return jsonify({
                    'success': True,
                    'message': 'Test file upload successful! Railway file uploads work.',
                    'filename': filename,
                    'size': file_size
                })
            
            if not allowed_file(file.filename):
                print(f"❌ File type not allowed: {filename}")
                return jsonify({'error': f'Invalid file type. Only mp4, mov, avi files are allowed. Got: {filename}'}), 400
            
            input_video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save uploaded file
            print(f"💾 Saving uploaded file: {filename} ({file_size / (1024*1024):.1f}MB)")
            file.save(input_video_path)

            # Add timeout protection and error handling for processing
            try:
                print(f"🔥 Starting fire detection processing...")
                fire_detected = main(input_video_path, None)
                print(f"✅ Fire detection completed. Fire detected: {fire_detected}")
                
            except Exception as processing_error:
                print(f"❌ Processing error: {str(processing_error)}")
                # Clean up uploaded file on error
                if os.path.exists(input_video_path):
                    os.remove(input_video_path)
                return jsonify({
                    'error': 'Video processing failed. Please try with a smaller or shorter video.',
                    'details': 'The video may be too complex or large to process on this server.'
                }), 500
            
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
                # Still return success but with original video only
                video_url = url_for('serve_video', filename=filename)
            
            response_data = {
                'success': True,
                'message': 'Video processed successfully',
                'fire_detected': fire_detected,
                'emergency_call_status': fire_detected,  # Only call if fire detected
                'video_url': video_url,
                'original_video': url_for('serve_video', filename=filename)
            }
            
            print(f"🚀 Sending response: {response_data}")
            return jsonify(response_data)

        return jsonify({'error': 'Invalid file type. Only mp4, mov, avi files are allowed.'}), 400
        
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return jsonify({
            'error': 'Upload failed due to server error.',
            'details': 'Please try again with a smaller video file.'
        }), 500

if __name__ == '__main__':
    # Create necessary folders if they don't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run in production mode for deployment
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

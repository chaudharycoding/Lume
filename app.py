from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import time
import threading
import json
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

# Global storage for processing status
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video_background(job_id, input_video_path, filename):
    """Background task to process video with YOLO"""
    try:
        print(f"🔥 Starting background processing for job {job_id}")
        print(f"🔥 Video path: {input_video_path}")
        print(f"🔥 File exists: {os.path.exists(input_video_path)}")
        
        processing_status[job_id] = {
            'status': 'processing',
            'message': 'Running fire detection...',
            'progress': 0,
            'start_time': time.time()
        }
        
        # Run fire detection with timeout protection
        print(f"🔥 Calling main() function...")
        
        # Add a processing timeout (8 minutes max)
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Processing timed out after 8 minutes")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(480)  # 8 minutes
        
        try:
            fire_detected = main(input_video_path, None)
            print(f"🔥 main() completed, fire detected: {fire_detected}")
        finally:
            signal.alarm(0)  # Cancel the alarm
        
        # Check if processed video exists
        processed_path = os.path.join('track', filename)
        full_processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_path)
        
        video_url = None
        if os.path.exists(full_processed_path):
            video_url = url_for('serve_video', filename=processed_path)
        else:
            video_url = url_for('serve_video', filename=filename)
        
        # Update status to completed
        processing_status[job_id] = {
            'status': 'completed',
            'message': 'Video processed successfully',
            'fire_detected': fire_detected,
            'emergency_call_status': fire_detected,
            'video_url': video_url,
            'original_video': url_for('serve_video', filename=filename),
            'processing_time': time.time() - processing_status[job_id]['start_time']
        }
        
        print(f"✅ Background processing completed for job {job_id}")
        
    except Exception as e:
        print(f"❌ Background processing failed for job {job_id}: {str(e)}")
        processing_status[job_id] = {
            'status': 'error',
            'message': 'Video processing failed',
            'error': str(e)
        }

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

@app.route('/status/<job_id>', methods=['GET'])
def check_status(job_id):
    """Check processing status of a video"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = processing_status[job_id].copy()
    
    # Add elapsed time for processing jobs
    if status.get('status') == 'processing' and 'start_time' in status:
        status['elapsed_time'] = time.time() - status['start_time']
        print(f"🔍 Status check for {job_id}: {status['status']}, elapsed: {status['elapsed_time']:.1f}s")
    
    return jsonify(status)

@app.route('/debug/jobs', methods=['GET'])
def debug_jobs():
    """Debug endpoint to see all processing jobs"""
    debug_info = {}
    for job_id, status in processing_status.items():
        debug_status = status.copy()
        if 'start_time' in status:
            debug_status['elapsed_time'] = time.time() - status['start_time']
        debug_info[job_id] = debug_status
    return jsonify(debug_info)

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

            # Generate unique job ID
            job_id = f"{int(time.time())}_{filename.replace('.', '_')}"
            
            # Initialize processing status
            processing_status[job_id] = {
                'status': 'uploaded',
                'message': 'Video uploaded successfully, starting processing...',
                'filename': filename,
                'original_video': url_for('serve_video', filename=filename),
                'upload_time': time.time()
            }
            
            # Start background processing
            print(f"🚀 Starting background processing for job: {job_id}")
            thread = threading.Thread(
                target=process_video_background, 
                args=(job_id, input_video_path, filename)
            )
            thread.daemon = True
            thread.start()
            
            # Return immediately with job ID for status checking
            response_data = {
                'success': True,
                'message': 'Video uploaded successfully! Processing in background...',
                'job_id': job_id,
                'status_url': url_for('check_status', job_id=job_id),
                'original_video': url_for('serve_video', filename=filename),
                'estimated_time': '2-5 minutes'
            }
            
            print(f"🚀 Sending immediate response: {response_data}")
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

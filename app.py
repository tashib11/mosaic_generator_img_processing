from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import cv2
import json
import numpy as np
from image_preprocessing import load_images, resize_images
from mosaic_creation import create_mosaic

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        n_segments = int(request.form['n_segments'])
        alpha = float(request.form['alpha'])
        target_file = request.files['target_image']
        
        # Save uploaded image
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'target.jpg')
        target_file.save(target_path)
        
        # Load images
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        tile_images = load_images('mosaic_tiles', output_dir)
        tile_images = resize_images(tile_images, (100, 100), output_dir)
        
        # Create mosaic
        target = cv2.imread(target_path)
        mosaic = create_mosaic(target, tile_images, n_segments, alpha, output_dir)
        
        # Save final result
        cv2.imwrite(f"{output_dir}/final.jpg", mosaic)
        
        return jsonify({'status': 'success', 'n_segments': n_segments, 'alpha': alpha})
    
    return render_template('index.html')

@app.route('/output')
def output():
    n_segments = request.args.get('n_segments', '80')
    alpha = request.args.get('alpha', '0.4')
    return render_template('output.html', n_segments=n_segments, alpha=alpha)

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/tile/<int:x>/<int:y>')
def get_tile(x, y):
    """Get tile at position"""
    output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
    
    # Load segment data
    segments = np.load(f"{output_dir}/segments.npy")
    with open(f"{output_dir}/mapping.json") as f:
        mapping = json.load(f)
    
    # Get segment at position
    seg_id = int(segments[y, x])
    
    if str(seg_id) in mapping:
        tile_file = mapping[str(seg_id)]['filename']
        return jsonify({'success': True, 'tile': f'output/{tile_file}', 'id': seg_id})
    
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True)
import cv2
import os
import json
import numpy as np
from tkinter import Tk, Label, Entry, Button, simpledialog
from image_preprocessing import load_images, resize_images
from mosaic_creation import create_mosaic

def get_user_input():
    """Get number of segments from user"""
    root = Tk()
    root.withdraw()
    n = simpledialog.askinteger("Input", "Number of Superpixels:", initialvalue=80)
    root.destroy()
    return n if n else 80

def on_click(event, x, y, flags, params):
    """Handle mouse click"""
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    
    # Load data
    segments = np.load(f"{params['output']}/segments.npy")
    with open(f"{params['output']}/mapping.json") as f:
        mapping = json.load(f)
    
    # Get clicked segment
    actual_x = int(x / params['scale'])
    actual_y = int(y / params['scale'])
    
    if actual_y >= segments.shape[0] or actual_x >= segments.shape[1]:
        return
    
    seg_id = int(segments[actual_y, actual_x])
    
    # Show tile
    if str(seg_id) in mapping:
        tile_path = f"{params['output']}/{mapping[str(seg_id)]['filename']}"
        if os.path.exists(tile_path):
            tile = cv2.imread(tile_path)
            cv2.imshow(f"Tile {seg_id}", cv2.resize(tile, (400, 400)))

def main():
    # Setup
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load tiles
    print("Loading tiles...")
    tiles = load_images("mosaic_tiles", output_dir)
    tiles = resize_images(tiles, (100, 100), output_dir)
    
    # Load target
    target = cv2.imread("OIP.jpg")
    if target is None:
        print("Error: Target image not found")
        return
    
    # Get user input
    n_segments = get_user_input()
    
    # Create mosaic
    print(f"Creating mosaic with {n_segments} segments...")
    mosaic = create_mosaic(target, tiles, n_segments, alpha=0.4, output_dir=output_dir)
    
    # Display
    h, w = mosaic.shape[:2]
    scale = min(800/w, 600/h)
    display = cv2.resize(mosaic, None, fx=scale, fy=scale)
    
    cv2.namedWindow("Mosaic (Click tiles)")
    cv2.imshow("Mosaic (Click tiles)", display)
    cv2.setMouseCallback("Mosaic (Click tiles)", on_click, 
                        {'output': output_dir, 'scale': scale})
    
    print("\n✅ Done! Click on tiles to see originals")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
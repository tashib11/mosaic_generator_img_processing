import numpy as np
import cv2
import json
from skimage.segmentation import slic, mark_boundaries
from best_match import find_best_match

def create_segments(image, n_segments):
    """Create superpixel segments using SLIC"""
    print(f"Creating {n_segments} superpixels...")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    segments = slic(image_rgb, n_segments=n_segments, compactness=10, sigma=1)
    print(f"Created {len(np.unique(segments))} segments")
    return segments

def visualize_segments(image, segments, output_dir):
    """Show and save segmentation boundaries"""
    # Convert to RGB for visualization
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Mark boundaries (red lines)
    marked = mark_boundaries(image_rgb, segments, color=(1, 0, 0), mode='thick')
    
    # Convert back to BGR for OpenCV
    marked_bgr = (marked * 255).astype(np.uint8)
    marked_bgr = cv2.cvtColor(marked_bgr, cv2.COLOR_RGB2BGR)
    
    # Save
    cv2.imwrite(f"{output_dir}/segmentation.jpg", marked_bgr)
    print(f"Segmentation saved: {output_dir}/segmentation.jpg")
    
    # Display
    cv2.imshow("Superpixel Segmentation", marked_bgr)
    cv2.waitKey(10000)  # Show for 2 seconds
    cv2.destroyWindow("Superpixel Segmentation")
    
    return marked_bgr

def place_tiles(mosaic, target_image, tile_images, segments, output_dir):
    """Place tiles for each segment"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    segment_mapping = {}
    total = len(np.unique(segments))
    
    print(f"Placing tiles for {total} segments...")
    
    for i, seg_id in enumerate(np.unique(segments)):
        # Get segment area
        mask = (segments == seg_id).astype(np.uint8) * 255
        coords = np.argwhere(mask > 0)
        
        if len(coords) == 0:
            continue
            
        y1, x1 = coords.min(axis=0)
        y2, x2 = coords.max(axis=0)
        
        # Skip tiny segments
        if (x2-x1) < 10 or (y2-y1) < 10:
            continue
        
        # Get region and find best tile
        region = target_image[y1:y2, x1:x2]
        best_tile = find_best_match(region, tile_images)
        resized_tile = cv2.resize(best_tile, (x2-x1, y2-y1))
        
        # Place tile
        mosaic[y1:y2, x1:x2][mask[y1:y2, x1:x2] > 0] = resized_tile[mask[y1:y2, x1:x2] > 0]
        
        # Save tile info
        tile_name = f"tile_{seg_id}.jpg"
        cv2.imwrite(f"{output_dir}/{tile_name}", resized_tile)
        segment_mapping[int(seg_id)] = {'filename': tile_name}
        
        if (i+1) % 10 == 0:
            print(f"Progress: {i+1}/{total}")
    
    # Save mapping
    np.save(f"{output_dir}/segments.npy", segments)
    with open(f"{output_dir}/mapping.json", 'w') as f:
        json.dump(segment_mapping, f)
    
    print(f"✅ Done! Placed {len(segment_mapping)} tiles")

def blend_images(mosaic, original, alpha):
    """Blend mosaic with original"""
    return cv2.addWeighted(mosaic, alpha, original, 1-alpha, 0)

def create_mosaic(target_image, tile_images, n_segments=80, alpha=0.4, output_dir='output'):
    """Main function to create mosaic"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*50)
    print("CREATING SUPERPIXEL MOSAIC")
    print("="*50)
    
    # Create segments
    segments = create_segments(target_image, n_segments)
    
    # Visualize segmentation
    visualize_segments(target_image, segments, output_dir)
    
    # Place tiles
    mosaic = target_image.copy()
    place_tiles(mosaic, target_image, tile_images, segments, output_dir)
    
    # Blend
    result = blend_images(mosaic, target_image, alpha)
    
    # Save
    cv2.imwrite(f"{output_dir}/mosaic.jpg", result)
    
    print("="*50)
    print("✅ MOSAIC COMPLETE")
    print("="*50)
    
    return result


# Test code
if __name__ == "__main__":
    from image_preprocessing import load_images, resize_images
    
    print("\nTesting Mosaic Generator\n")
    
    # Load tiles
    tiles = load_images("mosaic_tiles", "output")
    tiles = resize_images(tiles, (100, 100), "output")
    print(f"Loaded {len(tiles)} tiles\n")
    
    # Load target
    img = cv2.imread('OIP.jpg')
    if img is None:
        print("Error: Image not found")
        exit()
    
    # Resize if large
    h, w = img.shape[:2]
    if max(h, w) > 600:
        scale = 600 / max(h, w)
        img = cv2.resize(img, (int(w*scale), int(h*scale)))
    
    # Create mosaic
    result = create_mosaic(img, tiles, n_segments=150, alpha=0.4, output_dir='output')
    
    # Show final result
    cv2.imshow("Final Mosaic", cv2.resize(result, (800, 600)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
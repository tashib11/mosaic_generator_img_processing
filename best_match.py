import numpy as np
import cv2
from image_analysis import average_color, extract_edge_strengths

def color_difference(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))
def edge_similarity(texture1, texture2):
    sims = []
    for t1, t2 in zip(texture1, texture2):
       
        if t1.shape != t2.shape:
            t2 = cv2.resize(t2, (t1.shape[1], t1.shape[0]))
        sims.append(np.linalg.norm(t1 - t2))
    return np.mean(sims)


def find_best_match(target_segment, tile_images, weights=(0.5, 0.5)):
    target_avg_color = average_color(target_segment)
    target_texture = extract_edge_strengths(cv2.cvtColor(target_segment, cv2.COLOR_BGR2GRAY))

    min_score = float('inf')
    best_match = None

    for index, tile in enumerate(tile_images):
        tile_avg_color = average_color(tile)
        tile_texture = extract_edge_strengths(cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY))

        color_diff = color_difference(target_avg_color, tile_avg_color)
        edge_sim = edge_similarity(target_texture, tile_texture)

        score = weights[0] * color_diff + weights[1] * edge_sim
       # print(f"Tile {index}: Color diff: {color_diff}, Edge diff: {edge_sim}, Score: {score}")

        if score < min_score:
            min_score = score
            best_match = tile

    print(f"Best match score(nin): {min_score}")
    return best_match
'''
# ===== TEST CODE =====
if __name__ == "__main__":
    print("Testing best_match.py...")
    
    # Load images
    from image_preprocessing import load_images, resize_images
    
    tile_images = load_images("mosaic_tiles", "output")
    tile_images = resize_images(tile_images, (100, 100), "output")
    print(f"Loaded {len(tile_images)} tiles")
    
    # Create a fake target segment (first tile কে target হিসেবে use করা)
    target_segment = tile_images[0]
    
    # Find best match
    print("\nFinding best match...")
    best_tile = find_best_match(target_segment, tile_images)
    
    if best_tile is not None:
        print("✅ Best match found!")
        # Save for visual verification
        cv2.imwrite("output/best_match_result.jpg", best_tile)
        cv2.imshow('best_matched_title',best_tile)
        print("Result saved: output/best_match_result.jpg")
    else:
        print("❌ No match found")
        
   '''
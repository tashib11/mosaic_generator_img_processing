import numpy as np
import cv2
from best_match import find_best_match

def place_tiles(mosaic, target_image, tile_images, grid_size, output_dir):
    num_rows, num_cols = grid_size
    tile_height = target_image.shape[0] // num_rows
    tile_width = target_image.shape[1] // num_cols

    for row in range(num_rows):
        for col in range(num_cols):
            y1, y2 = row * tile_height, (row + 1) * tile_height
            x1, x2 = col * tile_width, (col + 1) * tile_width
            target_segment = target_image[y1:y2, x1:x2]
            best_tile = find_best_match(target_segment, tile_images)
            resized_tile = cv2.resize(best_tile, (tile_width, tile_height))
            mosaic[y1:y2, x1:x2] = resized_tile
            print(f"Placed tile at ({row}, {col})")
            cv2.imwrite(f"{output_dir}/tile_{row}_{col}.jpg", resized_tile)

def blend_mosaic_with_target(mosaic, target_image, alpha):
    blended = cv2.addWeighted(mosaic, alpha, target_image, 1 - alpha, 0)
    print("Blended mosaic with target image")
    return blended

def create_mosaic(target_image, tile_images, grid_size, alpha, output_dir):
    mosaic = np.zeros_like(target_image)
    place_tiles(mosaic, target_image, tile_images, grid_size, output_dir)
    blended_mosaic = blend_mosaic_with_target(mosaic, target_image, alpha)
    return blended_mosaic



if __name__ == "__main__":
    print("Testing best_match.py...")
    
    # Load images
    from image_preprocessing import load_images, resize_images
    
    tile_images = load_images("mosaic_tiles", "output")
    tile_images = resize_images(tile_images, (100, 100), "output")
    
    img = cv2.imread('input_image.jpg')
    
    res= create_mosaic(img, tile_images, (5,5), 0.3, 'output') 
    
  
    large_res = cv2.resize(res, (1000, 800), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("mosaic", large_res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



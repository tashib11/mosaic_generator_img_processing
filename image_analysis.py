import cv2
import numpy as np

def average_color(image):
    avg_color = cv2.mean(image)[:3] #takes only the first 3 values(BGR)
   # print(f"Average color: {avg_color}")
    return avg_color

def extract_edge_strengths(image):
    gabor_kernels = []
    for theta in np.arange(0, np.pi, np.pi / 4): #np.arange(start=0, stop=180, step=45 -> 0 45 90 135)
        kernel = cv2.getGaborKernel((21, 21), 3, theta, 10, 0.5, 0, ktype=cv2.CV_32F)
        gabor_kernels.append(kernel)

    features = []
    for kernel in gabor_kernels:
        filtered = cv2.filter2D(image, cv2.CV_8UC3, kernel)
        features.append(filtered)
    #print(f"Extracted texture features: {len(features)}")
    return features
'''

# ===== TEST =====
if __name__ == "__main__":
    print("Testing image_analysis.py...")
    
    # Load a test image
    from image_preprocessing import load_images, resize_images
    images = load_images("mosaic_tiles", "output")
    resized = resize_images(images, (100, 100), "output")
    test_img = resized[0]
    
    # Test color analysis
    color = average_color(test_img)

    
    # Test texture analysis
    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    textures = extract_texture_features(gray)
  
    
    print("All tests passed!")
    
    '''
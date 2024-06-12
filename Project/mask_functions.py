import cv2
import numpy as np

def setup_camera():
    return cv2.VideoCapture(0)

def get_kernel():
    return np.ones((11, 11), np.uint8)

def get_color_ranges():
    lower_1_pca = np.array([43, 18, 120])
    upper_1_pca = np.array([103, 255, 255])
    
    lower_2_pca = np.array([103, 51, 100])
    upper_2_pca = np.array([167, 255, 255])
    
    lower_1_pcr = np.array([4, 140, 50])
    upper_1_pcr = np.array([30, 255, 255])
    
    lower_2_pcr = np.array([175, 140, 50])
    upper_2_pcr = np.array([180, 255, 255])
    
    lower_1_prm = np.array([45, 51, 0])
    upper_1_prm = np.array([108, 255, 153])
    
    return {
        'pca': [(lower_1_pca, upper_1_pca), (lower_2_pca, upper_2_pca)],
        'prc': [(lower_1_pcr, upper_1_pcr), (lower_2_pcr, upper_2_pcr)],
        'prm': [(lower_1_prm, upper_1_prm)]
    }

def preprocess_frame(frame):
    img_cropped = frame[int((frame.shape[0])*3/4):(frame.shape[0]), int((frame.shape[1])*1/10):int((frame.shape[1])*9/10)]
    M = (np.ones(img_cropped.shape, np.uint8)) * 80
    gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
    total_pix = np.prod(gray.shape[:2])
    pix = cv2.countNonZero(gray)
    total_density = (pix / total_pix)
    
    if total_density < 0.3:
        img_cropped = cv2.add(img_cropped, M)
    elif total_density > 0.7:
        img_cropped = cv2.subtract(img_cropped, M)
    
    return img_cropped

def apply_mask(img_hsv, ranges):
    masks = [cv2.inRange(img_hsv, lower, upper) for lower, upper in ranges]
    combined_mask = cv2.bitwise_or(masks[0], masks[1]) if len(masks) > 1 else masks[0]
    return combined_mask

def process_mask(img_cropped, mask, kernel):
    result = cv2.bitwise_and(img_cropped, img_cropped, mask=mask)
    smoothed_image = cv2.GaussianBlur(result, (5, 5), 0)
    img_gray = cv2.cvtColor(smoothed_image, cv2.COLOR_RGB2GRAY)
    _, img_th = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
    closing = cv2.morphologyEx(img_th, cv2.MORPH_CLOSE, kernel)
    return closing

def calculate_density(closing):
    total_pix = closing.shape[0] * closing.shape[1]
    num_max_pix = cv2.countNonZero(closing)
    density = num_max_pix / total_pix
    return density

def detect_color(cap, kernel, color_ranges):
    ret, frame = cap.read()
    if not ret:
        return None, None, None
    
    img_cropped = preprocess_frame(frame)
    img_hsv = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2HSV)
    
    densities = {}
    closings = {}
    for color, ranges in color_ranges.items():
        mask = apply_mask(img_hsv, ranges)
        closing = process_mask(img_cropped, mask, kernel)
        density = calculate_density(closing)
        densities[color] = density
        closings[color] = closing
    
    # Determinar cuál color tiene la mayor densidad
    detected_color = max(densities, key=densities.get)
    
    if detected_color == 'pca':
        result = 1
    elif detected_color == 'prm':
        result = 2
    elif detected_color == 'prc':
        result = 3
    else:
        result = None
    
    return result, frame, closings[detected_color]

def show_images(frame, closing):
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Closing Image', closing)



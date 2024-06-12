import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

kernel_close = np.ones((11,11), np.uint8)

clase = input("emocion:" )

## PCA mask ##

lower_1_pca = np.array([43, 18, 120])
upper_1_pca = np.array([103, 255, 255])

lower_2_pca = np.array([103, 51, 100])
upper_2_pca = np.array([167, 255, 255])

## PCR mask ##

lower_1_pcr = np.array([4, 140, 50])
upper_1_pcr = np.array([30, 255, 255])

lower_2_pcr = np.array([175, 140, 50])
upper_2_pcr = np.array([180, 255, 255])

## PRM mask ##

lower_1_prm = np.array([45, 51, 0])
upper_1_prm = np.array([108, 255, 153])

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    img_cropped = frame[int((frame.shape[0])*3/4):(frame.shape[0]), int((frame.shape[1])*1/10):int((frame.shape[1])*9/10)]
    
    M =(np.ones(img_cropped.shape, np.uint8)) * 80
    
    gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
    
    total_pix= np.prod(gray[:2])
    pix = cv2.countNonZero(gray)
    total_density = (pix/total_pix)
    
    
    if total_density < 0.3:
        img_cropped = cv2.add(img_cropped,M)
    elif total_density > 0.7:
        img_cropped = cv2.subtract(img_cropped,M)
    else:
        img_cropped = img_cropped
    
    
    img_hsv = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2HSV)
    
    ### PCA mask ### green, blue and purple colors
    mask1_pca = cv2.inRange(img_hsv, lower_1_pca, upper_1_pca)
    mask2_pca = cv2.inRange(img_hsv, lower_2_pca, upper_2_pca)
    
    mask_pca = cv2.bitwise_or(mask1_pca, mask2_pca)
    
    result_pca = cv2.bitwise_and(img_cropped, img_cropped, mask=mask_pca)
    
    smoothed_image_pca = cv2.GaussianBlur(result_pca,(5,5),0)
    img_gray_pca = cv2.cvtColor(smoothed_image_pca, cv2.COLOR_RGB2GRAY)
    _, img_th_pca = cv2.threshold(img_gray_pca, 1, 255, cv2.THRESH_BINARY)
    closing_pca = cv2.morphologyEx(img_th_pca, cv2.MORPH_CLOSE, kernel_close)
    
    
    ### PRC mask ### red and yellow colors
    
    mask1_pcr = cv2.inRange(img_hsv, lower_1_pcr, upper_1_pcr)
    mask2_pcr = cv2.inRange(img_hsv, lower_2_pcr, upper_2_pcr)
    
    mask_pcr = cv2.bitwise_or(mask1_pcr, mask2_pcr)
    
    result_pcr = cv2.bitwise_and(img_cropped, img_cropped, mask=mask_pcr)
    
    smoothed_image_pcr = cv2.GaussianBlur(result_pcr,(25,25),0)
    img_gray_pcr = cv2.cvtColor(smoothed_image_pcr, cv2.COLOR_RGB2GRAY)
    _, img_th_pcr = cv2.threshold(img_gray_pcr, 1, 255, cv2.THRESH_BINARY)
    closing_pcr = cv2.morphologyEx(img_th_pcr, cv2.MORPH_CLOSE, kernel_close)
    
    ## PRM mask ## green colors
    
    mask_prm = cv2.inRange(img_hsv, lower_1_prm, upper_1_prm)
    
    result_prm = cv2.bitwise_and(img_cropped, img_cropped, mask=mask_prm)
    
    smoothed_image_prm = cv2.GaussianBlur(result_prm,(5,5),0)
    img_gray_prm = cv2.cvtColor(smoothed_image_prm, cv2.COLOR_RGB2GRAY)
    _, img_th_prm = cv2.threshold(img_gray_prm, 1, 255, cv2.THRESH_BINARY)
    closing_prm = cv2.morphologyEx(img_th_prm, cv2.MORPH_CLOSE, kernel_close)
    
    
    ## Densities ##
     
    total_pix_prm = closing_prm.shape[0] * closing_prm.shape[1]
    num_max_pix_prm = cv2.countNonZero(closing_prm)
    density_prm = num_max_pix_prm/total_pix_prm

    total_pix_pca = closing_pca.shape[0] * closing_pca.shape[1]
    num_max_pix_pca = cv2.countNonZero(closing_pca)
    density_pca = num_max_pix_pca/total_pix_pca
    
    total_pix_pcr = closing_pcr.shape[0] * closing_pcr.shape[1]
    num_max_pix_pcr = cv2.countNonZero(closing_pcr)
    density_pcr = num_max_pix_pcr/total_pix_pcr
        
    if (density_pca > 0.4):
        print("PCA")
    elif (density_prm > 0.4):
        print("PRM")
    elif (density_pcr > 0.4):
        print("PRC")
    else:
        print("nada")

    cv2.imshow('Imagen Original', frame)

    cv2.imshow('mask_pcr', closing_pcr)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
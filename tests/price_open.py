import cv2
import pytesseract
import numpy as np
from PIL import Image

#--------------------------------------------------------------------------------#

# Yellow color processing

def yellow_processing(image):

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define yellow range
    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([40, 255, 255])

    # Mask for yellow regions
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_region = cv2.bitwise_and(image, image, mask=mask)

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(yellow_region, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the image to make text dark on light background
    # inverted = 255 - thresh

    # Optional: Find contours and crop around the yellow box
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour is the yellow box
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cropped = image[y:y+h, x:x+w]
        
        # Convert cropped area to PIL image for OCR
        pil_cropped = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

        # OCR with relaxed config (for single line of text)
        text = pytesseract.image_to_string(pil_cropped, config='--psm 7')
        print("Detected Text (Cropped):", text.strip())
    else:
        print("No yellow box found.")


#--------------------------------------------------------------------------------#

# Price Open Function

img_path = "tests\CleanShot 2025-04-11 at 10.00.24@2x.png"
image = cv2.imread(img_path)
if image is None:
    raise ValueError(f"Could not load image from path: {img_path}")

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define yellow range
lower_yellow = np.array([15, 50, 50])
upper_yellow = np.array([40, 255, 255])

# Mask for yellow regions
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
yellow_region = cv2.bitwise_and(image, image, mask=mask)

yellow_processing(yellow_region)

#------------------------------------------------------#





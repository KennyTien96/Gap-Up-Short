import cv2
import pytesseract
import numpy as np
import re
import os

def load_image(path):
    return cv2.imread(path)

def find_yellow_regions(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 150])
    upper_yellow = np.array([35, 255, 255])
    return cv2.inRange(hsv, lower_yellow, upper_yellow)

def extract_yellow_boxes(image, mask, min_area=200):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > min_area:
            boxes.append(image[y:y+h, x:x+w])
    return boxes

def enhance_for_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
    enhanced = clahe.apply(gray)
    
    binary = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)[1]
    inverted = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY_INV)[1]
    
    resized_binary = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    resized_inverted = cv2.resize(inverted, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    
    return resized_binary, resized_inverted

def extract_text_from_boxes(boxes, debug_dir="debug_crops"):
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    for i, box in enumerate(boxes):
        binary, inverted = enhance_for_ocr(box)
        cv2.imwrite(f"{debug_dir}/box_{i}_binary.png", binary)
        cv2.imwrite(f"{debug_dir}/box_{i}_inverted.png", inverted)

        for version_name, img in [("binary", binary), ("inverted", inverted)]:
            text = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789.')
            cleaned = re.findall(r"\d+\.\d+", text)
            if cleaned:
                print(f"[OCR Success] Box {i} ({version_name}):", cleaned[0])
                return cleaned[0]
            else:
                print(f"[OCR Fail] Box {i} ({version_name}):", repr(text.strip()))
    return None

def extract_yellow_price_from_image(path):
    image = load_image(path)
    yellow_mask = find_yellow_regions(image)
    yellow_boxes = extract_yellow_boxes(image, yellow_mask)
    if not yellow_boxes:
        print("No yellow boxes found.")
        return None
    value = extract_text_from_boxes(yellow_boxes)
    return value

# Example usage
if __name__ == "__main__":
    image_path = "tests\error_price.png"
    result = extract_yellow_price_from_image(image_path)
    print("Detected Yellow Price:", result if result else "None detected")


# Gap_Up_Short 2025-04-28 at 08.20.24@2x
# Gap_Up_Short 2025-04-28 at 08.57.09@2x
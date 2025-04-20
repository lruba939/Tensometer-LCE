import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import IPython.display as display
from PIL import Image

# Funkcja do wykrywania i binaryzacji niebieskiego prostokąta
def process_blue_rectangle(image, frame_number):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Zakresy kolorów niebieskich (różne odcienie)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Maska dla niebieskich obszarów
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Znalezienie konturów niebieskiego prostokąta
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Nie znaleziono niebieskiego prostokąta.")
        return None

    # Wybór największego konturu (zakładamy, że to ekran LCD)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Kadrowanie do prostokąta
    cropped = image[y:y+h, x:x+w]

    # Konwersja do skali szarości i binaryzacja
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    # Poprawienie kontrastu przez equalizację histogramu
    gray = cv2.equalizeHist(gray)

    img = cv2.medianBlur(cropped[:,:,0].astype(np.uint8), 11)
     
    adaptive_threshold_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
    
    adaptive_threshold_mean = cv2.morphologyEx(adaptive_threshold_mean, cv2.MORPH_ERODE, np.ones((3,3)))
    
    resized_image = cv2.resize(adaptive_threshold_mean, (200, 80))
    
    binary_file_name = "binaries/" + str(frame_number) + "_binary.png"
    
    cv2.imwrite(binary_file_name, resized_image)  # Zapisz zdjęcie do pliku

    # Wyświetlenie wyników
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.title("Oryginalne zdjęcie")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Wykadrowany prostokąt")
    plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Binaryzacja")
    plt.imshow(resized_image, cmap="gray")
    plt.axis("off")
    
    post_process_img_name = "vid2img/" + str(frame_number) + "_img.png"
    
    plt.savefig(post_process_img_name)
    
    plt.close('all')
    
    return frame_number
    

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Nie można otworzyć pliku wideo.")
        return
    
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_img = process_blue_rectangle(frame, frame_number)
        
        display.clear_output(wait=True)
        display.display(processed_img)
        
        time.sleep(1 / 24)  # Założony FPS = 24
        frame_number += 1
    
    cap.release()
    display.clear_output()

# Ścieżka do nagranego pliku
video_path = "tensometer/06.04.2025_01.40/06.04.2025_01.40.mp4"

# Wywołanie funkcji przetwarzającej wideo
process_video(video_path)
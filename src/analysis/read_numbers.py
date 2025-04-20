import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Segments:
    def __init__(self):
        # create a 7seg model
        self.flags = [];
        self.segments = [];
        h1 = [[0.25, 0.75],[0.05, 0.20]];       # 0
        h2 = [[0.25, 0.75],[0.42, 0.58]];   # 1
        h3 = [[0.25, 0.75],[0.80, 0.95]];     # 2
        vl1 = [[0.1, 0.4],[0.15, 0.4]];      # 3 # upper-left
        vl2 = [[0.1, 0.4],[0.55, 0.85]];    # 4
        vr1 = [[0.6, 0.9],[0.15, 0.4]];    # 5 # upper-right
        vr2 = [[0.6, 0.9], [0.55, 0.85]]; # 6
        self.segments.append(h1);
        self.segments.append(h2);
        self.segments.append(h3);
        self.segments.append(vl1);
        self.segments.append(vl2);
        self.segments.append(vr1);
        self.segments.append(vr2);

    # returns the stored number (stored in self.flags)
    def getNum(self):
        # hardcoding outputs
        if self.flags == [0,2,3,4,5,6]:
            return 0;
        if self.flags == [5,6]:
            return 1;
        if self.flags == [0,1,2,4,5]:
            return 2;
        if self.flags == [0,1,2,5,6]:
            return 3;
        if self.flags == [1,3,5,6]:
            return 4;
        if self.flags == [0,1,2,3,6]:
            return 5;
        if self.flags == [0,1,2,3,4,6]:
            return 6;
        if self.flags == [0,5,6]:
            return 7;
        if self.flags == [0,1,2,3,4,5,6]:
            return 8;
        if self.flags == [0,1,2,3,5,6]:
            return 9;
        # ERROR
        return -1;
    
def black_white_ratio(binary_image, x1, y1, x2, y2):
    """
    Oblicza stosunek pikseli czarnych do białych w zadanym regionie obrazu binarnego.
    
    Parametry:
    - binary_image: obraz binarny (0 - czarny, 255 - biały)
    - x1, y1: współrzędne lewego górnego rogu regionu
    - x2, y2: współrzędne prawego dolnego rogu regionu
    
    Zwraca:
    - Stosunek czarnych pikseli do białych (black/white)
    """
    # Wycięcie interesującego regionu
    region = binary_image[y1:y2, x1:x2]

    # Liczenie czarnych i białych pikseli
    white_pixels = np.count_nonzero(region == 255)  # Piksele białe (255)
    black_pixels = np.count_nonzero(region == 0)    # Piksele czarne (0)

    # Unikanie dzielenia przez zero
    if white_pixels == 0:
        return float('inf')  # Jeśli nie ma białych pikseli, stosunek → nieskończoność

    return black_pixels / white_pixels
    
folder_path = "binaries/"
# img_number = 18

box_boundry = np.array([[160, 160+29], [10, 10 + 54]]) # [[x0, x],[y0, y]]

# Wymiary prostokąta (x, y, szerokość, wysokość)
x_start = box_boundry[0,0]   # Pozycja y lewego dolnego rogu
y = box_boundry[1,0]   # Pozycja x lewego dolnego rogu
width = box_boundry[0,1]-box_boundry[0,0]  # Szerokość prostokąta
height = box_boundry[1,1]-box_boundry[1,0]  # Wysokość prostokąta

numbers_vec = []

for f in range(413):
    img_number = f
    img_path = folder_path + str(img_number) + "_binary.png"
    binary_img = cv2.imread(img_path)

    # Tworzymy figurę i osie
    fig, ax = plt.subplots()
    ax.imshow(binary_img)

    numbers = []

    for j in range(5):
        
        x = x_start - width*j
        
        rectangle = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='red', facecolor='none')

        # Dodajemy prostokąt do osi
        ax.add_patch(rectangle)

        model = Segments()

        for i in range(len(model.segments[:])):
            rectangle_boundry = np.array(model.segments[i]) * np.array([[width, width], [height, height]]) + np.array([[x, x], [y, y]])
            
            rectangle_boundry = np.uint8(np.round(rectangle_boundry))
            # print(rectangle_boundry)
            
            [[x1, x2], [y1, y2]] = rectangle_boundry # Region do analizy
            ratio = black_white_ratio(binary_img, x1, y1, x2, y2)

            if ratio > 0.5:
                
                model.flags.append(i)
                
                x_s = rectangle_boundry[0,0]   # Pozycja y lewego dolnego rogu
                y_s = rectangle_boundry[1,0]   # Pozycja x lewego dolnego rogu
                width_s = rectangle_boundry[0,1]-rectangle_boundry[0,0]  # Szerokość prostokąta
                height_s = rectangle_boundry[1,1]-rectangle_boundry[1,0]  # Wysokość prostokąta
                
                rectangle = patches.Rectangle((x_s, y_s), width_s, height_s, linewidth=2, edgecolor='blue', facecolor='blue')

                # Dodajemy prostokąt do osi
                ax.add_patch(rectangle)
                
        if len(model.flags) == 0:
            break
        
        # print(model.flags)
        
        numbers.append(model.getNum())
        
    if -1 in numbers:
        x = np.nan
    else:
        x = sum(x*10**i for i, x in enumerate(numbers) if x >= 0)/100
    
    print("Frame: ", f, ";  Time:", 1/24*f , ";    Value: ", x)

    print(numbers)

    # # Wyświetlamy wykres
    # plt.show()
    
    numbers_vec.append([f, 1/24*f, x])
    
numbers_vec = np.array(numbers_vec)
    
clean_data = numbers_vec[~np.isnan(numbers_vec).any(axis=1)]
    
np.savetxt("dupa.dat", clean_data, fmt='%d %.2f %.2f')
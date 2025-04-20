import tkinter as tk
from tkinter import ttk, simpledialog
from multiprocessing import Process, Queue
import datetime
import csv
import numpy as np
from PIL import Image, ImageTk
import time

from src.camera.camera_saver import *
from src.mcu.mcu_reader import read_serial
from src.plots.plots import update_plot

# Zmienne globalne
camera_index = None
recording = False
process_frame_saver = None
video_queue = Queue()
process_MCU_data = None
data_queue = Queue()
data_log = []
data_to_save = []
csv_file = None
csv_writer = None
filename = ""
recording_folder = ""
process_plot = None
data_plot_queue = Queue()
plot_queue = Queue()

# Zmienne globalne dla GUI
root = None
recording_indicator = None
recording_label = None
camera_label = None
start_plot_index = 0
fig = None
canvas_frames = []


def create_GUI(cam_idx):
    global root, recording_indicator, recording_label, camera_label, canvas_frames, camera_index
    camera_index = cam_idx
    
    gui_color = "#222222"

    root = tk.Tk()
    root.title("STM32 Data Logger")
    root.geometry("1920x1080")
    root.configure(bg=gui_color)

    canvas_frames = []

    # Podgląd z kamerki z ramką
    camera_frame = tk.Frame(root, bg=gui_color, width=480, height=270)  # Szara ramka
    camera_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    camera_label = tk.Label(camera_frame, bg=gui_color)
    camera_label.pack(fill="both", expand=True)

    # Wskaźnik nagrywania
    recording_indicator = tk.Label(root, bg=gui_color, fg="red", font=("Arial", 20))
    recording_indicator.grid(row=0, column=0, sticky="ne", padx=20, pady=10)

    # Nazwa pliku nagrania
    recording_label = tk.Label(root, bg=gui_color, fg="white", font=("Arial", 12))
    recording_label.grid(row=2, column=0, sticky="ew", padx=20)

    # Kontener na wykresy (2x2)
    plots_frame = tk.Frame(root, bg=gui_color)
    plots_frame.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

    for row in range(2):
        for col in range(2):
            canvas = tk.Canvas(plots_frame, relief="solid", bg="white", width=600, height=420)
            canvas.grid(row=row, column=col, padx=10, pady=10)
            canvas_frames.append(canvas)

    # Przyciski sterujące w centrum kolumny
    button_frame = tk.Frame(root, bg=gui_color)
    button_frame.grid(row=3, column=0, pady=10, sticky="ew")

    # Wyśrodkowanie przycisków w kolumnie
    root.grid_columnconfigure(0, weight=1)  # Zapewnia, że kolumna z przyciskami może się rozciągać
    button_frame.grid_columnconfigure(0, weight=1)  # Wyśrodkowanie przycisków

    # Dodawanie przycisków
    ttk.Button(button_frame, text="Record", command=start_recording).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Stop", command=stop_recording).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Generate .mp4", command=create_movie).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Reset", command=reset_plots).grid(row=0, column=3, padx=5)

    # Waga kolumn w button_frame - dzięki temu przyciski są wyśrodkowane
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)

    # Ustawienie wagi w wierszach
    root.grid_rowconfigure(0, weight=1)  # Przydzielanie wagi dla wiersza z kamerą i wykresami
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)  # Daje wagę wierszowi z przyciskami

    return root

# Funkcja obsługi kamerki
def camera_stream():
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Nie udało się otworzyć kamery!")
        return
    while True:
        ret, frame = cap.read()
        if ret:
            img_tk = tk.PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())
            camera_label.config(image=img_tk)
            camera_label.image = img_tk
            
            if recording:
                video_queue.put(frame)
        root.update_idletasks()
    cap.release()
    
def MCU_comunication():
    global process_MCU_data, data_queue
    
    process_MCU_data = Process(target=read_serial, args=[data_queue], daemon=True)
    process_MCU_data.start()
    
def MCU_collect_data():
    global data_log, data_queue, data_to_save
    while True:
        root.update_idletasks()
        try:
            data_log.append(data_queue.get_nowait())
        except:
            time.sleep(0.1)
            continue
        if recording:
            data_to_save.append(data_log[-1])

# Rozpoczęcie nagrywania
def start_recording():
    global recording, process_frame_saver, process_MCU_data, csv_file, csv_writer, data_queue, filename, recording_folder, data_to_save
    
    recording = True

    # Zapisywanie zdjęć do plików w folderze
    filename = datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")
    recording_folder = f"records/{filename}"
    os.makedirs(recording_folder, exist_ok=True)

    process_frame_saver = Process(target=frame_saver, args=(video_queue, recording_folder), daemon=True)
    process_frame_saver.start()
    
    # GUI
    recording_label.config(text=f"Recording: {recording_folder}", fg="red")
    toggle_recording_indicator()
    
    # Zapisywanie danych z MCU do csv
    data_to_save = []
    
    csv_file = open(os.path.join(recording_folder, f"{filename}.csv"), 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Time[s]", "Temperature[V]", "Light[V]"])
    

# Zatrzymanie nagrywania
def stop_recording():
    global recording, process_frame_saver, process_MCU_data, csv_file, csv_writer, data_queue, filename, recording_folder, data_to_save
    
    recording = False
    
    video_queue.put(None)
    
    if process_frame_saver:
        process_frame_saver.join()
        process_frame_saver = None
    
    if csv_file:
        data_to_save = np.array(data_to_save)
        # data_to_save[:,0] = data_to_save[:,0] - data_to_save[0,0] # Czas liczony jest od podłączenia MCU do PC, dlatego dla danych z konkretnego pomiaru robimy przesunięcie do 0 s
        for row in data_to_save:
            csv_writer.writerow(row)
        csv_file.close()
        csv_file = None
        
    recording_label.config(text="")
    recording_indicator.config(text="")
    
# Migający wskaźnik nagrywania
def toggle_recording_indicator():
    if recording:
        recording_indicator.config(text="⬤" if recording_indicator.cget("text") == "" else "", fg="red")
        root.after(500, toggle_recording_indicator)    
            
# Tworzenie filmu ze zdjec
def create_movie():
    video_name = os.path.join(recording_folder, filename + '.mp4')

    images = sorted([img for img in os.listdir(recording_folder) if img.endswith(".png")])
    frame = cv2.imread(os.path.join(recording_folder, images[0]))
    height, width, _ = frame.shape

    video =cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24.0, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(recording_folder, image)))

    video.release()
    
def create_plot():
    global process_plot, plot_queue, data_plot_queue
    
    process_plot = Process(target=update_plot, args=[data_plot_queue, plot_queue], daemon=True)
    process_plot.start()

def get_plot():
    global data_plot_queue, plot_queue, root, canvas_frames, data_log, start_plot_index
    last = 0
    obrazki = [None] * 4  # referencje do PhotoImage, żeby ich nie zjadł GC

    while True:
        root.update_idletasks()
        if not data_log or len(data_log) - start_plot_index == last:
            time.sleep(0.1)
            continue

        data_plot_queue.put(data_log[start_plot_index:])
        last = len(data_log) - start_plot_index

        paths = None
        while paths is None:
            root.update_idletasks()
            try:
                paths = plot_queue.get_nowait()
            except Exception as e:
                time.sleep(0.1)

        try:
            for i in range(4):
                img = Image.open(paths[i])
                img = img.resize((600, 420))
                photo = ImageTk.PhotoImage(img)
                obrazki[i] = photo  # zachowaj referencję, żeby obraz nie znikł

                canvas = canvas_frames[i]
                canvas.delete("all")  # wyczyść poprzedni obraz
                canvas.config(width=photo.width(), height=photo.height())
                canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            print("Błąd podczas ładowania obrazów:", e)

        time.sleep(0.1)


# Reset wykresów
def reset_plots():
    global start_plot_index
    start_plot_index = len(data_log) - 1
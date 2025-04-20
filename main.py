import threading
from src.gui.gui import *

def main():
    global camera_index
    
    # Ręczne wpisanie numeru kamery
    camera_index = simpledialog.askinteger("Wybór kamery", "Podaj numer kamery:", minvalue=0, maxvalue=9)
    
    root = create_GUI(camera_index)
    
    # Uruchomienie wątku kamery
    threading.Thread(target=camera_stream, daemon=True).start()
    
    # Nawiązanie komunikacji z MCU
    MCU_comunication()
    # Uruchomienie wątku MCU
    threading.Thread(target=MCU_collect_data, daemon=True).start()
    
    create_plot()
    # Uruchomienie wątku plottera
    threading.Thread(target=get_plot, daemon=True).start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
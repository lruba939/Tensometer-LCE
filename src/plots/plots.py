import numpy as np
import matplotlib.pyplot as plt
import os

# Kolory
# Program Catalog Color Palette, https://www.color-hex.com/color-palette/894
temp_color = "#cc2a36"
light_color = "#edc951"

def plotter(x, y, color, y_label, plot_label):

    fontsize = 14
    
    fig, ax = plt.subplots(figsize = (6.0, 4.2))
    ax.plot(x, y, color=color, label=plot_label)
    
    ax.set_xlabel('Time [s]', fontsize = fontsize)
    ax.set_ylabel(y_label, fontsize = fontsize)
    
    ax.tick_params(direction="in", which="both", top=True, right=True)
    ax.set_title(plot_label, fontsize=fontsize)
    # ax.legend(loc='upper left', frameon=False, fontsize = fontsize)
    
    return fig, ax  # zwraca obiekt figury i osi

# Aktualizacja wykresów
def update_plot(in_queue, out_queue, folder='src/gui/pics'):
    os.makedirs(folder, exist_ok=True)
    
    while True:
        data_log = in_queue.get()
        data_log = np.array(data_log)

        time_data = data_log[:, 0]
        temp_data = data_log[:, 1]
        light_data = data_log[:, 2]

        y_label_temp = "Voltage [V]"
        y_label_light = "Voltage [V]"

        fig_t_t, _ = plotter(time_data[-100:], temp_data[-100:], temp_color, y_label_temp, "Temperature")
        fig_t_l, _ = plotter(time_data[-100:], light_data[-100:], light_color, y_label_light, "Light intensity")
        fig_t_t_full, _ = plotter(time_data, temp_data, temp_color, y_label_temp, "Temp. full time")
        fig_t_l_full, _ = plotter(time_data, light_data, light_color, y_label_light, "Light full time")

        def save_fig(fig, name):
            path = os.path.join(folder, f"{name}.png")
            fig.savefig(path, dpi=100, bbox_inches='tight')
            plt.close(fig)
            return path

        paths = [
            save_fig(fig_t_t, "temp_short"),
            save_fig(fig_t_l, "light_short"),
            save_fig(fig_t_t_full, "temp_full"),
            save_fig(fig_t_l_full, "light_full"),
        ]
        
        out_queue.put(paths)
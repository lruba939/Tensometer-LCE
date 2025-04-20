import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# Ustawienia bibliotek
plt.ioff() # Turn interactive plotting off
## Font
rcParams['font.family'] = 'Arial'
rcParams['font.size'] = 14

## Lines
rcParams['lines.solid_joinstyle'] = 'miter'  # other options: 'round' or 'bevel'
rcParams['lines.antialiased'] = True  # turning on/off of antialiasing for sharper edges
rcParams['lines.linewidth'] = 1.25

## Legend
rcParams['legend.loc'] = 'upper left'
rcParams['legend.frameon'] = False

## Ticks
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['xtick.top'] = True
rcParams['ytick.right'] = True

rcParams['xtick.minor.visible'] = True
rcParams['ytick.minor.visible'] = True

## Resolution
rcParams['figure.dpi'] = 150

## Colors
### Palettes from color-hex.com/
c_google = ['#008744', '#0057e7', '#d62d20', '#ffa700'] # G, B, R, Y # https://www.color-hex.com/color-palette/1872
c_twilight = ['#363b74', '#673888', '#ef4f91', '#c79dd7', '#4d1b7b'] # https://www.color-hex.com/color-palette/809

temp_color = "#cc2a36" # Program Catalog Color Palette, https://www.color-hex.com/color-palette/894
light_color = "#edc951" 

def plotter(x, y, color, y_label, plot_label):
    fig, ax = plt.subplots(figsize = (6.0, 4.2))
    ax.plot(x, y, color=color, label=plot_label)
    
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(y_label)
    
    ax.set_title(plot_label)
    # ax.legend(loc='upper left', frameon=False)
    
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
# Tensometer for Liquid Crystal Elastomers (LCE)

This project is a data logging and visualization tool designed to work with an STM32F103C8T6 microcontroller and a USB webcam to measure mechanical response in thin-film Liquid Crystal Elastomers (LCEs). It is a part of the master's thesis project **Variable geometry optical elements utilising liquid crystal elastomers**.

## Project Description

The application communicates with an STM32F103C8T6 microcontroller that collects data from:

- A PT1000 temperature sensor
- A BPW20RF photodiode

Simultaneously, a USB webcam photographs the display of a digital jewelry scale. This scale serves as a custom-built tensometer, measuring the deformation forces acting on an LCE film during an experiment.

The software performs the following tasks:

- Displays a live video feed from the camera
- Plots temperature and light intensity data from the sensors in real time
- Records data from both the sensors and camera for further analysis

After the experiment, the recorded images are processed to extract weight values over time. These are then used to calculate forces applied to the LCE strip.

## Purpose

This tool enables tension force measurements on thin LCE films fabricated in a laboratory environment. It is a custom solution designed for research in the field of soft matter and smart materials.

## Hardware Requirements

- STM32F103C8T6 microcontroller (with STM32duino bootloader)
- PT1000 temperature sensor
- BPW20RF photodiode
- USB webcam
- Digital jewelry scale with LCD screen

## Software Requirements

Tested on:

- Ubuntu 22.04.5 LTS 64-bit
- Python 3.10.12

Required Python packages:

- matplotlib==3.9.2
- numpy==1.26.4
- pillow==11.1.0
- opencv-python==4.10.0.84
- pyserial==3.5
- tkinter==8.6 (usually included with Python)

Microcontroller environment:

- Arduino IDE 1.8.5
- STM32duino bootloader
- Arduino AVR Boards version 1.6.20

## Setup and Usage

Detailed installation and usage instructions will be provided soon.

## Example Output

Sample screenshots and experimental data visualizations will be added.

## License

License information to be added.

## Author

This project was developed as part of a master's thesis in materials science. AGH University of Krakow.

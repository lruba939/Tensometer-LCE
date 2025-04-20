import serial
import serial.tools.list_ports

# Automatyczne wykrywanie portu STM32 Maple
def find_stm32_port():
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        if "Maple" in port.description or "STM" in port.description:
            return port.device
    return None

def get_serial(port):
    if port:
        ser = serial.Serial(port, 115200, timeout=1)
        return ser
    
    print("STM32F1 Maple nie został znaleziony!")
    exit()

def read_serial(queue):
    port = find_stm32_port()
    ser = get_serial(port)
    
    ser.reset_input_buffer()
    
    while True:
        line = ser.readline().decode().strip()
        if line:
            try:
                t, temp, light = map(float, line.split(','))
                queue.put((t / 1000, temp, light)) # Przechodzimy z [ms] na [s]
            except ValueError as e:
                print(e)
                print("Problem z odczytem danych!")
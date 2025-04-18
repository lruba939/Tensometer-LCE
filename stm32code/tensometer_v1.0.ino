#define ANALOG_PIN_TEMP PA2  // Możesz zmienić na inny pin ADC
#define ANALOG_PIN_LIGHT PA3  // Możesz zmienić na inny pin ADC

const int pinA8 = PA8; // Definicja pinu A8

unsigned long previousMillis_ADC = 0;  // Zmienna przechowująca czas ostatniego odczytu ADC
unsigned long previousMillis_RST = 0;  // Zmienna przechowująca czas ostatniego resetu
const long interval_ADC = 500;  // Czas między odczytami temp i światła w milisekundach
const long interval_weight_RST = 50000;  // Czas między resetami wagi w milisekundach

void setup() {
    Serial.begin(115200);  // Ustawienie komunikacji USB Serial (Maple)
    pinMode(ANALOG_PIN_TEMP, INPUT_ANALOG);  // Ustawienie pinu jako wejście analogowe
    pinMode(ANALOG_PIN_LIGHT, INPUT_ANALOG);  // Ustawienie pinu jako wejście analogowe
    
    pinMode(pinA8, OUTPUT); // Ustawienie pinu jako wyjście
    digitalWrite(pinA8, LOW); // Ustawienie domyślnie niskiego stanu
}

void loop() {
    unsigned long currentMillis = millis();  // Pobranie aktualnego czasu

    // Odczyt ADC co 500 ms
    if (currentMillis - previousMillis_ADC >= interval_ADC) {
        previousMillis_ADC = currentMillis;  // Aktualizacja poprzedniego czasu
        
        // Odczyt temperatury
        uint16_t adc_value_temp = analogRead(ANALOG_PIN_TEMP);  // Odczyt ADC (wartość 0-4095)
        float voltage_temp = adc_value_temp * (3.3 / 4095.0);  // Przeliczenie na napięcie

        // Odczyt światła
        uint16_t adc_value_light = analogRead(ANALOG_PIN_LIGHT);  // Odczyt ADC (wartość 0-4095)
        float voltage_light = adc_value_light * (3.3 / 4095.0);  // Przeliczenie na napięcie

        // Wypisanie wyników w formacie CSV
        Serial.print(currentMillis);
        Serial.print(",");
        Serial.print(voltage_temp, 3);
        Serial.print(",");
        Serial.println(voltage_light, 3);
    }
    
    // Reset wagi co 50 sekund
    if (currentMillis - previousMillis_RST >= interval_weight_RST) {
        previousMillis_RST = currentMillis;  // Aktualizacja poprzedniego czasu
//        Serial.println("Weight reset.");

        digitalWrite(pinA8, HIGH); // Aktywacja pinu
        delay(100); // Czekaj 0.1 sekundy
        digitalWrite(pinA8, LOW); // Dezaktywacja pinu
        delay(100); // Czekaj 0.1 sekundy
        digitalWrite(pinA8, HIGH); // Aktywacja pinu
        delay(100); // Czekaj 0.1 sekundy
        digitalWrite(pinA8, LOW); // Dezaktywacja pinu
    }
}

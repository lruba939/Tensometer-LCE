/*
 * Version 1.1
 */


#define ANALOG_PIN_TEMP PA2  // PT1000 sensor pin (temp.); PA is ADC type pin
#define ANALOG_PIN_LIGHT PA3  // BPW20RF sensor pin (light); PA too!

/* The used jeweler's scale has an automatic turn-off system that activates after one minute of inactivity.
To prevent this during the experiment, the "screen lighting" button is connected to pin PA8.
After 50 seconds of device operation, a sequence of turning the screen lighting off and on is initiated.
As a result, the scale does not turn off even when no measurement is being taken. */
const int pinA8 = PA8;

unsigned long previousMillis_ADC = 0;  // Variable storing the time of the last ADC reading
unsigned long previousMillis_RST = 0;  // Variable storing the time of the last scale screen lighting reset
const long interval_ADC = 500;  // Interval between successive readings from the temperature and light sensors (ms)
const long interval_weight_RST = 50000;  // Interval between screen lighting reset (ms)

void setup() {
    Serial.begin(115200);  // USB Serial (Maple) communication settings
    pinMode(ANALOG_PIN_TEMP, INPUT_ANALOG);
    pinMode(ANALOG_PIN_LIGHT, INPUT_ANALOG);
    
    pinMode(pinA8, OUTPUT);
    digitalWrite(pinA8, LOW); // Deafult state of PA8 is low!
}

void loop() {
    unsigned long currentMillis = millis();  // Reading the current time

    // ADC reading (every 500 ms)
    if (currentMillis - previousMillis_ADC >= interval_ADC) {
        previousMillis_ADC = currentMillis;  // Time update
        
        // Temp. reading
        uint16_t adc_value_temp = analogRead(ANALOG_PIN_TEMP);  // Values in range 0-4095
        float voltage_temp = adc_value_temp * (3.3 / 4095.0);  // Calculating the voltage signal

        // Light reading
        uint16_t adc_value_light = analogRead(ANALOG_PIN_LIGHT);
        float voltage_light = adc_value_light * (3.3 / 4095.0);

        // Writing results in CSV format
        Serial.print(currentMillis);
        Serial.print(",");
        Serial.print(voltage_temp, 3);
        Serial.print(",");
        Serial.println(voltage_light, 3);
    }
    
    // Scale screen reset (every 50 s)
    if (currentMillis - previousMillis_RST >= interval_weight_RST) {
        previousMillis_RST = currentMillis;  // Time update
    //  Serial.println("Weight reset.");

        digitalWrite(pinA8, HIGH);
        delay(100);
        digitalWrite(pinA8, LOW);
        delay(100);
        digitalWrite(pinA8, HIGH);
        delay(100);
        digitalWrite(pinA8, LOW);
    }
}

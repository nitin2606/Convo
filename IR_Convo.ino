const int PIR_SENSOR_OUTPUT_PIN = 2;  // PIR sensor O/P pin

void setup() {
  pinMode(PIR_SENSOR_OUTPUT_PIN, INPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'S') {
      // Send sensor value when 'S' is received
      int sensor_output = digitalRead(PIR_SENSOR_OUTPUT_PIN);
      Serial.println(sensor_output);
    }
  }

  // Your other loop code here
}

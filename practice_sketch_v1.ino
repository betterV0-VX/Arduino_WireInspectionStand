const int pins_input_size = 40;

int time_clk = 10,
    time_reset = 10;

const int pin_clk = A0,
          pin_reset = A1,
          max_number_of_wires = 40;

int cycles = 0;

int pins_input[pins_input_size] = {A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15, 22, 
                                   23, 24, 25, 26, 27, 28, 29, 30,  31,  32,  33,  34,  35,  36, 37,
                                   38, 39, 40, 41, 42, 43, 44, 45,  46,  47}; 
int values[pins_input_size];
int wire_values[pins_input_size];

void setup() {
  Serial.begin(9600);
  pinMode(pin_clk, OUTPUT);
  pinMode(pin_reset, OUTPUT);
  for (int i = 0; i < pins_input_size; i++)
    pinMode(pins_input[i], INPUT);
  Serial.print("\nНачало работы:\n");
}

void tickCLK(int pin, int time) {
  digitalWrite(pin, HIGH);
  delay(time);
  digitalWrite(pin, LOW);
  delay(time);
}

void reset(int pin, int time) {
  digitalWrite(pin, HIGH);
  delay(time);
  digitalWrite(pin, LOW);
}

void printPinStates() {
  Serial.print("Синхросигнал - ");
  Serial.print(cycles);
  Serial.print("; Значения ПИНов - ");
  for (int i = 0; i < pins_input_size; i++) {
    values[i] = digitalRead(pins_input[i]);
    Serial.print(values[i]);
    Serial.print(";");
    if (values[i] == 1) {
      wire_values[i] = cycles+1;
    }
  }
  Serial.println();
}

void printResult() {
  Serial.print("\nРезультат\n");
  for (int i = 0; i < pins_input_size; i++) {
    Serial.print("ПИН: ");
    Serial.print(pins_input[i]);
    Serial.print(" - Провод: ");
    if (wire_values[i] == 0)
      Serial.println("разрыв");
    else
      Serial.println(wire_values[i]);
  }
}

void printRawResult() {
  for (int i = 0; i < pins_input_size; i++) {
    Serial.print(pins_input[i]);
    Serial.print(" ");
    Serial.println(wire_values[i]);
  }
}

void loop() {
  if (cycles == 0) {
    reset(pin_reset, time_reset);
  }

  if (cycles < max_number_of_wires){
    tickCLK(pin_clk, time_clk);
    printPinStates();

  } else {
    Serial.print("Процесс завершен.\n");
    printRawResult();
    cycles = -1;
    //Serial.end();
  }
  delay(100);
  cycles++;
}

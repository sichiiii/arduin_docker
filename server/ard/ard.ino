//#include <ArduinoJson.h>
#include "HX711.h" 

#define DT  2
#define SCK 3

HX711 scale;  

float calibration_factor = 67000;     // поменять                      

int conveer_D5 = 6;
int blade_D7 = 7;
int escape_D6 = 5;
int check_D3 = 4;

void stop(){
  digitalWrite(conveer_D5, HIGH);
  digitalWrite(blade_D7, HIGH);
  digitalWrite(escape_D6, HIGH);
}

float weight = 0.0;
bool check = 0;

unsigned long interval = 0;
unsigned long previousMillis = 0;

float units;
float val1 = 0.0;
bool val2 = 0;

//StaticJsonDocument<200> flask;
//StaticJsonDocument<200> sensors;

void(* resetFunc) (void) = 0;

void setup() {
  Serial.begin(9600);
  scale.begin(DT, SCK);
  scale.tare();
  scale.set_scale(calibration_factor);
  pinMode(conveer_D5, OUTPUT);
  pinMode(blade_D7, OUTPUT);
  pinMode(escape_D6, OUTPUT);
  pinMode(check_D3, INPUT);
  digitalWrite(conveer_D5, HIGH);
  digitalWrite(escape_D6, HIGH);
  digitalWrite(blade_D7, HIGH);
}

void loop() {
    int command = Serial.read();
    if (command == 7){
        resetFunc();
    }
    if (command == 9){
        digitalWrite(conveer_D5, LOW);
        interval = 5000;
    }
    if (command == 0){
        digitalWrite(conveer_D5, LOW);
        interval = 900;
    }
    if (command == 1){
        digitalWrite(blade_D7, LOW);
        interval = 5000;
        check = 0;
    }
    if (command == 2){
        digitalWrite(escape_D6, LOW);
        interval = 200;
        check = 0;
    }
    if (command == 4){
        digitalWrite(escape_D6, LOW);
        interval = 200;
        check = 0;
    }
    if(digitalRead(check_D3)==LOW)  {
        check = 1;
    }
    units = scale.get_units()*0.453592;
    weight = units;
    Serial.print(check);
    Serial.print(',');
    Serial.print(weight);
    Serial.print(',');
    Serial.print(command);
    Serial.println();

    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis > interval) {
      previousMillis = currentMillis;
      stop();
    }
}



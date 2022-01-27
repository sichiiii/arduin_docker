#include <ArduinoJson.h>
#include "HX711.h"  

#define DT  A0
#define SCK A1

HX711 scale;  

float calibration_factor = -14.15;     // поменять                      
float units;                                                  
float ounces; 

int conveer_D5 = 5;
int blade_D7 = 7;
int escape_D6 = 6;
int check_D3 = 3;

float val1 = 0.0;
bool val2 = 0;

StaticJsonDocument<200> flask;
StaticJsonDocument<200> sensors;

void setup() {
  Serial.begin(9600);
  scale.begin(DT, SCK);                                      
  scale.set_scale();                                          
  scale.tare();                                             
  scale.set_scale(calibration_factor);
  pinMode(conveer_D5, OUTPUT);
  pinMode(blade_D7, OUTPUT);
  pinMode(escape_D6, OUTPUT);
  pinMode(check_D3, INPUT);
}

void loop() { 
       String command = Serial.readString();
       if (command == "conveer"){
            digitalWrite(conveer_D5, HIGH);
            delay(5000);   
            digitalWrite(conveer_D5, LOW);
       }
       if (command == "blade"){
            digitalWrite(blade_D7, HIGH);
            delay(5000); 
            digitalWrite(blade_D7, LOW);       
       }
       if (command == "escape"){
            digitalWrite(escape_D6, HIGH);  
            delay(5000); 
            digitalWrite(escape_D6, LOW);
       }
       if (command == "stop"){
            digitalWrite(conveer_D5, LOW);
            digitalWrite(blade_D7, LOW);
            digitalWrite(escape_D6, LOW);
       }
       for (int i = 0; i < 10; i ++) {                             
          units = + scale.get_units(), 10;                         
       }
       if(digitalRead(check_D3)==LOW)  {   
         sensors["check"] = "True";     
       }
       else  {                     
         sensors["check"] = "False";      
       }
       units = units / 10;                                       
       ounces = units * 0.035274;      
       sensors["weight"] = ounces;
       delay(500); 
       serializeJson(sensors, Serial);
}

  

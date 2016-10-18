#include "CmdMessenger.h"
#include <Thread.h>
#include <ThreadController.h>

/* Define available CmdMessenger commands */
enum {
    roll_out,
    get_temp,
    get_length,
    error,
    temp_is,
    rollout_done,
    length_is,
    get_light,
    light_is,
    set_temp_threshold,
    set_light_threshold
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');
int rollout = 0;
int lightThreshold = 0;
int tempThreshold = 0;

/* Create callback functions to deal with incoming messages */

void on_set_temp_threshold(void) {
  int setValue = c.readBinArg<int>();
  tempThreshold = setValue;
}

void on_set_light_threshold(void) {
  int setValue = c.readBinArg<int>();
  lightThreshold = setValue;
}

void on_get_light(void) {
  int light = getLight();
  c.sendCmd(light_is, light);
}

void on_get_temp(void) {
  float temp = getTemp();
  temp = roundf(temp);
  temp = (int) temp;
  c.sendCmd(temp_is, temp);
}

void on_get_length(void) {

  c.sendCmd(length_is, rollout);
}

void on_roll_out(void) {
  int rolValue = c.readBinArg<int>();
  rollout = rolValue;
  /* Blink led */
  pinMode(2, OUTPUT);
  int i = 0;
  while( i < rolValue) {
    digitalWrite(2, HIGH);
    delay(50);
    digitalWrite(2, LOW);
    delay(20);
    i += 2;
  }
  c.sendCmd(rollout_done, "Rollout complete");
}



/* callback */
void on_unknown_command(void){
    c.sendCmd(error,"Command without callback.");
}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) {

    c.attach(get_temp,on_get_temp);
    c.attach(get_light,on_get_light);
    c.attach(get_length,on_get_length);
    c.attach(roll_out, on_roll_out);
    c.attach(set_temp_threshold, on_set_temp_threshold);
    c.attach(set_light_threshold, on_set_light_threshold);
    c.attach(on_unknown_command);
}

float getTemp() {
  int reading = analogRead(0);

 // converting that reading to voltage, for 3.3v arduino use 3.3
  float voltage = reading * 5.0;
  voltage /= 1024.0;

 // print out the voltage

 // now print out the temperature
  float temperatureC = (voltage - 0.5) * 100 ;  //converting from 10 mv per degree wit 500 mV offset
                                               //to degrees ((voltage - 500mV) times 100)
   return temperatureC;
}

int getLight() {
  int lightPin = 1;
  int lightReading;

  lightReading = analogRead(lightPin);

    return lightReading;
}

void setup() {
    Serial.begin(BAUD_RATE);
    attach_callbacks();    
}

void loop() {
    c.feedinSerialData();
}

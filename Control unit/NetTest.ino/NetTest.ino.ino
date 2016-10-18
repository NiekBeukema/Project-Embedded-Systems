#include "CmdMessenger.h"

/* Define available CmdMessenger commands */
enum {
    roll_out,
    get_temp,
    get_length,
    get_type,
    type_is,
    temp_is,
    length_is,
    rollout_done,
    error,
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');
int rollout = 0;

/* Create callback functions to deal with incoming messages */

/* callback */
void on_get_type(void){
    c.sendCmd(type_is, "temp");
}

void on_get_temp(void) {
  c.sendCmd(temp_is, 25);
}

void on_get_length(void) {
  c.sendCmd(length_is, rollout);
}

void on_roll_out(void) {
  int rolValue = c.readBinArg<int>();
  rollout = rolValue;
  c.sendCmd(rollout_done, "Rollout complete");
}


/* callback */
void on_unknown_command(void){
    c.sendCmd(error,"Command without callback.");
}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
  
    c.attach(get_type,on_get_type);
    c.attach(get_temp,on_get_temp);
    c.attach(get_length,on_get_length);
    c.attach(roll_out, on_roll_out);
    c.attach(on_unknown_command);
}

void setup() {
    Serial.begin(BAUD_RATE);
    attach_callbacks();    
}

void loop() {
    c.feedinSerialData();
}

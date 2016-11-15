#include "CmdMessenger.h"
#include "pt.h"

struct pt pt1, pt2, pt3, pt4;

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
    distance_is,
    light_threshold_is,
    temp_threshold_is,
    get_distance,
    set_temp_threshold,
    set_light_threshold,
    get_light_threshold,
    set_max_rollout,
    get_temp_threshold,
    timer_runtime_end,
    is_rolled_out,
    is_rolled_out_is
};


/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');
bool isAuto = false;
int rolledOut = 0;
int lightThreshold = 200; //300 is daglicht
int tempThreshold = 25; // 20 is kamertmep
int temp;
int light;
int maxRollout = 150;


/* Create callback functions to deal with incoming messages */

static int thread1(struct pt *pt, int interval_1, int interval_2)
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
 
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval_1 );
    temp = getTemp();
    light = getLight();
    if((temp > tempThreshold || light > lightThreshold) && rolledOut == 0) {
      thread4(&pt4, true);
    }

    else if((temp < tempThreshold && light < lightThreshold) && rolledOut == 1) {
      thread4(&pt4, false);
    }
    timestamp = millis(); // take a new timestamp
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval_2 );
    if((light > lightThreshold || temp > tempThreshold) && rolledOut == 0) {
      thread4(&pt4, true);
    }

    else if((light < lightThreshold && temp < tempThreshold) && rolledOut == 1) {
      thread4(&pt4, false);
    }
    
    timestamp = millis(); // take a new timestamp
  PT_END(pt);
  }

static int thread2(struct pt *pt, int interval)
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  if(rolledOut == 1) {
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  }

  else {
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
  }
  PT_END(pt);
}

static int thread3(struct pt *pt)
{
  PT_BEGIN(pt);
  c.feedinSerialData();
  PT_END(pt);
}

static int thread4(struct pt *pt, bool rollIn) {
  PT_BEGIN(pt);
  int rolValue;
 if(rollIn) {
    while( getDistance() < maxRollout) {
      digitalWrite(2, HIGH);
      delay(50);
      digitalWrite(2, LOW);
      delay(20);
    }

  }

  else {
    while( getDistance() > 5) {
      digitalWrite(2, HIGH);
      delay(50);
      digitalWrite(2, LOW);
      delay(20);
    }
  }

  /* Blink led */


  if(rollIn) {
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
    rolledOut = 1;
  }

  else {
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
    rolledOut = 0;
  }
  PT_END(pt);
}

void on_get_light(void) {
  c.sendCmd(light_is, getLight());
}

void on_get_distance(void) {
  c.sendCmd(distance_is, getDistance());
}

void on_get_temp(void) {
  c.sendCmd(temp_is, getTemp());
}

void on_get_length(void) {
  c.sendCmd(length_is, 20);
}

void on_roll_out(void) {
  int rollout = c.readBinArg<int>();
  if(rollout == 1) {
    thread4(&pt4, true);
  }

  if(rollout == 0) {
    thread4(&pt4, false);
  }
  
}

void on_get_light_threshold(void) {
  c.sendCmd(light_threshold_is, lightThreshold);
}

void on_get_temp_threshold(void) {
  c.sendCmd(temp_threshold_is, tempThreshold);
}

void on_set_temp_threshold(void) {
   tempThreshold = c.readBinArg<int>();
    c.sendCmd(temp_threshold_is, tempThreshold);
}

void on_is_rolled_out(void) {
    c.sendCmd(is_rolled_out_is, rolledOut);
}

void on_set_light_threshold(void) {
   lightThreshold = c.readBinArg<int>();
  c.sendCmd(light_threshold_is, lightThreshold);
}
/* callback */
void on_unknown_command(void){
    c.sendCmd(error,"Command without callback.");
}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) {

    c.attach(get_temp,on_get_temp);
    c.attach(get_light,on_get_light);
    c.attach(get_distance,on_get_distance);
    c.attach(get_length,on_get_length);
    c.attach(roll_out, on_roll_out);
    c.attach(get_light_threshold, on_get_light_threshold);
    c.attach(get_temp_threshold, on_get_temp_threshold);
    c.attach(set_temp_threshold, on_set_temp_threshold);
    c.attach(set_light_threshold, on_set_light_threshold);
    c.attach(is_rolled_out, on_is_rolled_out);

    c.attach(on_unknown_command);
}

int getTemp() {
  int reading = analogRead(0);

 // converting that reading to voltage, for 3.3v arduino use 3.3
  float voltage = reading * 5.0;
  voltage /= 1024.0;

 // print out the voltage

 // now print out the temperature
  float temperatureC = (voltage - 0.5) * 100 ;  //converting from 10 mv per degree wit 500 mV offset
                                               //to degrees ((voltage - 500mV) times 100
  temp = roundf(temperatureC);
  temp = (int) temp;
   return temperatureC;
}

int getLight() {
  int lightPin = 1;
  int lightReading;

  lightReading = analogRead(lightPin);

    return lightReading;
}

int getDistance() {
  // WISKUNDE TIJD: tijd = afstand/snelheid
  // Snelheid van geluid is 0.034cm/ms
  // UltraSon verstuurt en ontvangt, dus delen door 2
  // s= t*0,034/2

  //Pins instellen
  int trigPin = 8;    //Trig - green Jumper
  int echoPin = 9;    //Echo - yellow Jumper
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  long duration;
  long distance;

  //Voor een goede waarde, begin met een lage pulse.
  //De sensor wordt getriggered door een hoge pulse van 10+ seconden.
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  // Lees echoPin, return in MS
  duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  distance = duration*0.034/2;
  delay(250);
  if(distance < 250){
    return distance;
  } else {
    return 250;
  }
}

int getLightThreshold() {
  return lightThreshold;
}

int getTempThreshold() {
  return tempThreshold;
}

void setup() {
    Serial.begin(BAUD_RATE);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    attach_callbacks();
    PT_INIT(&pt1);
    PT_INIT(&pt2);   
    PT_INIT(&pt3);
  
}

void loop() {
    
    
    //thread1(&pt1, 30000, 10000);
    thread1(&pt1, 5000, 5000);
    thread2(&pt2, 100);
    thread3(&pt3);
}


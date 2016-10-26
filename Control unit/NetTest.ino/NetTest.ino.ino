#include "CmdMessenger.h"
#include "pt.h"

struct pt pt1, pt2;

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
    get_distance,
    set_temp_threshold,
    set_light_threshold,
    timer_runtime_end
};


/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');
bool isAuto = false;
bool rolledOut = false;
int lightThreshold;
int tempThreshold;
int temp;

/* Create callback functions to deal with incoming messages */

static int thread1(struct pt *pt, int interval_1, int interval_2)
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
 
  while(1) {
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval_1 );
    temp = getTemp();
    if(temp > tempThreshold && !rolledOut) {
      rollOut(true);
    }

    else if(temp < tempThreshold && rolledOut) {
      rollOut(false);
    }
    if(!isAuto) {
      c.sendCmd(temp_is, temp);
    }
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval_2 );
    int light = getLight();
    if(light > lightThreshold && !rolledOut) {
      rollOut(true);
    }

    else if(light < lightThreshold && rolledOut) {
      rollOut(false);
    }
    if(!isAuto) {
      c.sendCmd(light_is, light);
    }
    
    timestamp = millis(); // take a new timestamp
  }
  PT_END(pt);
}

static int thread2(struct pt *pt, int interval)
{
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
 
  while(1) {
    PT_WAIT_UNTIL(pt, millis() - timestamp > interval );
    timestamp = millis(); // take a new timestamp
    c.sendCmd(timer_runtime_end, "light sensor");
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
  rollOut(true);
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
    return 0;
  }
}

void rollOut(bool rollOut) {
  int rolValue = 50;
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
  rolledOut = rollOut;
  c.sendCmd(rollout_done, "Rollout complete");
  
  
}

void setup() {
    Serial.begin(BAUD_RATE);
    attach_callbacks();
    PT_INIT(&pt1);
    PT_INIT(&pt2);   
}

void loop() {
    c.feedinSerialData();
    thread1(&pt1, 30000, 10000);
    thread2(&pt2, 40000);
}


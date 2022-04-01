int speeds[4] = {0,0,0,0}; //left, right, top, bottom

/*
int enables[4] = {D3,D5,D6,D9};
int pin1s[4] = {D2,D7,D10,D12};
int pin2s[4] = {D4,D8,D11,D13};
*/
//////////////////////////////
//Code added for compiling/testing purposes, comment out if necessary
int dirs = 0;
int enables[4] = {6,8,9,12};
int pin1s[4] = {5,10,13,15};
int pin2s[4] = {7,8,14,16};
//////////////////////////////

void setup() {
  // put your setup code here, to run once:
  for(int i=0;i<4;i++)
  {
    pinMode(speeds[i],OUTPUT);
    pinMode(enables[i],OUTPUT);
    pinMode(pin1s[i],OUTPUT);
    pinMode(pin2s[i],OUTPUT);
  }

  Serial.begin(9600);
}

void loop() {
  // update speeds and dirs from serial:
  if(Serial.available() >= 5)
  {
    for(int i=0;i<4;i++)
    {
      speeds[i] = Serial.read();
    }
    dirs = Serial.read();
  }

  // write speeds:
  for(int i=0;i<4;i++)
  {
    if(bitRead(dirs,i) == 0)
    {
      digitalWrite(pin1s[i],HIGH); 
      digitalWrite(pin2s[i],LOW); 
    }
    else
    {
      digitalWrite(pin1s[i],LOW); 
      digitalWrite(pin2s[i],HIGH); 
    }
    analogWrite(enables[i],speeds[i]);
  }
}
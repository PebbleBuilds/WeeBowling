int speeds[4] = {0,0,0,0}; //left, right, top, bottom
int dirs = 0;


int enables[4] = {3,9,5,10};
int pin1s[4] = {2,11,7,13};
int pin2s[4] = {4,12,8,A0};

//////////////////////////////
//Pinout for mega
/*
int enables[4] = {6,8,9,12};
int pin1s[4] = {5,10,13,15};
int pin2s[4] = {7,8,14,16};
*/
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
  
  // write speeds:
  for(int i=0;i<4;i++)
  {
    if(bitRead(dirs,3-i))
    {
      digitalWrite(pin1s[i],HIGH); 
      digitalWrite(pin2s[i],LOW); 

      Serial.print(pin1s[i]);
      Serial.print("set to HIGH\n");
      Serial.print(pin2s[i]);
      Serial.print("set to LOW\n");
    }
    else
    {
      digitalWrite(pin1s[i],LOW); 
      digitalWrite(pin2s[i],HIGH); 
      Serial.print(pin1s[i]);
      Serial.print("set to LOW\n");
      Serial.print(pin2s[i]);
      Serial.print("set to HIGH\n");
    }
    analogWrite(enables[i],speeds[i]);
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

    // report status:
    Serial.print("Speeds:");
    Serial.print(speeds[0]);
    Serial.print(speeds[1]);
    Serial.print(speeds[2]);
    Serial.print(speeds[3]);
    Serial.print("Dirs:");
    Serial.print(dirs);
    Serial.print("\n");

    // write speeds:
    for(int i=0;i<4;i++)
    {
      if(bitRead(dirs,3-i))
      {
        digitalWrite(pin1s[i],HIGH); 
        digitalWrite(pin2s[i],LOW); 

        Serial.print(pin1s[i]);
        Serial.print("set to HIGH\n");
        Serial.print(pin2s[i]);
        Serial.print("set to LOW\n");
      }
      else
      {
        digitalWrite(pin1s[i],LOW); 
        digitalWrite(pin2s[i],HIGH); 
        Serial.print(pin1s[i]);
        Serial.print("set to LOW\n");
        Serial.print(pin2s[i]);
        Serial.print("set to HIGH\n");
      }
      analogWrite(enables[i],speeds[i]);
    }
  }
}

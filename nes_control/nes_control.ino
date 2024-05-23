#define OUT_PIN 13
#define LATCH_INTERRUPT 2
#define CLOCK_INTERRUPT 3
#define CMD_EXIT_SAFE_MODE 1
#define CMD_UPDATE_CONTROL_STATE 2
#define CMD_ENTER_SAFE_MODE 3
#define HAND_SHAKE_BYTE 183
#define CMD_OK "OK"
#define CMD_FAIL "NO"
/*
clock_value 
-2: SafeMode 
-1: IDEL 
0-7: control_state write
*/
short clock_value = -2; 
byte control_state = 0;
byte serial_buffer[4]; 


void setup() { 
  // put your setup code here, to run once:

  serial_buffer[2] = 0;

  Serial.begin(9600);
  Serial.flush();
  pinMode(OUT_PIN, OUTPUT);
  pinMode(LATCH_INTERRUPT, INPUT);
  pinMode(CLOCK_INTERRUPT, INPUT);

  attachInterrupt(digitalPinToInterrupt(LATCH_INTERRUPT), NES_LATCH, HIGH);
  attachInterrupt(digitalPinToInterrupt(CLOCK_INTERRUPT), NES_CLOCK, HIGH);

  digitalWrite(OUT_PIN, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println("Howdy yall");
  if(clock_value >= 0){
    digitalWrite(OUT_PIN, bitRead(control_state, clock_value));
  }
  else{
    digitalWrite(OUT_PIN, LOW);
  }

  if(Serial.available() > 0)
  {
    int bytes_read = Serial.readBytes(serial_buffer, 4);
    if(bytes_read = 4 && serial_buffer[0] == HAND_SHAKE_BYTE)
    {
        if((serial_buffer[0] ^ serial_buffer[1] ^ serial_buffer[2]) == serial_buffer[3]){
          switch(serial_buffer[1])
          {
            case CMD_EXIT_SAFE_MODE:
              clock_value = -1;
              Serial.print(CMD_OK);
              Serial.flush();
              break;
            case CMD_UPDATE_CONTROL_STATE:
              control_state = serial_buffer[2];
              serial_buffer[2] = 0;
              Serial.print(CMD_OK); // verification
              Serial.flush(); 
              break;
            case CMD_ENTER_SAFE_MODE:
              control_state = -2;
              digitalWrite(OUT_PIN, LOW);
              Serial.print(CMD_OK);
              Serial.flush();
              break;

          }
          
        }
        else{
          Serial.print(CMD_FAIL);
          Serial.flush();
        }
    }
    else{
      Serial.print(CMD_FAIL);
      Serial.flush();
    }
  }
}

void NES_LATCH()
{
  if(clock_value < 0)
  {
    clock_value = 0;
  }
  else{
    clock_value = -1;
  }
}

void NES_CLOCK()
{
  if(clock_value >= 0){
    clock_value++;
    if(clock_value > 7){
      clock_value = -1;
    }
  }
}

void SendInt(int value)
{
  Serial.print(value);
}

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN   10         // Configurable, see typical pin layout above
#define SS_1_PIN  9          // Configurable, take a unused pin, only HIGH/LOW required

//byte ssPins[] = {SS_1_PIN};// , SS_2_PIN, SS_3_PIN, SS_4_PIN, SS_5_PIN, SS_6_PIN, SS_7_PIN

MFRC522 mfrc522;   // Create MFRC522 instance.

String tagID = "";

//Pump stuff
int SHOTS[6] = {150, 150, 155, 155, 165, 145}; //average time to pump 1oz based on pump data (17.5s)
const int controlPin[6] = {A0,A1,A2,A3,A4,A5}; //respectively relay 1-6

//serial connection stuff
String command;
String serialcon[7] = {"","","","","","",""};
double raspberryPi[6] = {0,0,0,0,0,0}; // [0,8000,0,8000,0,1000] array output of Cuba Libre
String seriallocation[6] = {"","","","","",""};
int location[6] = {0,1,2,3,4,5};
int cupSize;

// RFID Bottle Tag
String MasterTag = "A73E95FA";  
String VodkaTag = "423848A";
String WhiteRumTag = "420858A";
String TripleSecTag = "41B858A";
String CokeTag = "417858A";
String CranberryJuiceTag = "413858A";
String LimeJuiceTag = "4F858A";

void setup() {
  // Initiating
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init(SS_1_PIN, RST_PIN); // Init each MFRC522 card
  Serial.print(F("Reader "));
  Serial.print(F(": "));
  mfrc522.PCD_DumpVersionToSerial();

  //Pump set up
  for (uint8_t i = 0; i < 6; i++) {
    pinMode(controlPin[i], OUTPUT);
    digitalWrite(controlPin[i], LOW);
  }
}

//String dump_byte_array(byte *buffer, byte bufferSize) {
//  String temp = "";
//  for (byte i = 0; i < bufferSize; i++) {
//    temp.concat(String(buffer[i] < 0x10 ? " 0" : " "));
//    temp.concat(String(buffer[i], HEX));
//  }
//  return temp;
//}

void readRFID()
{
  tagID = "";
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.print(F("Reader "));
    for ( uint8_t i = 0; i < 4; i++) {        //The UIDs used here have a 4 byte UID
      //readCard[i] = mfrc522.uid.uidByte[i];
      tagID.concat(String(mfrc522.uid.uidByte[i], HEX)); // Adds the 4 bytes in a single String variable
      tagID.toUpperCase();
    }
    Serial.println(tagID);
    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();
  }
}

void serialConvert(){
  for ( uint8_t i = 0; i < 6; i++) {
    raspberryPi[i] = serialcon[i].toInt();
    raspberryPi[i] = raspberryPi[i]*SHOTS[i]; //8 oz cup example
    Serial.print("\nSerial: ");
    Serial.print(serialcon[i]);
    Serial.print("\nRaspberryPi: ");
    Serial.print(raspberryPi[i]);
  }
}

void serialConvertcustom(){
  for ( uint8_t i = 0; i < 6; i++) {
    raspberryPi[i] = serialcon[i].toInt();
    raspberryPi[i] = raspberryPi[i]*SHOTS[i]; //8 oz cup example
    Serial.print("\nSerial: ");
    Serial.print(serialcon[i]);
    Serial.print("\nRaspberryPi[i]: ");
    Serial.print(raspberryPi[i]);
  }
}

////This Function will handle dispensing fluid for the POC demonstration
void dispenseFluid(){
  //Serial.print("Dispensing Some Stuff\n");
  int cupSize = 8;
  int dispenseTime = findLowTime();
  while (dispenseTime>0){
    for ( uint8_t i = 0; i < 6; i++) {
      if (raspberryPi[i] > 0){
        raspberryPi[i] = raspberryPi[i]-dispenseTime;
        digitalWrite(controlPin[location[i]], HIGH);
        Serial.print("\nPump ON");
        Serial.print(location[i]);
        Serial.print("\nTime on:");
        Serial.print(dispenseTime);
      }else{
        Serial.print("\nPump OFF");
        Serial.print(location[i]);
      }


      Serial.print("\nTime left on Pump ");
      Serial.print(i);
      Serial.print(": ");
      Serial.print(raspberryPi[i]);
    }

    for ( uint8_t i = 0; i < cupSize; i++) {
      delay (dispenseTime);
    }
    for ( uint8_t i = 0; i < 6; i++) {
      if(raspberryPi[i]==0){
        digitalWrite(controlPin[location[i]], LOW);
        Serial.print("\nPump OFF");
        Serial.print(location[i]);
      }
    }
    dispenseTime = findLowTime();
  }
}

void dispenseFluidCustom(){
  //Serial.print("Dispensing Some Stuff\n");
  int dispenseTime = findLowTime();
  while (dispenseTime>0){
    for ( uint8_t i = 0; i < 6; i++) {
      if (raspberryPi[i] > 0){
        raspberryPi[i] = raspberryPi[i]-dispenseTime;
        digitalWrite(controlPin[i], HIGH);
        Serial.print("\nPump ON");
        Serial.print(i);
        Serial.print("\nTime on:");
        Serial.print(dispenseTime);
      }else{
        Serial.print("\nPump OFF");
        Serial.print(i);
      }


      Serial.print("\nTime left on Pump ");
      Serial.print(i);
      Serial.print(": ");
      Serial.print(raspberryPi[i]);
    }
    delay (dispenseTime);
    for ( uint8_t i = 0; i < 6; i++) {
      if(raspberryPi[i] == 0){
        digitalWrite(controlPin[i], LOW);
        Serial.print("\nPump OFF");
        Serial.print(i);
      }
    }
    dispenseTime = findLowTime();
  }
}

int findLowTime(){
  int high = 0;
  for ( uint8_t i = 0; i < 6; i++) {
    if(raspberryPi[i]>high){
      high = raspberryPi[i];
    }
  }
  Serial.println("High time");
  Serial.print(high);
  int low = high;
  for ( uint8_t i = 0; i < 6; i++) {
    if (0<raspberryPi[i] && raspberryPi[i] < low){
      low = raspberryPi[i];
      Serial.print("\nLow loop entry");
      Serial.print(i);
      Serial.print("\nValue: ");
      Serial.print(raspberryPi[i]);
      Serial.print("\nLow: ");
      Serial.print(low);
    }
  }
  Serial.println("Low time");
  Serial.print(low);
  return (low);
}

void prime_func(){
  for ( uint8_t i = 0; i < 6; i++){
    //Serial.println(serialcon[i]);
    raspberryPi[i] = serialcon[i].toInt();
    //Serial.println(raspberryPi[i]);
    if (raspberryPi[i] == 1){
        digitalWrite(controlPin[i], HIGH);
        Serial.print("pump ");
        Serial.print(i);
        Serial.println(" is priming");        
    }
  }
  delay(8000);
  for ( uint8_t i = 0; i < 6; i++){
    if (raspberryPi[i] == 1){
        digitalWrite(controlPin[i], LOW);
        Serial.print("pump ");
        Serial.print(i);
        Serial.println(" is done priming");        
    }
  }
}

void loop() {
  //readRFID();
   while (Serial.available()){
        command = Serial.readStringUntil('\n');
        if (command == "selected"){        
          Serial.println("bay1");
          serialcon[0] = Serial.readStringUntil('\n');
          Serial.println("bay2");
          serialcon[1] = Serial.readStringUntil('\n');
          Serial.println("bay3");
          serialcon[2] = Serial.readStringUntil('\n');
          Serial.println("bay4");
          serialcon[3] = Serial.readStringUntil('\n');
          Serial.println("bay5");
          serialcon[4] = Serial.readStringUntil('\n');
          Serial.println("bay6");
          serialcon[5] = Serial.readStringUntil('\n');
//          Serial.println("Cup Size");
//          serialcon[6] = Serial.readStringUntil('\n');
          serialConvert();
          dispenseFluid(); 
          Serial.println("\nDone");
          
       }else if (command == "custom"){        
         Serial.println("bay1");
          serialcon[0] = Serial.readStringUntil('\n');
          Serial.println("bay2");
          serialcon[1] = Serial.readStringUntil('\n');
          Serial.println("bay3");
          serialcon[2] = Serial.readStringUntil('\n');
          Serial.println("bay4");
          serialcon[3] = Serial.readStringUntil('\n');
          Serial.println("bay5");
          serialcon[4] = Serial.readStringUntil('\n');
          Serial.println("bay6");
          serialcon[5] = Serial.readStringUntil('\n');
          serialConvertcustom();
          dispenseFluidCustom();
          Serial.println("\nDone");
          
       }else if (command == "prime"){
          Serial.println("bay1");
          serialcon[0] = Serial.readStringUntil('\n');
          Serial.println("bay2");
          serialcon[1] = Serial.readStringUntil('\n');
          Serial.println("bay3");
          serialcon[2] = Serial.readStringUntil('\n');
          Serial.println("bay4");
          serialcon[3] = Serial.readStringUntil('\n');
          Serial.println("bay5");
          serialcon[4] = Serial.readStringUntil('\n');
          Serial.println("bay6");
          serialcon[5] = Serial.readStringUntil('\n');
          prime_func();
          Serial.println("\nDone");
          
       }else if (command == "readRFID"){        
          readRFID();
          
       }
       else{
        Serial.println(" Serial_fail");
       }
  }
}

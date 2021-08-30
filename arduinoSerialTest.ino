int led[6] = {A0, A1, A2, A3, A4, A5};
String incoming;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 6; i++){
    pinMode(led[i], OUTPUT);
  }
}

void loop() {
  //Serial.println("Hello from Arduino!");
  //delay(1000);
  
//  for (int i = 0; i < 6; i++){
//        digitalWrite(led[i], HIGH);
//        delay(500);
//        digitalWrite(led[i], LOW);
//        delay(500);
//  }
//  delay(2000); 

//  while(Serial.available()){
//      //Serial.println("sup");
//      //Serial.println("Hello from Arduino!");
//    incoming = Serial.readStringUntil('\n');
//    Serial.print("RPI sent: ");
//    Serial.print(incoming);
//  }
  while(Serial.available()){
    incoming = Serial.readStringUntil('\n');
    if(incoming == "listen"){
      Serial.println("answering");
      for (int j = 0; j < 6; j++){
          digitalWrite(led[j], HIGH);
      }
      delay(300);
      for (int j = 0; j < 6; j++){
        digitalWrite(led[j], LOW);
      }
      delay(300);
      Serial.write(10); //ack connection
    }else if(incoming == "bay1"){
      digitalWrite(led[0], HIGH);
      delay(300);
      digitalWrite(led[0], LOW);
      delay(300);
      Serial.write(1); //ack bay 1
    }else if(incoming == "bay2"){
      digitalWrite(led[1], HIGH);
      delay(300);
      digitalWrite(led[1], LOW);
      delay(300);
      Serial.write(2); //ack bay 2
    }else if(incoming == "bay3"){
      digitalWrite(led[2], HIGH);
      delay(300);
      digitalWrite(led[2], LOW);
      delay(300);
      Serial.write(3); //ack bay 3
    }else if(incoming == "bay4"){
      digitalWrite(led[3], HIGH);
      delay(300);
      digitalWrite(led[3], LOW);
      delay(300);
      Serial.write(4); //ack bay 4
    }else if(incoming == "bay5"){
      digitalWrite(led[4], HIGH);
      delay(300);
      digitalWrite(led[4], LOW);
      delay(300);
      Serial.write(5); //ack bay 5
    }else if(incoming == "bay6"){
      digitalWrite(led[5], HIGH);
      delay(300);
      digitalWrite(led[5], LOW);
      delay(300);
      Serial.write(6); //ack bay 6
    }else if(incoming == "Good Talk!"){
      for (int i = 0; i < 6; i++){
        for (int j = 0; j < 6; j++){
          digitalWrite(led[j], HIGH);
        }
        delay(300);
        for (int j = 0; j < 6; j++){
          digitalWrite(led[j], LOW);
        }
        delay(300);
      }
    }else{
      Serial.write(16);
      for (int j = 0; j < 6; j++){
          digitalWrite(led[j], HIGH);
      }
      delay(300);
      for (int j = 0; j < 6; j++){
        digitalWrite(led[j], LOW);
      }
      delay(300);
    }
  }
  //Serial.println("Nothing coming in");
}

#include <KeyboardFR.h>
//Writen for pro micro
//These proved to be usefull 
//http://arduino.stackexchange.com/questions/1471/arduino-pro-micro-get-data-out-of-tx-pin
//https://forum.sparkfun.com/viewtopic.php?f=32&t=38889&sid=8178cdb38005ff33cc380a5da34fb583&start=15
//https://github.com/Sackhorn/HC05-BluetoothWithArduinoProMicro
//https://forum.arduino.cc/t/arduino-uno-hc05-weird-data-transfer/891267/15

void setup()
{
  pinMode(9, OUTPUT);  
  digitalWrite(9, HIGH); 
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop()
{
  String message;   
  int byte;                    
    while (Serial1.available()){     // Boucle de lecture sur le BT = Reading BT 
    message = Serial1.readString();  // Lecture du message envoyé par le BT = Read message send by BT
    //byte=Serial1.read();
    //Serial.println(byte,DEC);
    Serial.println(message); 
    Serial.println("______________");        // Ecriture du message dans le serial usb = write in serial usb
    //Serial1.println(byte,HEX);        // Ecriture du message dans le serial BT = write in serial BT
    }
}
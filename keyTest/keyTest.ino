#include <Keyboard.h>

String message; 

void setup( )
{

// Configure the keyboard library
Keyboard.begin();

Serial.begin(9600);

delay(5000);
for (int i=0x00;i<0x80;i++){
  message=String(i, HEX);
  Keyboard.print(message);
  Keyboard.print(":");
  Keyboard.press(i);
  Keyboard.release(i);
  Keyboard.print(" ");
  delay(10);
}
}

void loop( )
{
}

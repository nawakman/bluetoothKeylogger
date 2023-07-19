/*  Simple keyboard to serial port at 115200 baud

  PS2KeyAdvanced library example

  Advanced support PS2 Keyboard to get every key code byte from a PS2 Keyboard
  for testing purposes.

  IMPORTANT WARNING

    If using a DUE or similar board with 3V3 I/O you MUST put a level translator
    like a Texas Instruments TXS0102 or FET circuit as the signals are
    Bi-directional (signals transmitted from both ends on same wire).

    Failure to do so may damage your Arduino Due or similar board.

  Test History
    September 2014 Uno and Mega 2560 September 2014 using Arduino V1.6.0
    January 2016   Uno, Mega 2560 and Due using Arduino 1.6.7 and Due Board
                    Manager V1.6.6

  This is for a LATIN style keyboard using Scan code set 2. See various
  websites on what different scan code sets use. Scan Code Set 2 is the
  default scan code set for PS2 keyboards on power up.

  Will support most keyboards even ones with multimedia keys or even 24 function keys.

  The circuit:
   * KBD Clock (PS2 pin 1) to an interrupt pin on Arduino ( this example pin 3 )
   * KBD Data (PS2 pin 5) to a data pin ( this example pin 4 )
   * +5V from Arduino to PS2 pin 4
   * GND from Arduino to PS2 pin 3

   The connector to mate with PS2 keyboard is a 6 pin Female Mini-Din connector
   PS2 Pins to signal
    1       KBD Data
    3       GND
    4       +5V
    5       KBD Clock

   Keyboard has 5V and GND connected see plenty of examples and
   photos around on Arduino site and other sites about the PS2 Connector.

 Interrupts

   Clock pin from PS2 keyboard MUST be connected to an interrupt
   pin, these vary with the different types of Arduino

  PS2KeyAdvanced requires both pins specified for begin()

    keyboard.begin( data_pin, irq_pin );

  Valid irq pins:
     Arduino Uno:  2, 3
     Arduino Due:  All pins, except 13 (LED)
     Arduino Mega: 2, 3, 18, 19, 20, 21
     Teensy 2.0:   All pins, except 13 (LED)
     Teensy 2.0:   5, 6, 7, 8
     Teensy 1.0:   0, 1, 2, 3, 4, 6, 7, 16
     Teensy++ 2.0: 0, 1, 2, 3, 18, 19, 36, 37
     Teensy++ 1.0: 0, 1, 2, 3, 18, 19, 36, 37
     Sanguino:     2, 10, 11

  Read method Returns an UNSIGNED INT containing
        Make/Break status
        Caps status
        Shift, CTRL, ALT, ALT GR, GUI keys
        Flag for function key not a displayable/printable character
        8 bit key code

  Code Ranges (bottom byte of unsigned int)
        0       invalid/error
        1-1F    Functions (Caps, Shift, ALT, Enter, DEL... )
        1A-1F   Functions with ASCII control code
                    (DEL, BS, TAB, ESC, ENTER, SPACE)
        20-61   Printable characters noting
                    0-9 = 0x30 to 0x39 as ASCII
                    A to Z = 0x41 to 0x5A as upper case ASCII type codes
                    8B Extra European key
        61-A0   Function keys and other special keys (plus F2 and F1)
                    61-78 F1 to F24
                    79-8A Multimedia
                    8B NOT included
                    8C-8E ACPI power
                    91-A0 and F2 and F1 - Special multilingual
        A8-FF   Keyboard communications commands (note F2 and F1 are special
                codes for special multi-lingual keyboards)

    By using these ranges it is possible to perform detection of any key and do
    easy translation to ASCII/UTF-8 avoiding keys that do not have a valid code.

    Top Byte is 8 bits denoting as follows with defines for bit code

        Define name bit     description
        PS2_BREAK   15      1 = Break key code
                   (MSB)    0 = Make Key code
        PS2_SHIFT   14      1 = Shift key pressed as well (either side)
                            0 = NO shift key
        PS2_CTRL    13      1 = Ctrl key pressed as well (either side)
                            0 = NO Ctrl key
        PS2_CAPS    12      1 = Caps Lock ON
                            0 = Caps lock OFF
        PS2_ALT     11      1 = Left Alt key pressed as well
                            0 = NO Left Alt key
        PS2_ALT_GR  10      1 = Right Alt (Alt GR) key pressed as well
                            0 = NO Right Alt key
        PS2_GUI      9      1 = GUI key pressed as well (either)
                            0 = NO GUI key
        PS2_FUNCTION 8      1 = FUNCTION key non-printable character (plus space, tab, enter)
                            0 = standard character key

  Error Codes
     Most functions return 0 or 0xFFFF as error, other codes to note and
     handle appropriately
        0xAA   keyboard has reset and passed power up tests
               will happen if keyboard plugged in after code start
        0xFC   Keyboard General error or power up fail

  See PS2Keyboard.h file for returned definitions of Keys

  Note defines starting
            PS2_KEY_* are the codes this library returns
            PS2_*     remaining defines for use in higher levels

  To get the key as ASCII/UTF-8 single byte character conversion requires use
  of PS2KeyMap library AS WELL.

  Written by Paul Carpenter, PC Services <sales@pcserviceselectronics.co.uk>
*/

#include <PS2KeyAdvanced.h>
#include <Keyboard.h>
#include "keycodesUS.h"

/* Keyboard constants  Change to suit your Arduino
   define pins used for data and clock from keyboard */
#define DATAPIN 4
#define IRQPIN  3
#define USB_KB_ALIM 2
#define RESET_PIN 9
#define RX_PIN 1
#define TX_PIN 0

uint16_t c;
uint16_t lastC=0;
unsigned long keypressTime;
String message; 
String messageBT; 
bool ignoreFirstKeypress=false;//else it keeps pressing "[" or "e" while plugging the board

PS2KeyAdvanced PS2Keyboard;

void setup( )
{
digitalWrite(RESET_PIN,HIGH);//prevent reboot //need to be called before pinMode else locked in reset mode
pinMode(RESET_PIN,OUTPUT);
pinMode(USB_KB_ALIM,OUTPUT);//5V alim for PS2 or USB Keyboard
digitalWrite(USB_KB_ALIM,HIGH);

// Configure the keyboard library
Keyboard.begin();
// Configure the PS2 keyboard library
PS2Keyboard.begin( DATAPIN, IRQPIN );
// Configure serial communication
Serial.begin(9600);
Serial1.begin(9600);  // HC-05 //https://github.com/Sackhorn/HC05-BluetoothWithArduinoProMicro //https://forum.arduino.cc/t/arduino-uno-hc05-weird-data-transfer/891267/15
}

void loop( )
{
  if( PS2Keyboard.available( ) )
    {
      // read the next key
      lastC=c;
      c = PS2Keyboard.read( );
      if((c>0) && (ignoreFirstKeypress || bitRead(c,15))){//ignore first keypress but not the other after
        keypressTime=millis();
        ignoreFirstKeypress=true;
        TransmitKeypress();
        AddCharToMessage();
        PrintModifiers();
      }
  }
  if((millis()-keypressTime)>650){//if x millisecond passed without key pressed
    PrintAndClearMessage();
  }
  if(Serial1.available()){
    messageBT=Serial1.readString();
    Serial1.print("received: ");
    Serial1.println(messageBT);
    SerialToKeyboard();
  }
}

int StrHexToInt(String str)
{
  char temp[4];//0x..
  str.toCharArray(temp,4);
  return (uint8_t)strtol(temp, 0, 16);//char arraay to long to uint8_t
}

void SerialToKeyboard(){
  if(messageBT.length()>0){
    if(messageBT=="test\r\n"){
      Serial1.println("************");
      Serial1.println("bluetooth connexion successful");
      Serial1.println("Ready to write...");
      Serial1.println("************");
    }
    else if(messageBT=="reboot\r\n"){//restart arduino board
      digitalWrite(RESET_PIN,LOW);
    }
    else if(messageBT=="clear\r\n"){//clear message (sometimes message contains \0 characters and we cannot use it anymore)
      message="";
      Serial1.println("message cleared");
    }
    //individual keys  
    else if((messageBT[0]=='0') && (messageBT[1]=='x')){//key identified by its keycode
      Serial1.println("isCustomKey");
      String messageNo0x=messageBT;
      messageNo0x.remove(0,2);//remove '0x'
      Keyboard.press(StrHexToInt(messageNo0x));
      Keyboard.release(StrHexToInt(messageNo0x));
    } 
    else if(messageBT=="releaseAll\r\n"){
      Keyboard.releaseAll();
    }
    else if(messageBT=="enter\r\n"){
      Keyboard.press(KEY_RETURN);
    }
    else if(messageBT=="backspace\r\n"){
      Keyboard.press(KEY_BACKSPACE);
      Keyboard.release(KEY_BACKSPACE);
    }
    else if(messageBT=="ctrl\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
    }
    else if(messageBT=="alt\r\n"){
      Keyboard.press(KEY_LEFT_ALT);
    }
    else if(messageBT=="tab\r\n"){
      Keyboard.press(KEY_TAB);
    }
    else if(messageBT=="1tab\r\n"){
      Keyboard.press(KEY_TAB);
      Keyboard.release(KEY_TAB);
    }
    else if(messageBT=="windows\r\n"){
      Keyboard.press(KEY_LEFT_GUI);
    }
    else if(messageBT=="1windows\r\n"){
      Keyboard.press(KEY_LEFT_GUI);
      Keyboard.release(KEY_LEFT_GUI);
    }
    else if(messageBT=="shift\r\n"){
      Keyboard.press(KEY_LEFT_SHIFT);
    }
    else if(messageBT=="esc\r\n"){
      Keyboard.press(KEY_ESC);
    }
    else if(messageBT=="del\r\n"){
      Keyboard.press(KEY_DELETE);
      Keyboard.release(KEY_DELETE);
    }
    else if(messageBT=="up\r\n"){
      Keyboard.press(KEY_UP_ARROW);
      Keyboard.release(KEY_UP_ARROW);
    }
    else if(messageBT=="down\r\n"){
      Keyboard.press(KEY_DOWN_ARROW);
      Keyboard.release(KEY_DOWN_ARROW);
    }
    else if(messageBT=="left\r\n"){
      Keyboard.press(KEY_LEFT_ARROW);
      Keyboard.release(KEY_LEFT_ARROW);
      }
    else if(messageBT=="right\r\n"){
      Keyboard.press(KEY_RIGHT_ARROW);
      Keyboard.release(KEY_RIGHT_ARROW);
    }
    //keyboard shortcuts
    else if(messageBT=="alt f4\r\n"){
      Keyboard.press(KEY_LEFT_ALT);
      Keyboard.press(KEY_F4);
      Keyboard.release(KEY_LEFT_ALT);
      Keyboard.release(KEY_F4);
    }
    else if(messageBT=="alt d\r\n"){
      Keyboard.press(KEY_LEFT_ALT);
      Keyboard.press('d');
      Keyboard.release(KEY_LEFT_ALT);
      Keyboard.release('d');
    }
    else if(messageBT=="alt tab\r\n"){
      Keyboard.press(KEY_LEFT_ALT);
      Keyboard.press(KEY_TAB);
      Keyboard.release(KEY_LEFT_ALT);
      Keyboard.press(KEY_TAB);
    }
    else if(messageBT=="ctrl c\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('c');
      Keyboard.release(KEY_LEFT_CTRL);
      Keyboard.release('c');
    }
    else if(messageBT=="ctrl a\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('a');
      Keyboard.release(KEY_LEFT_CTRL);
      Keyboard.release('a');
    }
    else if(messageBT=="ctrl v\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('v');
      Keyboard.release(KEY_LEFT_CTRL);
      Keyboard.release('v');
    }
    else if(messageBT=="ctrl w\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('w');
      Keyboard.release(KEY_LEFT_CTRL);
      Keyboard.release('w');
    }
    else if(messageBT=="ctrl t\r\n"){
      Keyboard.press(KEY_LEFT_CTRL);
      Keyboard.press('t');
      Keyboard.release(KEY_LEFT_CTRL);
      Keyboard.release('t');
    }  
    else{
      String messageNoRN=messageBT;
      int msgLen=messageNoRN.length();
      messageNoRN.remove(msgLen-1);//remove \r
      messageNoRN.remove(msgLen-2);//remove \n
      Keyboard.print(messageNoRN);
    }
  }
}

void AddCharToMessage(){//called twice each keypress (pressed/released)
  if (bitRead(c,15)){//is key released
    uint8_t code=c & 0xFF;
    bool shiftPressed=bitRead(c,12) || bitRead(c,14);//shift or capslock pressed
    if(!(AddSpecialCharacterUS(shiftPressed,code) || IsBlankCharacterUS(shiftPressed,code))){//if this is not a  a special character (has not been processed) or blank character //NEED TO BE EXECUTED IN THIS ORDER //do not go further if any of the two functions return true)
      if(shiftPressed){//if shift or capsLock
        message+=(char)shiftCharactersUS[code];//upperCase
      }
      else{//if not shift or capsLock
        message+=(char)charactersUS[code];//lowerCase
      }
    }
  }
}

bool AddSpecialCharacterUS(bool shiftPressed,uint8_t code){//return true if this is a special character and is added to the message, false else
  /*ADD ANYWAY*/
  if(code==0x1f){
      message+=' ';
      return true;
  }
  else if(code==0x1c){
    message+='\b';
    return true;
  }
  else if(code==0x1d){
    message+='\t';
    return true;
  }
  else if(code==0x1e){
    message+='\n';
    return true;
  }
  if (shiftPressed){//shift pressed
    if(code==0x5d){
      message+='{';
      return true;
    }
    else if(code==0x5e){
      message+='}';
      return true;
    }
  }
  else{//shift not pressed
    if(code==0x5d){//[
      message+='[';
      return true;
    }
    else if(code==0x5e){
      message+=']';
      return true;
    }
    else if(code==0x3a){
      message+='\'';
    }
  }
  return false;
}

bool IsBlankCharacterUS(bool shiftPressed, uint8_t code){//if a blank character is added to String the String comparisons do not work //KEYS LIKE ENTER AND BACKSPACE ARE BLANK CHARACTER BUT STILL NEED TO BE EXAMINATED
  if (shiftPressed){
    return shiftCharactersUS[code]=='\0';
  }
  else{
    return charactersUS[code]=='\0';
  }
}

void PrintAndClearMessage(){
  if(message != ""){
    Serial.println(message);
    Serial1.println(message);
    message="";
  }
}

void Debug(){
  uint8_t code=c & 0xFF;//get 8 lower bits (key code) //https://stackoverflow.com/questions/3270307/how-do-i-get-the-lower-8-bits-of-an-int
  Serial.println( c, BIN );
  Serial.println(code, HEX);
  if(code<31){//Functions
    Serial.println("modifier ");
  }
  else if(code<97){//ASCII //31 is space key
    Serial.println((char)c);
  }
  else{
    Serial.println("F key or multimedia ");
  }
  Serial.println("________________________________");
}

void PrintModifiers(){
  /*if(bitRead(c,15)){//if all keys released
    Serial1.println("Break");
  }*/
  if(bitRead(c,14) && !bitRead(lastC,14)){//pressed but not already pressed
    Serial1.println("Shift");
  }
  if(bitRead(c,13) && !bitRead(lastC,13)){
    Serial1.println("Ctrl");
  }
  if(bitRead(c,12) && !bitRead(lastC,12)){
    Serial1.println("CapsLock");
  }
  if(bitRead(c,11) && !bitRead(lastC,11)){
    Serial1.println("Alt");
  }
  if(bitRead(c,10) && !bitRead(lastC,10)){
    Serial1.println("AltGr");
  }
  if(bitRead(c,9) && !bitRead(lastC,9)){
    Serial1.println("GUI"); 
  }
  /*if(bitRead(c,8) && !bitRead(lastC,8)){
    Serial1.println("Function");
  }*/
}

void TransmitKeypress(){
  uint8_t code=c & 0xFF;
  if(!bitRead(c,15)){//key pressed
    Serial.print(code, HEX);
    Serial.print(">>");
    Serial.println(keyboardKeysUS[code],HEX);
    if(bitRead(c,14) || bitRead(c,12)){//shift or capslock active
      Keyboard.press(keyboardShiftKeysUS[code]);
    }
    else{
      Keyboard.press(keyboardKeysUS[code]);
    }
  }
  else{//key released
    Keyboard.release(keyboardShiftKeysUS[code]);
    Keyboard.release(keyboardKeysUS[code]);
  }
}

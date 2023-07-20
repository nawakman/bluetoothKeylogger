class keyCodesFileFactory:
    def __init__(self, filePath):
        open(filePath, 'w').close()#clear file
        self.file=open(filePath,'a')
        self.file.write("const uint8_t keyboardKeysFR[256]={")
        self.associations=[0 for i in range(256)]#2**8, all possible keycodes
        self.shiftAssociations=[0 for i in range(256)]#2**8, all possible keycodes
        self.altAssociations=[0 for i in range(256)]#2**8, all possible keycodes
        self.characters=['\0' for i in range(140)]#2**8, all possible keycodes //memory optimisation, last character is "<" at index 129
        self.shiftCharacters=['\0' for i in range(140)]#2**8, all possible keycodes //memory optimisation, last character is "<" at index 139
        self.altCharacters=['\0' for i in range(96)]#2**8, all possible keycodes //memory optimisation, last character is "}" at index 95
    
    def AddKeycode(self,PS2Code,keyboardCode,character="\0"):
        if self.associations[PS2Code]!=0:
            print(str(hex(PS2Code)),"overwritten")
        self.associations[PS2Code]=keyboardCode
        if character!="\0":
            self.characters[PS2Code]=character
    
    def AddShiftKeycode(self,PS2Code,shiftKeyboardCode,character="\0"):
        if self.shiftAssociations[PS2Code]!=0:
            print(str(hex(PS2Code)),"overwritten")
        self.shiftAssociations[PS2Code]=shiftKeyboardCode
        if character!="\0":
            self.shiftCharacters[PS2Code]=character
    
    def AddAltKeycode(self,PS2Code,altKeyboardCode,character="\0"):
        if self.altAssociations[PS2Code]!=0:
            print(str(hex(PS2Code)),"overwritten")
        self.altAssociations[PS2Code]=altKeyboardCode
        if character!="\0":
            self.altCharacters[PS2Code]=character

    def AddAllKeycodes(self,PS2Code,keyboardCode,character="\0"):
        self.AddKeycode(PS2Code, keyboardCode,character)
        self.AddShiftKeycode(PS2Code, keyboardCode, character)
        self.AddAltKeycode(PS2Code, keyboardCode, character)
    
    def WriteKeycodes(self):
        lastElem=self.associations.pop()
        lastShiftElem=self.shiftAssociations.pop()
        lastAltElem=self.altAssociations.pop()
        lastChar=self.characters.pop()
        lastShiftChar=self.shiftCharacters.pop()
        lastAltChar=self.altCharacters.pop()
        for code in self.associations:
            self.file.write(str(hex(code))+",")
        self.file.write(str(hex(lastElem))+"};//for access with PS2 key as index\nconst uint8_t keyboardShiftKeysFR[256]={")
        for code in self.shiftAssociations:
            self.file.write(str(hex(code))+",")
        self.file.write(str(hex(lastShiftElem))+"};//for access with PS2 key as index (shift pressed)\nconst uint8_t keyboardAltKeysFR[256]={")
        for code in self.altAssociations:
            self.file.write(str(hex(code))+",")
        self.file.write(str(hex(lastAltElem))+"};//for access with PS2 key as index (alt pressed)\nconst uint8_t charactersFR[140]={")
        for char in self.characters:
            self.file.write("'"+char+"',")
        self.file.write("'"+lastChar+"'};//character associated to each key\nconst uint8_t shiftCharactersFR[140]={")
        for shiftChar in self.shiftCharacters:
            self.file.write("'"+shiftChar+"',")
        self.file.write("'"+lastShiftChar+"'};//character associated to each shift key\nconst uint8_t altCharactersFR[96]={")
        for altChar in self.altCharacters:
            self.file.write("'"+altChar+"',")
        self.file.write("'"+lastAltChar+"'};//character associated to each alt key")
        self.file.close()


kcff=keyCodesFileFactory("./bluetoothKeyloggerFR/keycodesFR.h")

#arduino keyboard library follow ascii hex codes, see https://www.asciitable.com/
#extra keys https://github.com/arduino-libraries/Keyboard/blob/master/src/Keyboard.h
#S means shift
#means alt

kcff.AddKeycode(0x40,0xb2,"²")#²
kcff.AddKeycode(0x31,0x26,"&")#&
kcff.AddKeycode(0x32,0xe9,"é")#é
kcff.AddKeycode(0x33,0x22,'''"''')#"
kcff.AddKeycode(0x34,0x27)#'
kcff.AddKeycode(0x35,0x28,"(")#(
kcff.AddKeycode(0x36,0x2d,"-")#-
kcff.AddKeycode(0x37,0xe8,"è")#è
kcff.AddKeycode(0x38,0x5f,"_")#_
kcff.AddKeycode(0x39,0xe7,"ç")#ç
kcff.AddKeycode(0x30,0xe0,"à")#à
kcff.AddKeycode(0x3c,0x29,")")#)
kcff.AddKeycode(0x5f,0x3d,"=")#=
kcff.AddShiftKeycode(0x31,0x31,"1")#1 S
kcff.AddShiftKeycode(0x32,0x32,"2")#2 S
kcff.AddShiftKeycode(0x33,0x33,"3")#3 S
kcff.AddShiftKeycode(0x34,0x34,"4")#4 S
kcff.AddShiftKeycode(0x35,0x35,"5")#5 S
kcff.AddShiftKeycode(0x36,0x36,"6")#6 S
kcff.AddShiftKeycode(0x37,0x37,"7")#7 S
kcff.AddShiftKeycode(0x38,0x38,"8")#8 S
kcff.AddShiftKeycode(0x39,0x39,"9")#9 S
kcff.AddShiftKeycode(0x30,0x30,"0")#0 S
kcff.AddShiftKeycode(0x3c,0xba,"°")#° S
kcff.AddShiftKeycode(0x5f,0x2b,"+")#+ S
kcff.AddAltKeycode(0X32,0x7e,"~")#~ A
kcff.AddAltKeycode(0x33,0x23,"#")## A
kcff.AddAltKeycode(0x34,0x7b,"{")#{ A
kcff.AddAltKeycode(0x35,0x5b,"[")#[ A
kcff.AddAltKeycode(0x36,0x7c,"|")#| A
kcff.AddAltKeycode(0x37,0x27)#' A
kcff.AddAltKeycode(0x38,0x5c,"\\\\")#\ A
kcff.AddAltKeycode(0x39,0x5e,"^")#^ A
kcff.AddAltKeycode(0x30,0x40,"@")#@ A
kcff.AddAltKeycode(0x3c,0x5d,']')#] A
kcff.AddAltKeycode(0x5f,0x7d,"}")#} A

kcff.AddKeycode(0x20,0x30,"0")#numpad 0
kcff.AddKeycode(0x21,0x31,"1")#numpad 1
kcff.AddKeycode(0x22,0x32,"2")#numpad 2
kcff.AddKeycode(0x23,0x33,"3")#numpad 3
kcff.AddKeycode(0x24,0x34,"4")#numpad 4
kcff.AddKeycode(0x25,0x35,"5")#numpad 5
kcff.AddKeycode(0x26,0x36,"6")#numpad 6
kcff.AddKeycode(0x27,0x37,"7")#numpad 7
kcff.AddKeycode(0x28,0x38,"8")#numpad 8
kcff.AddKeycode(0x29,0x39,"9")#numpad 9
kcff.AddKeycode(0x2a,0xeb,".")#numpad .
kcff.AddKeycode(0x2c,0x2b,"+")#numpad +
kcff.AddKeycode(0x2d,0x2d,"-")#numpad -
kcff.AddKeycode(0x2e,0x2a,"*")#numpad *
kcff.AddKeycode(0x2f,0x2f,"/")#numpad /

kcff.AddKeycode(0x5d,0x5e,"^")#^
kcff.AddKeycode(0x5e,0x24,"$")#$
kcff.AddKeycode(0x3a,0xf9,"ù")#ù
kcff.AddKeycode(0x5c,0x2a,"*")#*
kcff.AddKeycode(0x8b,0x3c,"<")#<
kcff.AddKeycode(0x4d,0x2c,",")#,
kcff.AddKeycode(0x3b,0x3b,";")#;
kcff.AddKeycode(0x3d,0x3a,":")#:
kcff.AddKeycode(0x3e,0x21,"!")#!
kcff.AddShiftKeycode(0x5d,0xa8,"¨")#¨ S
kcff.AddShiftKeycode(0x5e,0xa3,"£")#£ S
kcff.AddShiftKeycode(0x3a,0x25,"%")#% S
kcff.AddShiftKeycode(0x5c,0xb5,"µ")#µ S
kcff.AddShiftKeycode(0x8b,0x3e,">")#> S
kcff.AddShiftKeycode(0x4d,0x38,"?")#? S
kcff.AddShiftKeycode(0x3b,0x2e,".")#. S
kcff.AddShiftKeycode(0x3d,0x2f,"/")#/ S
kcff.AddShiftKeycode(0x3e,0xa7,"§")#§ S
kcff.AddAltKeycode(0x5e,0xa4,"¤")#¤

kcff.AddKeycode(0x41,0x71,"q")#q
kcff.AddKeycode(0x42,0x62,"b")#b
kcff.AddKeycode(0x43,0x63,"c")#c
kcff.AddKeycode(0x44,0x64,"d")#d
kcff.AddKeycode(0x45,0x65,"e")#e
kcff.AddKeycode(0x46,0x66,"f")#f
kcff.AddKeycode(0x47,0x67,"g")#g
kcff.AddKeycode(0x48,0x68,"h")#h
kcff.AddKeycode(0x49,0x69,"i")#i
kcff.AddKeycode(0x4a,0x6a,"j")#j
kcff.AddKeycode(0x4b,0x6b,"k")#k
kcff.AddKeycode(0x4c,0x6c,"l")#l
kcff.AddKeycode(0x5b,0x6d,"m")#m
kcff.AddKeycode(0x4e,0x6e,"n")#n
kcff.AddKeycode(0x4f,0x6f,"o")#o
kcff.AddKeycode(0x50,0x70,"p")#p
kcff.AddKeycode(0x51,0x61,"a")#a
kcff.AddKeycode(0x52,0x72,"r")#r
kcff.AddKeycode(0x53,0x73,"s")#s
kcff.AddKeycode(0x54,0x74,"t")#t
kcff.AddKeycode(0x55,0x75,"u")#u
kcff.AddKeycode(0x56,0x76,"v")#v
kcff.AddKeycode(0x57,0x7a,"z")#z
kcff.AddKeycode(0x58,0x78,"x")#x
kcff.AddKeycode(0x59,0x79,"y")#y
kcff.AddKeycode(0x5a,0x77,"w")#w
kcff.AddShiftKeycode(0x41,0x51,"Q")#Q S
kcff.AddShiftKeycode(0x42,0x42,"B")#B S
kcff.AddShiftKeycode(0x43,0x43,"C")#C S
kcff.AddShiftKeycode(0x44,0x44,"D")#D S
kcff.AddShiftKeycode(0x45,0x45,"E")#E S
kcff.AddShiftKeycode(0x46,0x46,"F")#F S
kcff.AddShiftKeycode(0x47,0x47,"G")#G S
kcff.AddShiftKeycode(0x48,0x48,"H")#H S
kcff.AddShiftKeycode(0x49,0x49,"I")#I S
kcff.AddShiftKeycode(0x4a,0x4a,"J")#J S
kcff.AddShiftKeycode(0x4b,0x4b,"K")#K S
kcff.AddShiftKeycode(0x4c,0x4c,"L")#L S
kcff.AddShiftKeycode(0x5b,0x4d,"M")#M S
kcff.AddShiftKeycode(0x4e,0x4e,"N")#N S
kcff.AddShiftKeycode(0x4f,0x4f,"O")#O S
kcff.AddShiftKeycode(0x50,0x50,"P")#P S
kcff.AddShiftKeycode(0x51,0x41,"A")#A S
kcff.AddShiftKeycode(0x52,0x52,"R")#R S
kcff.AddShiftKeycode(0x53,0x53,"S")#S S
kcff.AddShiftKeycode(0x54,0x54,"T")#T S
kcff.AddShiftKeycode(0x55,0x55,"U")#U S
kcff.AddShiftKeycode(0x56,0x56,"V")#V S
kcff.AddShiftKeycode(0x57,0x5a,"Z")#Z S
kcff.AddShiftKeycode(0x58,0x58,"X")#X S
kcff.AddShiftKeycode(0x59,0x59,"Y")#Y S
kcff.AddShiftKeycode(0x5a,0x57,"W")#W S

kcff.AddAllKeycodes(0xfa,0xc1)#capslock
kcff.AddAllKeycodes(0x06,0x81)#leftShift #maybe add to shiftAssociastions too ?
kcff.AddAllKeycodes(0x04,0xce)#printScreen
kcff.AddAllKeycodes(0x07,0x85)#rightShift
kcff.AddAllKeycodes(0x08,0x80)#leftControl
kcff.AddAllKeycodes(0x09,0x84)#rightControl
kcff.AddAllKeycodes(0x0a,0x82)#leftAlt
kcff.AddAllKeycodes(0x0b,0x86)#altGr
kcff.AddAllKeycodes(0x0c,0x83)#GUI
kcff.AddAllKeycodes(0x0e,0x00)#context
kcff.AddAllKeycodes(0x11,0xd2)#home
kcff.AddAllKeycodes(0x12,0xd5)#end
kcff.AddAllKeycodes(0x13,0xd3)#pageUp
kcff.AddAllKeycodes(0x14,0xd6)#pageDown
kcff.AddAllKeycodes(0x15,0xd8)#leftArrow
kcff.AddAllKeycodes(0x16,0xd7)#rightArrow
kcff.AddAllKeycodes(0x17,0xda)#upArrow
kcff.AddAllKeycodes(0x18,0xd9)#downArrow
kcff.AddAllKeycodes(0x19,0xd1)#inser
kcff.AddAllKeycodes(0x1a,0xd4)#DEL
kcff.AddAllKeycodes(0x1b,0xb1)#escape
kcff.AddAllKeycodes(0x1c,0xb2)#backspace #08 works too
kcff.AddAllKeycodes(0x1d,0xb3)#tab
kcff.AddAllKeycodes(0x1e,0xb0)#enter
kcff.AddAllKeycodes(0x1f,0x20)#space

kcff.AddKeycode(0x61,0xc2)#f1
kcff.AddKeycode(0x62,0xc3)#f2
kcff.AddKeycode(0x63,0xc4)#f3
kcff.AddKeycode(0x64,0xc5)#f4
kcff.AddKeycode(0x65,0xc6)#f5
kcff.AddKeycode(0x66,0xc7)#f6
kcff.AddKeycode(0x67,0xc8)#f7
kcff.AddKeycode(0x68,0xc9)#f8
kcff.AddKeycode(0x69,0xca)#f9
kcff.AddKeycode(0x6a,0xcb)#f10
kcff.AddKeycode(0x6b,0xcc)#f11
kcff.AddKeycode(0x6c,0xcd)#f12

kcff.WriteKeycodes()

class keyCodesFileFactory:
    def __init__(self, filePath):
        open(filePath, 'w').close()#clear file
        self.file=open(filePath,'a')
        self.file.write("const uint8_t keyboardKeysUS[256]={")
        self.associations=[0 for i in range(256)]#2**8, all possible keycodes
        self.shiftAssociations=[0 for i in range(256)]#2**8, all possible keycodes
        self.characters=['\0' for i in range(96)]#2**8, all possible keycodes //memory optimisation, last character is "=" at index 95
        self.shiftCharacters=['\0' for i in range(96)]#2**8, all possible keycodes //memory optimisation, last character is "+" at index 95
    
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
    
    def AddBothKeycodes(self,PS2Code,keyboardCode,character="\0"):
        self.AddKeycode(PS2Code, keyboardCode,character)
        self.AddShiftKeycode(PS2Code, keyboardCode, character)
    
    def WriteKeycodes(self):
        lastElem=self.associations.pop()
        lastShiftElem=self.shiftAssociations.pop()
        lastChar=self.characters.pop()
        lastShiftChar=self.shiftCharacters.pop()
        for code in self.associations:
            self.file.write(str(hex(code))+",")
        self.file.write(str(hex(lastElem))+"};//for access with PS2 key as index\nconst uint8_t keyboardShiftKeysUS[256]={")
        for code in self.shiftAssociations:
            self.file.write(str(hex(code))+",")
        self.file.write(str(hex(lastShiftElem))+"};//for access with PS2 key as index (shift pressed)\nconst uint8_t charactersUS[96]={")
        for char in self.characters:
            self.file.write("'"+char+"',")
        self.file.write("'"+lastChar+"'};//character associated to each key\nconst uint8_t shiftCharactersUS[96]={")
        for shiftChar in self.shiftCharacters:
            self.file.write("'"+shiftChar+"',")
        self.file.write("'"+lastShiftChar+"'};//character associated to each shift key")
        self.file.close()


kcff=keyCodesFileFactory("./bluetoothKeyloggerUS/keycodesUS.h")

#arduino keyboard library follow ascii hex codes, see https://www.asciitable.com/
#extra keys https://github.com/arduino-libraries/Keyboard/blob/master/src/Keyboard.h
#S means shift

kcff.AddKeycode(0x40,0x60,"`")#``
kcff.AddShiftKeycode(0x40,0x7e,"~")#~
kcff.AddKeycode(0x31,0xe1,"1")#1
kcff.AddKeycode(0x32,0xe2,"2")#2
kcff.AddKeycode(0x33,0xe3,"3")#3
kcff.AddKeycode(0x34,0xe4,"4")#4
kcff.AddKeycode(0x35,0xe5,"5")#5
kcff.AddKeycode(0x36,0xe6,"6")#6
kcff.AddKeycode(0x37,0xe7,"7")#7
kcff.AddKeycode(0x38,0xe8,"8")#8
kcff.AddKeycode(0x39,0xe9,"9")#9
kcff.AddKeycode(0x30,0xea,"0")#0
kcff.AddKeycode(0x3c,0x2d,"-")#-
kcff.AddKeycode(0x5f,0x3d,"=")#=
kcff.AddShiftKeycode(0x31,0x21,"!")#! S
kcff.AddShiftKeycode(0x32,0x1f,"@")#@ S
kcff.AddShiftKeycode(0x33,0x23,"#")## S
kcff.AddShiftKeycode(0x34,0x24,"$")#$ S
kcff.AddShiftKeycode(0x35,0x25,"%")#% S
kcff.AddShiftKeycode(0x36,0x5e,"^")#^ S
kcff.AddShiftKeycode(0x37,0x26,"&")#& S
kcff.AddShiftKeycode(0x38,0x2a,"*")#* S
kcff.AddShiftKeycode(0x39,0x28,"(")#( S
kcff.AddShiftKeycode(0x30,0x29,")")#) S
kcff.AddShiftKeycode(0x3c,0x5f,"_")#_ S
kcff.AddShiftKeycode(0x5f,0x2b,"+")#+ S

kcff.AddKeycode(0x20,0xea,"0")#numpad 0
kcff.AddKeycode(0x21,0xe1,"1")#numpad 1
kcff.AddKeycode(0x22,0xe2,"2")#numpad 2
kcff.AddKeycode(0x23,0xe3,"3")#numpad 3
kcff.AddKeycode(0x24,0xe4,"4")#numpad 4
kcff.AddKeycode(0x25,0xe5,"5")#numpad 5
kcff.AddKeycode(0x26,0xe6,"6")#numpad 6
kcff.AddKeycode(0x27,0xe7,"7")#numpad 7
kcff.AddKeycode(0x28,0xe8,"8")#numpad 8
kcff.AddKeycode(0x29,0xe9,"9")#numpad 9
kcff.AddKeycode(0x2a,0xeb,".")#numpad .
kcff.AddKeycode(0x2c,0x2b,"+")#numpad +
kcff.AddKeycode(0x2d,0x2d,"-")#numpad -
kcff.AddKeycode(0x2e,0x2a,"*")#numpad *
kcff.AddKeycode(0x2f,0x2f,"/")#numpad /
kcff.AddKeycode(0x2b,0xb0)#numpad enter

kcff.AddKeycode(0x5d,0x5b,"[")#[
kcff.AddKeycode(0x5e,0x5d,"]")#]
kcff.AddKeycode(0x5b,0x3b,";")#;
kcff.AddKeycode(0x3a,0x27,"\\'")#'
kcff.AddKeycode(0x3b,0x2c,",")#,
kcff.AddKeycode(0x3d,0x2e,".")#.
kcff.AddKeycode(0x3e,0x2f,"/")#/
kcff.AddShiftKeycode(0x5d,0x7b,"{")#{ S
kcff.AddShiftKeycode(0x5e,0x7d,"}")#} S
kcff.AddShiftKeycode(0x5b,0x3a,":")#: S
kcff.AddShiftKeycode(0x3a,0x22,'''"''')# S
kcff.AddShiftKeycode(0x3b,0x3c,"<")#< S
kcff.AddShiftKeycode(0x3d,0x3e,">")#> S
kcff.AddShiftKeycode(0x3e,0x38,"?")#? S

kcff.AddKeycode(0x5c,0x5c,"\\\\")#\
kcff.AddShiftKeycode(0x5c,0x7c,"|")#| S

kcff.AddKeycode(0x41,0x61,"a")#a
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
kcff.AddKeycode(0x4d,0x6d,"m")#m
kcff.AddKeycode(0x4e,0x6e,"n")#n
kcff.AddKeycode(0x4f,0x6f,"o")#o
kcff.AddKeycode(0x50,0x70,"p")#p
kcff.AddKeycode(0x51,0x71,"q")#q
kcff.AddKeycode(0x52,0x72,"r")#r
kcff.AddKeycode(0x53,0x73,"s")#s
kcff.AddKeycode(0x54,0x74,"t")#t
kcff.AddKeycode(0x55,0x75,"u")#u
kcff.AddKeycode(0x56,0x76,"v")#v
kcff.AddKeycode(0x57,0x77,"w")#w
kcff.AddKeycode(0x58,0x78,"x")#x
kcff.AddKeycode(0x59,0x79,"y")#y
kcff.AddKeycode(0x5a,0x7a,"z")#z
kcff.AddShiftKeycode(0x41,0x41,"A")#A S
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
kcff.AddShiftKeycode(0x4d,0x4d,"M")#M S
kcff.AddShiftKeycode(0x4e,0x4e,"N")#N S
kcff.AddShiftKeycode(0x4f,0x4f,"O")#O S
kcff.AddShiftKeycode(0x50,0x50,"P")#P S
kcff.AddShiftKeycode(0x51,0x51,"Q")#Q S
kcff.AddShiftKeycode(0x52,0x52,"R")#R S
kcff.AddShiftKeycode(0x53,0x53,"S")#S S
kcff.AddShiftKeycode(0x54,0x54,"T")#T S
kcff.AddShiftKeycode(0x55,0x55,"U")#U S
kcff.AddShiftKeycode(0x56,0x56,"V")#V S
kcff.AddShiftKeycode(0x57,0x57,"W")#W S
kcff.AddShiftKeycode(0x58,0x58,"X")#X S
kcff.AddShiftKeycode(0x59,0x59,"Y")#Y S
kcff.AddShiftKeycode(0x5a,0x5a,"Z")#Z S

kcff.AddBothKeycodes(0xfa,0xc1)#capslock
kcff.AddBothKeycodes(0x06,0x81)#leftShift #maybe add to shiftAssociastions too ?
kcff.AddBothKeycodes(0x04,0xce)#printScreen
kcff.AddBothKeycodes(0x07,0x85)#rightShift
kcff.AddBothKeycodes(0x08,0x80)#leftControl
kcff.AddBothKeycodes(0x09,0x84)#rightControl
kcff.AddBothKeycodes(0x0a,0x82)#leftAlt
kcff.AddBothKeycodes(0x0b,0x86)#altGr
kcff.AddBothKeycodes(0x0c,0x83)#GUI
kcff.AddBothKeycodes(0x0e,0x00)#context
kcff.AddBothKeycodes(0x11,0xd2)#home
kcff.AddBothKeycodes(0x12,0xd5)#end
kcff.AddBothKeycodes(0x13,0xd3)#pageUp
kcff.AddBothKeycodes(0x14,0xd6)#pageDown
kcff.AddBothKeycodes(0x15,0xd8)#leftArrow
kcff.AddBothKeycodes(0x16,0xd7)#rightArrow
kcff.AddBothKeycodes(0x17,0xda)#upArrow
kcff.AddBothKeycodes(0x18,0xd9)#downArrow
kcff.AddBothKeycodes(0x19,0xd1)#inser
kcff.AddBothKeycodes(0x1a,0xd4)#DEL
kcff.AddBothKeycodes(0x1b,0xb1)#escape
kcff.AddBothKeycodes(0x1c,0xb2)#backspace #08 works too
kcff.AddBothKeycodes(0x1d,0xb3)#tab
kcff.AddBothKeycodes(0x1e,0xb0)#enter
kcff.AddBothKeycodes(0x1f,0x20)#space

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

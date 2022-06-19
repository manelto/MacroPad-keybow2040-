# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""

import time
import board


# keyboard HID and keybow lib
# ________________________________________________________________________________________________
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()

# Set up Keybow
keybow = PMK(hardware)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control (used to send media key presses)
consumer_control = ConsumerControl(usb_hid.devices)


# I2C for OLED and Encoder with QT Stemma
i2c = hardware.i2c()

#OLED
# ____________________________________________________________________________________________________
import adafruit_ssd1306
oled  = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d)


# encoder
#___________________________________________________________________________________________________
from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel
from rainbowio import colorwheel
seesaw = seesaw.Seesaw(i2c, 0x36)
seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.5

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None



# layers config (keys and leds)
#_______________________________________________________________________________________________________

#COLOURS
RGB =  {
            0: (0,0,0), # OFF / BLACK
            1: (255,0,0), # RED
            2: (255,255,0), # YELLOW
            3: (100,200,0),
            4: (0,255,0), # GREEN
            5: (0,255,255),
            6: (0,100,100),
            7: (0,0,255), # BLUE
            8: (255,0,255),
            9: (255,255,255) # WHITE
            }

#NUMPAD
layer_numpad_1 =  {
            0: Keycode.ZERO,
            1: Keycode.ONE,
            2: Keycode.FOUR,
            3: Keycode.SEVEN,
            4: Keycode.COMMA,
            5: Keycode.TWO,
            6: Keycode.FIVE,
            7: Keycode.EIGHT,
            8: Keycode.KEYPAD_ENTER,
            9: Keycode.THREE,
            10: Keycode.SIX,
            11: Keycode.NINE,
            12: Keycode.KEYPAD_PLUS, #PLUS
            13: Keycode.KEYPAD_MINUS,
            14: Keycode.KEYPAD_ASTERISK, #MULTIPLY
            15: Keycode.KEYPAD_FORWARD_SLASH
            }


# MACRO Strings
layer_strings_2 =  {
            0: "lavanguardia.com\n",
            1: "eldiario.es\n",
            2: "elpais.com\n",
            3: "publico.es\n",
            4: "adslzone.net\n",
            5: "es.gizmodo.com\n",
            6: "xataka.com\n",
            7: "printables.com\n",
            8: "\n"
            }

# MEDIA CONTROLS
layer_3 =  {
            0: ConsumerControlCode.RECORD,
            1: ConsumerControlCode.EJECT,
            4: ConsumerControlCode.BRIGHTNESS_DECREMENT,
            5: ConsumerControlCode.VOLUME_DECREMENT,
            6: ConsumerControlCode.REWIND,
            7: ConsumerControlCode.SCAN_PREVIOUS_TRACK,
            9: ConsumerControlCode.MUTE,
            10: ConsumerControlCode.STOP,
            11: ConsumerControlCode.PLAY_PAUSE,
            12: ConsumerControlCode.BRIGHTNESS_INCREMENT,
            13: ConsumerControlCode.VOLUME_INCREMENT,
            14: ConsumerControlCode.FAST_FORWARD,
            15: ConsumerControlCode.SCAN_NEXT_TRACK}

##--------------------------------------
##|       |  <<    |Play/Pause|    >>  |
##--------------------------------------
##|       | rewind |  stop    | foward |
##--------------------------------------
##| eject |  Vol-  |MUTE      |  Vol+  |
##--------------------------------------
##| rec   | brigh -|          |brigh + |
##--------------------------------------


# WINDOWS SHORTCUTS
layer_4_shortcuts = {
            0: Keycode.KEYPAD_ENTER,
            1: [Keycode.CONTROL, Keycode.S], #save
            2: [Keycode.CONTROL, Keycode.C], #copy
            3: [Keycode.CONTROL, Keycode.V], #paste
            4: [Keycode.ALT, Keycode.SHIFT, Keycode.TAB], #switch active app
            5: [Keycode.GUI, Keycode.PERIOD], #Emoji Keyboard
            6: [Keycode.CONTROL, Keycode.X], #cut
            7: [Keycode.CONTROL, Keycode.A], #select all
            8: [Keycode.GUI, Keycode.SHIFT, Keycode.RIGHT_ARROW], # Move app to next monitor
            9: [Keycode.GUI, Keycode.UP_ARROW], #Maximize
            10: [Keycode.GUI, Keycode.DOWN_ARROW], #Minimize
            11: Keycode.HOME,
            12: [Keycode.GUI, Keycode.L], #Lock screen
            13: Keycode.PAGE_UP, # Page up
            14: Keycode.PAGE_DOWN, # Page down
            15: Keycode.END
}
##|---------------------
##|PASTE|All |HOME|END
##|---------------------
##|COPY |CUT |min |PgUp
##|---------------------
##|SAVE |EMoj|MAX |PgDn
##|---------------------
##|MOD* |APP |Mov |LOCK
##|---------------------


# Microsoft Teams Shortcuts
layer_5_teams_cuts = {
            2: [Keycode.CONTROL, Keycode.TWO], #Teams Chat
            1: [Keycode.CONTROL, Keycode.THREE], # Teams Calendar
            4: [Keycode.ALT, Keycode.SHIFT, Keycode.TAB], #switch active app
            3: [Keycode.CONTROL, Keycode.SHIFT, Keycode.M], #Teams Toggle Mute
            6: [Keycode.CONTROL, Keycode.SHIFT, Keycode.E], #Share screen
            12: [Keycode.CONTROL, Keycode.SHIFT, Keycode.B], # Leave Meeting
            7: [Keycode.CONTROL, Keycode.SHIFT, Keycode.O], #Teams Toggle Video
            11: [Keycode.CONTROL, Keycode.SHIFT, Keycode.S], #Accept call
            15: [Keycode.CONTROL, Keycode.SHIFT, Keycode.A], #Accept video
            10: [Keycode.CONTROL, Keycode.SHIFT, Keycode.D], #decline call
            14: [Keycode.CONTROL, Keycode.SHIFT, Keycode.K] #RAISE LOWER HAND
            }

layer_5_vba = {
            0: [Keycode.SHIFT,Keycode.F8],
            1: [Keycode.F5],
            4: [Keycode.SHIFT,Keycode.CONTROL,Keycode.F8],
            5: [Keycode.CONTROL,Keycode.S],
            8: [Keycode.F8],
            9: [Keycode.CONTROL, Keycode.PAUSE],
            12: [Keycode.LEFT_ALT,Keycode.F11],
            13: [Keycode.ENTER]
            }

##----------------------------
##|MUTE|VID  |A_call|A_vid|
##----------------------------
##|CHAT|SHARE|D_call|HAND |
##----------------------------
##|CALE|     |      |     |
##----------------------------
##|MOD*|APP  |      |LEAVE|
##----------------------------


## layers structure:
#  {index, [layer name, type, colors, layer id, keys text],....}
# layer name: a string with the name of layer
# keypad type: "key","string","control"
# key color: 0-9. a digit for each key
# id: the id of keys layers
# key text: the text to show in OLED
#

layers =      {1: ["teclado numerico","key","9999299919997777",layer_numpad_1,"0","1","4","7",",","2","5","8","Ent","3","6","9","+","-","*","/"],
               2: ["webs","string","9999999920000000",layer_strings_2," vang "," diar "," pais "," publ "," adsl "," gizm "," xatk "," prusa "," Enter ","","","","","","",""],
               3: ["Multimedia","control","1100375507113711",layer_3,"REC","EJCT","","","B-","V-","REW ","<<","","V0","STOP ", chr(16)+chr(19),"B+","V+","FAST",">>"],
               4: ["edicion","key","9999499919997777",layer_4_shortcuts,"Enter","save","copy","paste","nxAPP",chr(1),"cut","selAll","nxMon","Max","Rest","Home","Look","PgUP","PgDown","END"],
               5: ["VBA","key","6100470053008900",layer_5_vba,chr(16),"F5","","",chr(16)+chr(16),"Save","","","F8","<>","","","||","Enter","",""]}



# Start on layer 1
current_layer = 1

#actives keys
layer_keys = range(0, 16)

# Set the LEDs for each key in the current layer
for k in layers[current_layer][3].keys():
    keys[k].set_led(*RGB[current_layer])

# To prevent the strings (as opposed to single key presses) that are sent from
# refiring on a single key press, the debounce time for the strings has to be
# longer.
short_debounce = 0.03
long_debounce = 0.15
debounce = 0.03
fired = False

#________________________________________________________________________________________________________________
def showKeyboards():
    global current_layer
    global last_position

    seleccion = current_layer - 1
    seleccionAnterior = seleccion

    oled.fill(0)
    oled.fill_rect(0,0,12,63,1)
    oled.text("L", 3, 2, 0)
    oled.text("A", 3, 12, 0)
    oled.text("Y", 3, 22, 0)
    oled.text("E", 3, 32, 0)
    oled.text("R", 3, 42, 0)
    oled.text("S", 3, 52, 0)


    for i in range(len(layers)):
        oled.text(layers[i+1][0], 18, i*13+2, 1)

    oled.rect(15,seleccion*13,112,13,1)
    oled.show()

    seguir = False

    cambio = False
    last_position = encoder.position
    position = encoder.position

    while not seguir:
        position = encoder.position
        if position != last_position:
            if position < last_position and seleccion >= 1:
                seleccionAnterior = seleccion
                seleccion = seleccion - 1
                cambio = True
            if position>last_position and seleccion < 5:
                seleccionAnterior = seleccion
                seleccion = seleccion + 1
                cambio = True

            if cambio:
                oled.rect(15,seleccionAnterior*13,112,13,0)
                oled.show()

                oled.rect(15,seleccion*13,112,13,1)
                oled.show()

        last_position = position

        if not button.value and not seguir:
            seguir = True

    current_layer = seleccion + 1

#◘_______________________________________________________________________________________________________


oled.fill(0)
oled.show()
time.sleep(1)

oled.text("Pulsa el encoder... ", 0, 14, 1)
oled.text("   para seleccionar", 0, 28, 1)
oled.text("el modelo de teclado.",0,42,1)
oled.show()

seguir = False

n = 1
pixel.brightness = 0.1

while not seguir:
    pixel.fill(colorwheel(256-n))
    if n<257:
        n = n + 1
    else:
        n = 1

    if not button.value and not seguir:
        seguir = True
        pixel.fill(colorwheel(0))


button_held = False

while True:
    # Always remember to call keybow.update()!
    if not button.value and not button_held:
        button_held = True
        pixel.brightness = 0.2
        pixel.fill(colorwheel(255))
        showKeyboards()

    if button.value and button_held:
        button_held = False
        print("modelo: ",current_layer)

        for k in layer_keys:
            keys[k].set_led(*RGB[0])

        oled.fill(0)
        #oled.text(layers[current_layer][0], 18, 2, 1)
        #oled.rect(0,0,127,13,1)
        tope = len(layers[current_layer])-4
        for i in range(len(layers[current_layer])-4):
            if len(layers[current_layer][i+4])<3:
                n = 2
            else:
                n = 1

            oled.text(layers[current_layer][i+4], (i // 4)*33, 50-((i % 4)*17-(2-n)*4),1,size = n)
            keys[i].set_led(*RGB[int(layers[current_layer][2][i])])
        oled.show()
        pixel.fill(colorwheel(0))
        pixel.brightness = 0


    keybow.update()


    for k in layers[current_layer][3].keys():
        if keys[k].pressed:
            key_press = layers[current_layer][3][k]

            # If the key hasn't just fired (prevents refiring)
            if not fired:
                fired = True

            # Send the right sort of key press and set debounce for each
            # layer accordingly type
                if layers[current_layer][1]=="string":
                    debounce = long_debounce
                    layout.write(key_press)
                elif layers[current_layer][1]=="control":
                    debounce = short_debounce
                    consumer_control.send(key_press)
                else :
                    debounce = short_debounce
                    if isinstance(key_press, list):
                        keyboard.send(*key_press)
                    else:
                        keyboard.send(key_press)


    # If enough time has passed, reset the fired variable
    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False


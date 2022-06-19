# MacroPad-keybow2040-
a MacroPad variant with keybow2040, OLED display and rotary encoder
This project was a challenge for me. I wanted to use a Pimoroni Keybow2040 board with an OLED screen (to show the possible keyboard modes as well as the active key combination) and a rotary encoder to select the available keyboard configurations.

After several tests, I thought that it would be impossible for me to add new devices through the QT Stemma connectors. In fact, in my review of the Keybow2040 on the Pimoroni page, I gave the device a low rating, precisely because of my belief that, despite the existence of pins to connect I2C devices, it was not possible to do so. I have to correct that criticism by acknowledging my mistake and increasing the score.

And I also have to value the answer that Pimoroni gave me, which served to guide me to find the solution and, finally, carry out the project presented here.

The main code is based on one of @Gadgetoid's examples (https://github.com/pimoroni/keybow2040-circuitpython). In particular the hid-keypad-fifteen-layers.py example (https://github.com/pimoroni/keybow2040-circuitpython/blob/master/examples/hid-keypad-fifteen-layers.py).

I have changed the code somewhat to adapt it both to the new elements (OLED screen and rotary encoder) and to make it closer to my way of programming.

In any case, I think it can be used and understood by any programming neophyte and modified by any programmer with minimal knowledge of Python.

I hope that this development can help other people to use the Pimoroni Keybow2040 for their projects. It would have been very useful to me if someone had developed it before me.

Oh, and sorry if I've made a lot of mistakes in the English writing. I have needed the help of google translate.

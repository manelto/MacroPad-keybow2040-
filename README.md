# MacroPad-keybow2040-
a MacroPad variant with keybow2040, OLED display and rotary encoder
This project was a challenge for me. I wanted to use a Pimoroni Keybow2040 board with an OLED screen (to show the possible keyboard modes as well as the active key combination) and a rotary encoder to select the available keyboard configurations.

After several tests, I thought that it would be impossible for me to add new devices through the QT Stemma connectors. In fact, in my review of the Keybow2040 on the Pimoroni page, I gave the device a low rating, precisely because of my belief that, despite the existence of pins to connect I2C devices, it was not possible to do so. I have to correct that criticism by acknowledging my mistake and increasing the score.

And I also have to value the answer that Pimoroni gave me, which served to guide me to find the solution and, finally, carry out the project presented here.

The main code is based on one of @Gadgetoid's examples (https://github.com/pimoroni/keybow2040-circuitpython). In particular the hid-keypad-fifteen-layers.py example (https://github.com/pimoroni/keybow2040-circuitpython/blob/master/examples/hid-keypad-fifteen-layers.py).

I have changed the code somewhat to adapt it both to the new elements (OLED screen and rotary encoder) and to make it closer to my way of programming.

In any case, I think it can be used and understood by any programming neophyte and modified by any programmer with minimal knowledge of Python.

I hope that this development can help other people to use the Pimoroni Keybow2040 for their projects. It would have been very useful to me if someone had developed it before me.

To build the keyboard I used a 3D printer. Models can be found at
https://www.printables.com/model/228327-keybow2040-macropad-with-display-and-encoder


Oh, and sorry if I've made a lot of mistakes in the English writing. I have needed the help of google translate.

_______________________________________________________________________________________________________________________________

Now, in Spanish...


Este proyecto constituia un reto para mí. Quería utilizar una placa Keybow2040 de Pimoroni con una pantalla OLED (para mostrar los  modos de teclados posibles así como la combinación de teclas activas) y un codificador rotatorio para seleccionar las configuraciones de teclados disponibles.

Tras varias pruebas, pensé que me sería imposible añadir nuevos dispositivos mediante los conectores QT Stemma. De hecho, en la crítica que hicé al Keybow2040 en la página de Pimoroni, puse una valoración baja al dispositivo, precisamente por mi creencía de que, a pesar de la existencia de pines para conectar dispositivos I2C, no era posible hacerlo. He de corregir esa critica reconociendo mi error y aumentando la puntuación. 

Y también he de valorar la contestación que me dieron desde Pimoroni que sirvió para guiarme a encontrar la solución y, finalmente, realizar el proyecto que aquí se presenta.

El código principal esta basado en uno de los ejemplos de @Gadgetoid (https://github.com/pimoroni/keybow2040-circuitpython). En particular el ejemplo hid-keypad-fifteen-layers.py (https://github.com/pimoroni/keybow2040-circuitpython/blob/master/examples/hid-keypad-fifteen-layers.py).

He cambiado algo el código para adaptarlo tanto a los nuevos elementos (pantalla OLED y codificador rotatorio) como para hacerlo más cercano a mi manera de programar.

En cualquier caso, creo que puede ser utilizado y entendido por cualquier neofito en programación y modificado por cualquier programador con unos mínimos conocimientos de Python. 

Espero que este desarrollo pueda ayudar a otras personas a utilizar el Keybow2040 de Pimoroni para sus proyectos. A mí me hubiera sido de mucha utilizar si alguien lo hubiera desarrollado antes que yo.

Para construir el teclado he utilizado una Impresora 3D. Los modelos pueden encontrarse en
https://www.printables.com/model/228327-keybow2040-macropad-with-display-and-encoder


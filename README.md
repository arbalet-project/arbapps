# Arbalet
Arbalet is an *ARduino-BAsed LED Table*, a plane surface filled with several hundreds of coloured square lights designed for _Education_, _Geeks_, and _Pleasure_. With its limited number of pixels, Arbalet brings our old 80 arcad games back into fashion through a modern, classy, and hackable device.

Arbalet is intended to be easily reproducible, highly customizable, and programmable to create new games, light animations and applications. Whether you're looking for a modern, stylish and ready-to-use platform for your home, or a hackable and original platform to teach programming and develop exciting projects, Arbalet is made for you!

## Arbalet for Home

Arbalet is not the first LED table, but this type of device is still not common and original. Modern trends regarding interior decoration for home as well as pubs or clubs deal with LED lightning, colourful discrete and soft, provided by numerous low power lights rather than a traditional single powerful light source. However they generally use static colors or simple and poor animations. Arbalet fits into this contemporary LED universe, whilest providing greater originality, dynamism and expressivity.

Being happy? Choose an african brown-orange-beige animation! Festive? Choose a multicolor wheel. Needing serenity? A sober blue slowly flashing to white. And more to come...

## Arbalet for Hacking
As an opensource project, Arbalet is fully compatible with customization, hacking and improvements to expand possibilities and create new fascinating projects.
Geeks and DIYers will enjoy buiding their custom Aralet, and sharing it to the community.

Customization includes:
* Integration into different hosts (portable device, high-class wooded furniture, vertical walls, giant terraces...)
* Use of different hardware (especially the LED strip), for a cheaper product, or just for challenge
* Programming of new apps, games, and light effects
* Addition of different kinds of natural interaction (touch screen, hands motion, microphone, ...)
* Everything else brought to you by your imagination

## Arbalet for Education

Whether you're a teacher looking for cool tech plaforms to teach your students without boring them or just a curious guy or chick wanting to discover programming, Arbalet is made for you!

Casual programming lessons generally start explaning to newcomers how to program a computer through simple games executing in a terminal. But terminals are probably the best way to put students off programming by showing them an esoteric user interface. Let's show them that programming is not reserved to (male) nerds hacking Facebook accounts in a dark cellar with a slice of pizza and scrolling inintelligible white-on-black text on his computer screen.

Fortunately playful work platforms and tools are now being considered by teachers to teach programming, logic and algorithmic, like robots or visual programming languages. Arbalet is another affordable device enriching the palette of friendly devices to learn these academic subjects enjoying oneself.

### Arbaserver [In progress]
Arbalet comes with a server called _arbaserver_. This server allows sharing a single hardware table among several plug-and-play workstations. Without any complicated setup or logging, the teacher controling the server can choose what running application must be shown to the entire class among all students developing and testing their prototype thanks to the simulator of their workstation. The simplicity of the SDK allows students to download it on their personal computer and get ready to work instantly with a simulator. These features allow to give short personal projects (4 to 8 hours) as homework to students that they can finally present in class using real hardware.

### Arbasnap [In progress]
Apart from its python implementation, Arbalet is also compatible with the Snap! language, a visual programming language for very beginners or youngest students for whom the visual aspect of the programming interface is important. 

# Call to contributions - How can I help?
Arbalet is an opensource project under development, open to all testers, developers, comments and suggestions. If you find the project nice, please consider sharing it through social networks, recall that a community project lives only thanks to word of mouth and volunteer contributions.

# Headlines regarding Hardware and Software

Arbalet is a set of several systems communicating together:
* A multicolor LED strip of several meters long
* An [Arduino](http://en.wikipedia.org/wiki/Arduino) board implementing the protocol of the strip
* A laptop running the rest of the software
* A software development kit called _arbasdk_ providing simulation, tools and easy communication with hardware
* Python applications called _arbapps_ being the actual games or light animations

All hardware components are placed inside or above a furniture like a coffee table. Each LED is isolated from the light of others inside little closed squares formed with a plastic or wooden grid. Overhead the grid, a glass with a privacy film ensure the dispersion of the light (and incidentally allow to put objects on the table).

According to your usage, the laptop can be replaced by:
* A [Raspberry Pi](http://fr.wikipedia.org/wiki/Raspberry_Pi) board to make the table automonous
* A server concentrating client streams, to be mainly used in class (see Education section)

## The LED strip
To simplify conception, Arbalet uses adressable LED strips. Indeed, using conventionnal LEDs would require a lot of wires, soldering and electronic conception to be able to address individually each light from the computer that can be hard for beginners. Several manufacturers sell adressable color LED strips that make the conception of Arbalet really easier.

The **addressable** characteristics of the LED strip in primordial. It means that each LED can be driven independently from others. Non-adressable LED strips will usually require that all the LEDs are lit with the same color, or at least that several LEDs are lit with the same color. However we need to be able to give each single LED a different color from others. Each LED is given an adress that identify it among all others, what explains this _addressable_ keyword.

## Control
Arduino is an opensource programming board embedding Input/Output pins to communicate with external hardware. Arduino's microcontroller is programmable in [Processing langage](http://en.wikipedia.org/wiki/Processing_%28programming_language%29). However to benefit from a maximum number of libraries and software tools, the Arduino board is only used for real-time communication with the LEDs while the user application (game, light effect...) runs on a conventional computer or a Raspberry Pi running the Arbalet SDK

## Arbalet SDK for Linux, Windows and MacOS
The Arbalet Python SDK (_arbasdk_) provides a simple configuration and runtime environment to create applications.
Written in Python it is fully portable and multiplatform. The setup script [soon on pip] installs instantly all packages and dependencies. Only the Windows OS requires a preliminary installation of Python.

## My hardware is different than yours, how to configure it?
The default Arbalet geometry is 15 lineto s x 10 columns (= pixels), but you may want to create a bigger table with 300, 450 or even 600 pixels. Also, if your wiring may be different than the default one.
In those cases you will need to write a new config file (no worries, this will be only 20 minutes long). Config files are stored in the config/ folder, they describe the physical characteristics of your table. [Documentation to come]

## My hardware is now configured, how to create a new Arbalet app?
The arbasdk provides all you need to send colors to your table, the ipython notebook folder (notebooks/) is a good start to get familiar with the Arbalet API.
The next step will be to have a look to the _Arbapp_ interface, from which you should inheritate to implement most of your appplications. You'll get everything in less than 1 hour and start writing your app quickly.

### Sound, joysticks and sensors
Light effects are even better when associated to sounds and music, although there is no default way to play sound with Arbalet, using a Raspberry pi will allow you to plug speakers and integrate them to your table. USB joysticks, keyboards and sensors may also be plugged to the Pi, and advanced users can use its GPIO to plug non-USB devices to Arbalet. There is no Arbalet-specific hardware or software interface to control sound joysticks and sensors, you can use the _pygame_ module to access the first two, or more generally the python lib provided by the manufacturer of your device.

Need some ideas? You could plug touch screens, TFT screens, leapmotion, ...

Right now, Arbalet still has no official input device, they will come soon!

# Arbalet project
## Hackable LED table for geeks and pleasure
Arbalet is an *ARduino-BAsed LED Table*, a flat surface filled with several hundreds of coloured square lights designed for _Education_, _Geeks_, and _Pleasure_. With its limited number of pixels, Arbalet brings our old 80 arcad games back into fashion through a modern, classy, and hackable device.

Arbalet is intended to be easily reproducible, highly customizable, and programmable to create new games, light animations and applications. It's not only a LED table, it's an open development platform. Whether you're looking for a modern, stylish and ready-to-use platform for your home, or a hackable and original platform to teach programming and develop exciting projects, Arbalet is made for you!

Wanna get more information and/or start hacking? Please consult the [Arbalet wiki](https://github.com/arbalet-project/arbadoc/wiki), here is a video trailer to whet your appetite:

[![Arbalet video trailer](https://raw.githubusercontent.com/arbalet-project/arbadoc/master/pics/vimeo_snapshot.jpeg)](https://vimeo.com/arbalet/1)

The project has just started and is looking for beta-testers and passionate makers, to keep in touch: [![Follow @arbalet_project on Twitter](https://raw.githubusercontent.com/arbalet-project/arbadoc/master/graphical_elements/twitter.png)](https://twitter.com/arbalet_project)

## Arbapps
Arbalet's source code is organized around three repositories: [Arbasdk](https://github.com/arbalet-project/arbasdk) (Python SDK), Arbapps (Applications) and [Arbadoc](https://github.com/arbalet-project/arbadoc) (Documentation, diagrams and howtos).

*Arbapps* (Arbalet applications) is your workspace for all Arbalet applications. This repository already contains a set of basic applications written in Python, feel free to fork it, improve them and add your custom programs.

Arbalet comes with these apps:
* **bounces** are bouncing balls propelled by physical interaction with hand gestures thanks to a [LeapMotion controller](http://leapmotion.com/).
* **colors** shows nice light effets on your Arbalet table. It comes with an initial set of 6 effects: Blue flashing to white, African style, turquoise/chocolate, pink/blue, warm colors, and whole color wheel.
* **images** is a GIF renderer. It will stretch the frames to fit the whole table so it may distort the original image.
* **lightshero** is a GuitarHero-like game playable with the keys F1 to F5 of a keyboard to be holded... like a guitarist does. It's compatible with frets-on-fire songs.
* **pixeliser** reads any video in input and reduces dramatically its resolution to play it on the table. You won't be able to watch a movie for sure, but this is a simple way to create nice light effects with... nice input videos.
* **snake** is a Snake game, playable with a joystick or a keyboard. It also comes with an autoplaying AI in module `snake.ai` 
* **spectrum** 	is an online musical spectrum analyzer. Play a song from your favorite music player and it renders your song in colors
* **tetris** is... a Tetris! Playable with a joystick or a keyboard.
* **timeclock** is a very simple time clock, currently only suited for tables of size 15x10

Tools and meta-applications:
* **sequencer** is an application sequencer. Mainly written for demonstration purposes it starts Arbalet applications automatically and switch to a new one after a while or after the user asked to change.
* **server** 	is a server allowing to share hardware between several clients over the network
* **snap** 	is a bridge for the [Snap! visual programming language](http://snap.berkeley.edu/). (see the [quick start for with Snap!](https://github.com/arbalet-project/arbadoc/wiki/Meta-applications#arbasnap))

**IMPORTANT NOTE**: You **must** [download and install the Arbalet SDK](https://github.com/arbalet-project/arbadoc/wiki/Software-tutorials) before running any of these applications, otherwise you will raise an `ImportError`.

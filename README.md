# BoInG!
## A Python tune generator based on cellular automata
![boing!](https://github.com/zetof/boing/blob/master/images/boing.png)
This sequencer is based on the excellent idea of [Generative Sound Sequencer For iOS – Otomata](http://www.synthtopia.com/content/2011/07/17/generative-sound-sequencer-for-ios-otomata/).
It is written in Python and uses OSC messages to command sound generation by using synths defined in Super Collider.
The idea behind it is to create a theater, add one or more stages to it, add instruments to each stages, define how instruments will behave by setting their range and scale, the number of notes they generate and at which rate.
Melodies emmerge from bunches of migrating cells. Every time a cell hits a border, it emmits a sound defined by the instrument. Everytime two cells collide, they change direction.
This is ongoing work. Feel free to fork and make it your own!

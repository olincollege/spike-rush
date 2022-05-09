# spike-rush

A pygame implementation version of the game mode Spike Rush present in the popular game, Valorant.

## How To Play
These instructions are also present in the game itself on startup: 

Spike Rush: Pygame Implemenatation is played by two players - one attacking, one defending; the game is played on a singular keyboard with each player having a set of controls for movement, shooting, reloading, aiming, and planting the “spike.” Each player has a primary goal, but may also shoot at the opposing player in order to guarantee a victory. <br />
-The “spike” is a bomb that will go off 45 seconds after it has been successfully placed in the designated “plant zone” on the map<br />
-The spike can only be planted within the first 100 seconds after the game has started<br />
-Press “H” to view controls<br />

Attacking Player: <br />
Primary goal: Plant the spike<br />
-The attacker’s goal is to plant the spike in the plant zone before the first 100 seconds are up; it takes 4 seconds to plant<br />
Win conditions:<br />
1-Kill the defending player - since no one will be able to defuse the spike, it is considered an automatic win<br />
2-Stall the defending player long enough that the spike detonates<br />

Defending Player:<br />
Primary goal: Prevent the spike from being planted<br />
-The  defender’s goal is to prevent the attacker from planting the spike in the first 100 seconds or to defuse the spike before it blows up (the 45 seconds); it takes 7 seconds to defuse<br />
Win conditions:<br />
1-Attacking player dies before planting spike<br />
2-Spike is defused<br />
3-Attacking player has not planted within 100 seconds<br />

## Installation

From https://github.com/olincollege/spike-rush, either clone the repository or download the zip file.

The following libraries were utilized in python 3.9..7 in the Conda environment:<br />
Pygame - ``$ pip install pygame``<br />
Numpy - ``$ pip install numpy`` <br />

For unit testing:<br />
``$ pip install pytest``

## Usage

Cloning from this repository to mess around with features is welcome. No changes are necessary in order to run the code if all of the assets in images have been downloaded as well.

In order to play, run ``python run_game.py`` in the terminal.

## Controls
Show Controls - H<br />

**Player 1 - Attacking:**<br />
Move Forwards - W <br />
Move Backwards - S<br />
Move Left - A <br />
Move Right - D <br />

Shoot - X v
Reload - R <br />
Rotate Counter Clockwise - C <br /> 
Rotate Clockwise - V <br />

Plant/Defuse Spike - 4 <br />

**Player 2 - Defending:** <br />
Move Forwards - Up Arrow <br />
Move Backwards - Down Arrow <br />
Move Left - Left Arrow <br />
Move Right - Right Arrow <br />

Shoot - M <br />
Reload - L <br />
Rotate Counter Clockwise - , <br />
Rotate Clockwise - . <br />

Plant/Defuse Spike - ; <br />

## Website
The website can be found [here.](https://glowing-carnival-60eeb349.pages.github.io/)
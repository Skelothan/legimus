# *Legimus* Readme

## Installing Pygame
I used pip to install Pygame. It's probably best to follow the instructions 
[here](https://www.pygame.org/wiki/GettingStarted).

## About *Legimus*
*Legimus* is a turn-based RPG inspired by games such as Final Fantasy, Dragon 
Quest, and Octopath Traveller. 

Upon loading the game, it will generate a maze and put a boss enemy (the "Grand 
Wizard") at the end. The goal is to navigate the maze and defeat the boss. Along 
the way, the player will engage in random battles. Defeating these enemies will 
earn you experience. Your player character will level up and become stronger by 
gaining experience. I found fighting the boss fun at level 9.

Enemies will keep a record of your past actions in battle and use them to make 
predictions on what you will do. If they predict correctly, they can utilize a 
counterattack, which will nullify damage to them and do extra damage to you. The 
goal for the player is to try and figure what attack, if any, the enemy is 
trying to counter, and then take a different action.

The name, *Legimus*, is derived from the Latin word meaning "we read". I chose 
this name because the enemies are trying to "read" your actions. If this were a 
full length game, I would love to include visual theming around books.

## Running the Project

Navigate to the project folder in your terminal and run 
`python3 overworld_v08.py`.

## Controls

### Overworld
WASD or arrow keys: move

J (debug command): Give your player character 500 experience points. You'll level up (if you're eligible) after completing the next fight.

K (debug command): Fully restore your player character's HP and SP.

### Menus and Battle
W, S, or up and down arrow keys: move menu cursor up and down. 

Enter or Space: select menu option

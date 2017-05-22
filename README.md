# Artificial Intelligence Engineer Nanodegree
## Game-Playing Agents
### Project: Sign Language Recognition System

![Example game of isolation](viz.gif)

In this project, I developed an adversarial search agent to play the game "Isolation".  Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.  These rules are implemented by Udacity in the `isolation.Board` class provided in the repository. 

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

I only needed to modify code in the `game_agent.py` file to complete the project.  Additional files include example Player and evaluation functions, the game board class, and a template to develop local unit tests.  

## Getting Started

To get this code on your machine you can fork the repo or open a terminal and run this command.
```sh
git clone https://github.com/JonathanKSullivan/Sign-Language-Recognizer.git
```

### Prerequisites

This project requires **Python 3** and the following Python libraries installed:

- [NumPy](http://www.numpy.org/)
- [SciPy](https://www.scipy.org/)
- [scikit-learn](http://scikit-learn.org/0.17/install.html)
- [pandas](http://pandas.pydata.org/)
- [matplotlib](http://matplotlib.org/)
- [jupyter](http://ipython.org/notebook.html)

##### Notes: 
1. It is highly recommended that you install the [Anaconda](http://continuum.io/downloads) distribution of Python and load the environment included below.
I used pygame to help me visualize mu programs so that I have beautiful visualizations of AI I can share with others in your portfolio. However, pygame is optional as it can be tricky to install. 

### Installing
#### Mac OS X and Linux
1. Download the `aind-environment-unix.yml/aind-environment-unix.yml`/`aind-environment-osx.yml` file at the bottom of this section.
2. Run `conda env create -f aind-environment-unix.yml`(or `aind-environment-osx.yml`) to create the environment.
then source activate aind to enter the environment.

#### Windows
1. Download the `aind-environment-windows.yml` file at the bottom of this section.
2. `conda env create -f aind-environment-windows.yml` to create the environment.
then activate aind to enter the environment.


#### Optional: Install Pygame
I used pygame to help you visualize my programs so that I have beautiful visualizations of AI I can share with others in my portfolio. 
##### Mac OS X
1. Install [homebrew](http://brew.sh/)
2. `brew install sdl sdl_image sdl_mixer sdl_ttf portmidi mercurial`
3. `source activate aind`
4. `pip install pygame`
Some users have reported that pygame is not properly initialized on OSX until you also run `python -m pygame.tests`.

Windows and Linux
1. `pip install pygame`
2. In Windows, an alternate method is to install a precompiled binary wheel:
    1. Download the appropriate `pygame-1.9.3-yourpythonwindows.whl` file from here
    2. Install with `pip install pygame-1.9.3-yourpythonwindows.whl`.


Download the one of the following yml files:
[aind-environment-osx.yml](https://d17h27t6h515a5.cloudfront.net/topher/2017/April/58ee7e68_aind-environment-macos/aind-environment-macos.yml)
[aind-environment-unix.yml](https://d17h27t6h515a5.cloudfront.net/topher/2017/April/58ee7eff_aind-environment-unix/aind-environment-unix.yml)
[aind-environment-windows.yml](https://d17h27t6h515a5.cloudfront.net/topher/2017/April/58ee7f6c_aind-environment-windows/aind-environment-windows.yml)

## Running the tests

Test are included in notebook. To run test from terminal, navigate to project directory and run 
```sh
    agent_test.py
```

## Deployment
##### Game Visualization
The isoviz folder contains a modified version of chessboard.js that can animate games played on a 7x7 board. In order to use the board, you must run a local webserver by running python -m http.server 8000 from your project directory (you can replace 8000 with another port number if that one is unavailable), then open your browser to http://localhost:8000 and navigate to the /isoviz/display.html page. Enter the move history of an isolation match (i.e., the array returned by the Board.play() method) into the text area and run the match. Refresh the page to run a different game. (Feel free to submit pull requests with improvements to isoviz.)

##### Agent vs NPC Competition 
To see the outcome of my agent performing against other agents
run `tournament.py`

## Built With

* [Jupyter](http://www.http://jupyter.org/) - The Document Editor used
* [Anaconda](https://www.continuum.io/downloads) - The data science platform used


## Authors
* **Udacity** - *Initial work* - [AIND-Isolation](https://github.com/udacity/AIND-Isolation)
* **Jonathan Sulivan**

## Acknowledgments
* Hackbright Academy
* Udacity

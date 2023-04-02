# Memory-Puzzle-Game-in-Python
This is a memory puzzle game developed using Python and the Pygame library. The game features a visually appealing interface with a grid of cards, each with a hidden image. The player must flip over pairs of cards to find matches and rack up points. The game includes a scoring system and tracks the player's progress throughout the game. The code utilizes object-oriented programming concepts, Pygame's built-in event handling mechanism, and several helper functions to handle game logic and rendering. Additionally, the game's visual elements are defined using RGB color values and the game's state is stored in global variables. The code also employs the use of the random module to randomly generate the game's board and shuffle the shapes and colors on the board. The repository includes detailed instructions on how to set up and run the game, including any dependencies that need to be installed. This is a fun and interactive way to test your memory skills.

The key takeaways from this project include the following:
A basic understanding of the Python programming language, including data types, control statements, and functions, is necessary to follow along.
Pygame is a powerful library that can be used to create a graphical user interface, handle user input, and display images and animations.
Implementing the game logic, such as generating a random set of cards, shuffling them, and allowing the player to flip cards and match pairs is the core of the game.
Adding animation effects can greatly improve the overall user experience of the game.

The development process will be broken down into several steps, each step adding a new layer of functionality to our game. We'll start by initializing the Pygame library and setting up the game environment. Next, we'll implement the event handling system, allowing the player to interact with the game using input devices such as the keyboard and mouse.

Complete Code

The core functionality of the game is implemented in the main game loop within the main() function, which continually updates the game state and checks for player input. The main elements of the game logic are:

Generating a randomized board: The symbols on the game board are generated randomly using the getRandomizedBoard() function. It returns a 2D list of symbols.
Handling player input: The player interacts with the game using the mouse. The game continuously checks for mouse events, like mouse movement and mouse clicks, using the pygame.event.get() function.
Revealing boxes: The generateRevealedBoxesData() function is used to create a 2D list containing a Boolean value for each box on the board indicating whether the box is currently revealed or hidden. When a box is clicked, its corresponding value in the revealedBoxes list is set to True.
Checking for matches: If the player clicks on two boxes, the game checks if the symbols behind those boxes match or not. If they match, the game marks both boxes as "revealed" and increases the player's score. If they don't match, the game hides both boxes.
Checking for the end of the game: The game ends when all the boxes on the game board have been revealed.
Drawing the game: The game continuously redraws the game board in its current state. The drawBoard() function is used to draw the game board, and the drawHighlightBox function is used to highlight the boxes when the mouse is over them.

Altogether, these elements work together to implement the game's core functionality, allowing the player to select boxes, reveal them, check for matches and determine the end of the game.


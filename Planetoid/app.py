"""
Primary module for Alien Invaders

This module contains the main controller class for the Planetoids application. There
is no need for any any need for additional classes in this module. If you need more
classes, 99% of the time they belong in either the wave module or the models module. If
you are ensure about where a new class should go, post a question on Ed Discussions.

Name: Narayan Jat
Date: 15 May, 2023
"""
from consts import *
from game2d import *
from wave1 import *
import json

# PRIMARY RULE: Planetoids can only access attributes in wave.py via getters/setters
# Planetoids is NOT allowed to access anything in models.py

class Planetoids(GameApp):
    """
    The primary controller class for the Planetoids application
    
    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.
        
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class. Any initialization should be done in
    the start method instead. This is only for this class. All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state. For a complete description of how the states work, see the 
    specification for the method update().
    
    As a subclass of GameApp, this class has the following (non-hidden) inherited
    INSTANCE ATTRIBUTES:
    
    Attribute view: the game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView
    
    Attribute input: the user input, used to control the ship and change state
    Invariant: input is an instance of GInput
    
    This attributes are inherited. You do not need to add them. Any other attributes
    that you add should be hidden.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _state: the current state of the game as a value from consts.py
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED, 
    #            STATE_ACTIVE, STATE_CONTINUE
    #
    # Attribute _wave: the subcontroller for a single wave, which manages the game
    # Invariant: _wave is a Wave object, or None if there is no wave currently active.
    #            _wave is only None if _state is STATE_INACTIVE.
    #
    # Attribute _title: the game title
    # Invariant: _title is a GLabel, or None if there is no title to display. It is None 
    #            whenever the _state is not STATE_INACTIVE.
    #
    # Attribute _message: the currently active message
    # Invariant: _message is a GLabel, or None if there is no message to display. It is 
    #            only None if _state is STATE_ACTIVE.
    #
    # Attribute _sdown: Whether the 'S' was held down last frame
    # Invariant: _sdown is a boolean.
    #
    # Attribute _shieldTime: This is time for which shield to be shielded. 
    # Invariant: It is integer at starting it zero.
    #
    # Attribute _background: It is the background color at different stages of the game.
    # Invariant: It must be of the type GLabel.
    #
    # Attribute _scoreCard: It is the score board on the upper most part of the screen.
    # Invariant: It must be of the type GLabel.
    #
    # Attribute _level: It is the level of the game.
    # Invariant: It must be a value at starting it is zero.
    #
    # Attribute _right: Whether the 'right' was held down last frame.
    # Invariant: right is a boolean. 

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and creates both 
        the title (in attribute _title) and a message (in attribute _message) saying 
        that the user should press a key to play a game.
        """
        self._state = STATE_INACTIVE
        self._title = GLabel(font_size = TITLE_SIZE, font_name = TITLE_FONT, x = GAME_WIDTH / 2, 
            y = GAME_HEIGHT / 2 + TITLE_OFFSET, text = 'Planetoid')
        self._message = GLabel(font_size = MESSAGE_SIZE, font_name = MESSAGE_FONT, x = GAME_WIDTH/ 2, 
            y = GAME_HEIGHT / 2 + MESSAGE_OFFSET, text = 'Press S to start')
        self._background = GLabel(x = GAME_WIDTH / 2, y = GAME_HEIGHT / 2, width = GAME_WIDTH, 
            height = GAME_HEIGHT, fillcolor = RGB(210, 218, 217))
        self._sdown = False
        self._right = False
        self._wave = None
        self._level = 1
        self._shieldTime = 0
        self._scoreCard = GLabel(font_size = SCORE_SIZE, font_name = MESSAGE_FONT, x = GAME_WIDTH/ 2, 
            y = GAME_HEIGHT - 20, width = GAME_WIDTH, height = 40, fillcolor = RGB(217, 218, 210))

    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game. That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_LOADING,
        STATE_ACTIVE, STATE_PAUSED, and STATE_CONTINUE. Each one of these does its own
        thing, and might even needs its own helper. We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens. It is a
        paused state, waiting for the player to start the game. It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key. In addition, the application returns to this state
        when the game is over (all lives are lost or all planetoids are destroyed).
        
        STATE_LOADING: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay. The player can move the
        ship and fire bullets. All of this should be handled inside of class Wave
        (NOT in this class). Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.
        
        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineInput()
        # if self._state == STATE_LOADING:
        #     self._title = None
        if self._state == STATE_ACTIVE:
            if self._wave.lives > 0:
                if len(self._wave.asteroid) != 0:
                    if self._wave.ship == None:
                        self._state = STATE_PAUSED
                    else:
                        self._shieldTime += 1
                        self._wave.checkShield(self._shieldTime)
                        self._wave.update(self.input)
                else:
                    self._state = STATE_COMPLETE
            else:
                self._state = STATE_COMPLETE
                                
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. To draw a GObject
        g, simply use the method g.draw(self.view). It is that easy!
        
        Many of the GObjects (such as the ships, planetoids, and bullets) are attributes 
        in Wave. In order to draw them, you either need to add getters for these 
        attributes or you need to add a draw method to class Wave. We suggest the latter. 
        See the example subcontroller.py from class.
        """
        if self._state != STATE_INACTIVE and self._state != STATE_COMPLETE:
            self._scoreBoard(f'score: {self._wave.score[0]}   Lives: {self._wave.lives}   Level: {self._level}')
        if self._state == STATE_INACTIVE:
            self._background.draw(self.view)
            self._message.draw(self.view)
            self._title.draw(self.view)
        elif self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
            # print(self._wave.score[1])
        elif self._state == STATE_PAUSED:
            self._wave.draw(self.view)
            self._messages('PRESS S TO CONTINUE', TITLE_OFFSET)     
        elif self._state == STATE_COMPLETE:
            self._background.fillcolor = RGB(210, 218, 217)
            self._background.draw(self.view)
            self._completionMessage()

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineInput(self):
        '''
        This is helper of update method which helps it to identify state.

        This helper is checking input and based on that it is changing states of the game.
        '''
        check = self.input.is_key_down('s') and not self._sdown
        if not self._sdown and check and (self._state == STATE_INACTIVE or self._state == STATE_COMPLETE):
            self._state = STATE_LOADING
            self._level -= 1
            self._nextLevel()         
        elif self._sdown and self._state == STATE_LOADING:
            self._state = STATE_ACTIVE
        elif self._sdown and self._state == STATE_PAUSED:
            self._state = STATE_CONTINUE
        if self._sdown and self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE
            self._wave.ship = self._wave.data
            self._activateShield()
        self._sdown = self.input.is_key_down('s')
        if self._state == STATE_COMPLETE and self._wave.score[0] > self._wave.score[1] * 65/ 100:
            self._determineInputHelper()

    def _determineInputHelper(self):
        '''
        This is helper function for the function _determineInput.
        '''
        check1 = self.input.is_key_down('right') and not self._right
        if check1 and not self._right and self._state == STATE_COMPLETE:
            self._nextLevel()
        self._right = self.input.is_key_down('right')        

    def _messages(self, text, position):
        '''
        This is a helper method to set new messages at different states of game.

        Parameter text: This is text to be showed.
        Precondition: must be a string.

        Parameter position: This is position of the text to be showed.
        Precondition: It is a float or integer.
        '''

        # Problem here we are changing the self._message attribute by two ways
        # 1. is by assigning it the same object type as earlier but creating new object of it.
        # self._message = GLabel(font_size = MESSAGE_SIZE, font_name = MESSAGE_FONT, x = GAME_WIDTH/ 2, 
        #     y = GAME_HEIGHT / 2 + position, text = text)
        #2. by changing the content of the object type assigned to the 
        # self._message as follows:
        self._message.text = text
        self._message.x = GAME_WIDTH / 2
        self._message.y = GAME_HEIGHT / 2 + position
        self._message.draw(self.view)

        # Problem is that from both ways anyway content of the object assigned to 
        # self._message is changing but both are giving different results.
        # 1. implementation giving all messages printed at once on the screen
        # but 2. is only printing the most last one message passed to the method. why 
        # it is happening whereas both ways should give the same output.
        

    def _activateShield(self):
        '''
        This is helper to activate shield for ship at starting and just after collision.
        '''
        self._wave.shield = self._wave.ship
        self._shieldTime = 0

    def _scoreBoard(self, score):
        '''
        This is helper to show scoreboard at the top of the window.
        '''
        self._background.fillcolor = RGB(0, 0, 139)
        self._scoreCard.text = score
        self._background.draw(self.view)
        self._scoreCard.draw(self.view)

    def _completionMessage(self):
        '''
        It shows a message when game is completed.

        It updates the message based on the win or loss in the game.
        '''
        if self._wave.score[0] < self._wave.score[1] * 65/ 100:
            self._messages('LEVEL NOT COMPLETED', 2 * TITLE_OFFSET)
            self._messages('LEVEL NOT COMPLETED', TITLE_OFFSET)
            self._messages(f'SCORE: {self._wave.score[0]}', 0)
            self._messages('PRESS S TO PLAY AGAIN', MESSAGE_OFFSET)
        else:
            self._messages('CONGRATS YOU COMPLETED', TITLE_OFFSET)
            self._messages(f'SCORE: {self._wave.score[0]}', 0)
            self._messages('PRESS S TO PLAY AGAIN', MESSAGE_OFFSET)
            self._messages('Press right to play next', -140)

    def _nextLevel(self):
        '''
        This is method to bring next level in the game.
        '''
        try:
            self._wave = Wave(GameApp.load_json(LEVELS[self._level]))
            self._activateShield()
            self._state = STATE_ACTIVE
            self._level += 1
        except:
            self._state = STATE_INACTIVE
            self._title.text = 'CONGRATS'
            self._messages('YOU CLEARED ALL LEVELS', MESSAGE_OFFSET)

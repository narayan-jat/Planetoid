"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

Name: Narayan Jat
Date: 15 May, 2023
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you wone or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _astroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    #
    # Attribute _shield: It is the shield for the ship.
    # Invariant: It must be of type Shield.
    #
    # Attribute _scores: It is the score of the game.
    # Invariant: It must be value list storing current score and maximum score in particular level.

    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property 
    def ship(self):
        '''
        It is the ship.
        '''
        return self._ship

    @ship.setter
    def ship(self, other):
        '''
        It sets the ship to the _ship attribute of Wave.

        Parameter other: It is the data required for the creating a ship.
        Precondition: It must be a dictionary.
        '''
        assert type(other) == dict, repr(other) + ' This is not a dictionary'
        self._ship = Ship(other)

    @property
    def data(self):
        '''
        It is the data of all asteroids and ship.
        '''
        return self._data
    
    @property
    def shield(self):
        '''
        It is the shield of the ship.
        '''
        return self._shield

    @shield.setter
    def shield(self, other):
        '''
        It sets the shield of ship at it's current position.

        Parameter other: It is data of ship for which shield is to be applied.
        Precondition: It must be of type Ship.
        '''
        assert type(other) == Ship, repr(other) + ' This is not a Ship object'
        self._shield = Shield(other)

    @property 
    def lives(self):
        '''
        It is the lives of player.
        '''
        return self._lives

    @property 
    def asteroid(self):
        '''
        These are the asteroids.
        '''
        return self._astroids

    @property 
    def score(self):
        '''
        This is the score of the player.
        '''
        return self._scores

    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self, data):
        '''
        It initializes the Wave object.

        Parameter data: It is the dataset required to draw ship and asteroids.
        Precondition: It must be of type dict.
        '''
        assert type(data) == dict, repr(data) + ' This is not a dictionary'
        astData = data['asteroids']
        self._data = data
        self._ship = Ship(data)
        self._astroids = []
        self._bullets = []
        self._firerate = BULLET_RATE
        self._lives = SHIP_LIVES
        self._shield = Shield(self.ship)
        self._astroidCreation(astData)
        self._scores = [0, self._maxScore()]
        

    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, inp):
        '''
        It updates the ship, bullets and asteroids.

        Parameter inp: It is the input attribute of app class.
        Precondition: It must of type GInput.
        '''
        self._ship.turn(inp)
        self._ship.move(inp)
        self._firerate += 1
        if inp.is_key_down('spacebar') and self._firerate > BULLET_RATE:
            self._bullets.append(Bullet(self._ship.facing, self._ship.position))
            pewSound = Sound('pew1.wav')
            pewSound.play()
            self._firerate = 0
        for i in self._astroids:
            i.move()
        self._collisionBull()
        self._collisionShip()

    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self, view):
        '''
        This is method to draw all the objects to the screen.

        Parameter view: It is the screen to draw upon.
        Precondition: It must of type Planetoids.
        '''
        if self._ship != None:
            if self._shield != None:
                self._shield.move(self.ship)
                self._shield.draw(view)
            self._ship.draw(view)
        self._drawAndDelBullets(view)        # function to Delete bullets.
        for i in self._astroids:
            i.draw(view)
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def checkShield(self, value):
        '''
        It is helper to check the shield of the ship.

        Parameter value: It is the value of shiled time.
        Precondition: It must be of value.
        '''
        if value > SHIELD_TIME:
            self._shield = None

    def _astroidCreation(self, astData):
        '''
        It is the helper to create astroids.

        Parameter astData: It is the data required to create asteroids.
        Precondition: It must be a list type.
        '''
        for i in range(len(astData)):
            ast = astData[i]
            pos = ast['position']
            if ast['size'] == LARGE_ASTEROID:
                self._astroids.append(Asteroid(Vector2(ast['direction'][0], ast['direction'][1]), ast['size'], 
                    x = pos[0], y = pos[1], width = 2 * LARGE_RADIUS, height = 2 * LARGE_RADIUS, source = LARGE_IMAGE))
            elif astData[i]['size'] == MEDIUM_ASTEROID:
                self._astroids.append(Asteroid(Vector2(ast['direction'][0], ast['direction'][1]), ast['size'], 
                    x = pos[0], y = pos[1], width = 2 * MEDIUM_RADIUS, height = 2 * MEDIUM_RADIUS, source = MEDIUM_IMAGE))
            else:
                self._astroids.append(Asteroid(Vector2(ast['direction'][0], ast['direction'][1]), ast['size'], 
                    x = pos[0], y = pos[1], width = 2 * SMALL_RADIUS, height = 2 * SMALL_RADIUS, source = SMALL_IMAGE))

    def _drawAndDelBullets(self, view):
        '''
        It is helper to draw to bullet and delete going far from on screen.

        Parameter view: It is screen to draw upon.
        Precondition: It must be of type Planetoids.
        '''
        i = 0
        while i < len(self._bullets):
            self._bullets[i].draw(view)
            self._bullets[i].move()
            if self._bullets[i].x > GAME_WIDTH or self._bullets[i].x < 0:
                self._bullets.pop(i)
                i -= 1
            elif self._bullets[i].y > GAME_HEIGHT or self._bullets[i].y < 0:
                self._bullets.pop(i)
                i -= 1
            i += 1

    def _collisionShip(self):
        '''
        This helper to detect collision between ship and asteroids.
        '''
        i = 0
        while i < len(self._astroids):
            radiiSumShip = (self._astroids[i].width + self._ship.width) / 2
            ast = self._astroids[i]
            distanceShip = math.sqrt((ast.x - self._ship.x) ** 2 + (ast.y - self._ship.y) ** 2)
            if radiiSumShip >= distanceShip:
                Sound('explosion.wav').play()
                self._breakUp(self.ship, self._astroids[i])
                if self.shield == None:
                    self._lives -= 1
                    self._ship = None
                    self._scores[0] -= 10
                self._astroids.pop(i)
                break
            i += 1

    def _collisionBull(self):
        '''
        This is helper to detect collision between bullets and asteroids.
        '''
        j = 0
        while j < len(self._bullets):
            i = 0
            while i < len(self._astroids):
                radiiSum = (self._astroids[i].width + self._bullets[j].width) / 2
                ast = self._astroids[i]
                distance = math.sqrt((ast.x - self._bullets[j].x) ** 2 + (ast.y - self._bullets[j].y) ** 2)          
                if radiiSum >= distance:
                    # self._soundHelper(self._astroids[i])
                    self._breakUp(self._bullets[j], self._astroids[i])
                    self._astroids.pop(i)
                    self._bullets.pop(j)
                    j -= 1
                    break
                i += 1
            j += 1

    def _breakUp(self, other, ast):
        '''
        This is helper to break asteroid on the basis of their sizes.

        Parameter other: It is the either ship or bullet object.
        Precondition: It must of type either Ship or Bullets.

        Parameter ast: It is asteroid object.
        Precondition: It must be of type Asteroids.
        '''
        if other.velocity.length() != 0:
            vect = other.velocity
        else:
            vect = other.facing
        direction = vect.normalize()
        direction1 = Vector2(vect.x * math.cos(degToRad(120)) - vect.y * math.sin(degToRad(120)), 
            vect.x * math.sin(degToRad(120)) + vect.y * math.cos(degToRad(120)))
        direction2 = Vector2(vect.x * math.cos(degToRad(240)) - vect.y * math.sin(degToRad(240)), 
            vect.x * math.sin(degToRad(240)) + vect.y * math.cos(degToRad(240)))
        self._newAsteroid(direction, direction1, direction2, ast)

    def _newAsteroid(self, direction, direction1, direction2, ast):
        '''
        This is helper to create new asteroids upon breaking older one.

        Parameter direction: This is direction vector of first asteroid.
        Precondition: It must be a vector object.

        Parameter direction1: This is direction vector of second asteroid.
        Precondition: It must be a vector object.

        Parameter direction2: This is direction vector of third asteroid.
        Precondition: It must be a vector object.

        Parameter ast: It is asteroid object.
        Precondition: It must be of type Asteroids.
        '''
        if ast.size == LARGE_ASTEROID:
            self._scores[0] += 5
            self._newAsteroidHelper(ast, MEDIUM_ASTEROID, direction, direction1, direction2, MEDIUM_SPEED, MEDIUM_RADIUS, MEDIUM_IMAGE)
        elif ast.size == MEDIUM_ASTEROID:
            self._scores[0] += 10
            self._newAsteroidHelper(ast, SMALL_ASTEROID, direction, direction1, direction2, SMALL_SPEED, SMALL_RADIUS, SMALL_IMAGE)
        else:
            self._scores[0] += 15

    def _newAsteroidHelper(self, ast, size, direction, direction1, direction2, speed, radius, image):
        '''
        This is helper function for function named newAsteroids it.

        This is will create new asteroids only based on given parameters.

        Parameter ast: It is asteroid object.
        Precondition: It must be of type Asteroids.

        Parameter direction: This is direction vector of first asteroid.
        Precondition: It must be a vector object.

        Parameter direction1: This is direction vector of second asteroid.
        Precondition: It must be a vector object.

        Parameter direction2: This is direction vector of third asteroid.
        Precondition: It must be a vector object.

        Parameter speed: It is the speed to be assigned to asteroid.
        Precondition: It must be value.

        Parameter radius: It is the radius of asteroid.
        Precondition: It must be a value.

        Parameter image: It is the image file name for the image of asteroid.
        Precondition: It must be a valid file name.
        '''
        s, r, i = speed, radius, image
        self._astroids.append(Asteroid(direction, size, x = ast.x + (direction * r).x, 
            y = ast.y + (direction * r).y, width = 2 * r, height = 2 * r, source = i))
        self._astroids.append(Asteroid(direction1, size, x = ast.x + (direction1 * r).x, 
            y = ast.y + (direction1 * r).y, width = 2 * r, height = 2 * r, source = i))
        self._astroids.append(Asteroid(direction2, size, x = ast.x + (direction2 * r).x, 
            y = ast.y + (direction2 * r).y, width = 2 * r, height = 2 * r, source = i))

    def _soundHelper(self, ast):
        '''
        This is helper to create different type of sounds for different type of collision.

        Parameter ast: It is asteroid object.
        Precondition: It must be of type Asteroids.
        '''
        if ast.size == LARGE_ASTEROID:
            Sound('blast1.wav').play()
        elif ast.size == MEDIUM_ASTEROID:
            Sound('blast2.wav').play()
        else:
            Sound('blast4.wav').play()

    def _maxScore(self):
        '''
        This is helper to calculate maximum score in a particular level of the game.
        '''
        ast = self.asteroid
        large, medium, small = 0, 0, 0 
        for i in ast:
            if i.size == LARGE_ASTEROID:
                large += 1
            elif i.size == MEDIUM_ASTEROID:
                medium += 1
            else:
                small += 1
        maxScore = large * 5 + (medium + large * 3) * 10 + (small + (medium + large * 3) * 3) * 15
        return maxScore

"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

Name: Narayan Jat
Date: 15 May, 2023
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION ADDING VELOCITY AND WRAPPING OBJECTS.
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180

def velocityAdder(obj):
    '''
    This function adds velocity to the x and y components of the object.

    Parameter obj: This is object to which velocity is to be added.
    Precondition: This is object of any class which is having x and y as attribute 
    and also velocity attribute.
    '''
    obj.x += obj._velocity.x 
    obj.y += obj._velocity.y

def objectWrapper(obj):
    '''
    This function wrap object on the screen.

    Parameter obj: This is object which is to be wrapped up.
    Precondition: This is object of any class which is having x and y as attribute.
    '''
    if obj.x >= GAME_WIDTH + DEAD_ZONE:
        obj.x = - DEAD_ZONE
    elif obj.x < - DEAD_ZONE:
        obj.x = GAME_WIDTH + DEAD_ZONE
    if obj.y >= GAME_HEIGHT + DEAD_ZONE:
        obj.y = - DEAD_ZONE
    elif obj.y < - DEAD_ZONE:
        obj.y = GAME_HEIGHT + DEAD_ZONE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _velocity: It is the velocity of bullet.
    # Invariant: It must be a vector object. 
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    def velocity(self):
        '''
        It is the velocity of the Bullet.
        '''
        return self._velocity

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, facing, position):
        '''
        Initializes the Bullet objects.

        Parameter facing: It is the direction of the Bullet.
        Precondition: It must be non-zero vector.

        Parameter position: It is the position of the bullet.
        Precondition: It must be list or tuple type object
        '''
        self._velocity = facing * BULLET_SPEED
        product = facing * SHIP_RADIUS
        super().__init__(fillcolor = BULLET_COLOR, width = 2 * BULLET_RADIUS, height = 2 * BULLET_RADIUS, 
            x = position[0] + product.x, y = position[1] + product.y)

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        '''
        This is helper to move bullets across the screen.
        '''
        velocityAdder(self)

class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vector (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _velocity: It is the velocity of bullet.
    # Invariant: It must be a vector object.
    #
    # Attribute _facing: It is the direction of bullet.
    # Invariant: It is object of the vector.

    # Attribute moveTrack = It is the value to track record of up key press once pressed then 
    #ship should move always._velocity.
    # Invariant: It must be a value.

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    def velocity(self):
        '''
        It is the velocity of the Ship.
        '''
        return self._velocity

    @property
    def facing(self):
        '''
        It is the facing of the Ship.
        '''
        return self._facing

    @property
    def position(self):
        '''
        It is the position of the Ship.
        '''
        return (self.x, self.y)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, data):
        '''
        Initializes the Ship object.

        Parameter data: It is the data type which store the all initial values for ship.
        Precondition: It must be a dictionary.
        '''
        self._facing = Vector2(math.cos(degToRad(data['ship']['angle'])), math.sin(degToRad(data['ship']['angle'])))
        self._velocity = Vector2(0, 0)
        self.moveTrack = False
        super().__init__(x = data['ship']['position'][0], y = data['ship']['position'][1], width = 2 * SHIP_RADIUS, 
            height = 2 * SHIP_RADIUS, angle = data['ship']['angle'], source = SHIP_IMAGE)
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self, inp):
        '''
        It is helper method to turn the Ship.

        Parameter inp: It is the input attribute of the class Planetoids.
        Precondition: It must be the input attribute of Planetoids which is already 
        created in GameApp.
        '''
        if inp.is_key_down('left'):
            self.angle += SHIP_TURN_RATE
        if inp.is_key_down('right'):
            self.angle -= SHIP_TURN_RATE
        self._facing = Vector2(math.cos(degToRad(self.angle)), math.sin(degToRad(self.angle)))

    def move(self, inp):
        '''
        This is helper to move ship across the screen.

        Parameter inp: It is the input attribute of the class Planetoids.
        Precondition: It must be the input attribute of Planetoids which is already 
        created in GameApp.
        '''
        if inp.is_key_down('up'):
            self.moveTrack = True
            impulse = self._facing * SHIP_IMPULSE
            self._velocity =  self._velocity + impulse
        if self.moveTrack:
            speed = self._velocity.length()
            if speed <= SHIP_MAX_SPEED:
                velocityAdder(self)
            else:
                self._velocity = self._velocity.normalize() * SHIP_MAX_SPEED
                velocityAdder(self)
        objectWrapper(self)


class Asteroid(GImage):
    """ 
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _size: It is the size of the of asteroid.
    # Invariant: It must be a string.
    
    # Attribute _velocity: It is the velocity of the asteroid.
    # Invariant: It is the object of the vector.
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    def velocity(self):
        '''
        It is the velocity of the Aasteroid.
        '''
        return self._velocity

    @property
    def size(self):
        '''
        It is the size of the asteroid.
        '''
        return self._size
    
    # INITIALIZER TO CREATE A NEW ASTEROID 
    def __init__(self, direction, size, **data):
        '''
        Initializes the object of the Asteeroid.

        Parameter size: It is the size of the asteroid.
        Precondtion: It must be string.

        Parameter direction: It is the direction of the asteroid.
        Precondition: It must be non-zero vector.

        Parameter **data: It is the dictionary of the random number of passed keyword arguments.
        Precondition: It must be a dictionary.
        '''
        super().__init__(**data)
        self._size = size
        if direction.length() == 0:
            direction = Vector2(math.cos(0), math.sin(0))
        if self._size == 'large':
            velo = direction.normalize() * LARGE_SPEED
        elif self._size == 'medium':
            velo = direction.normalize() * MEDIUM_SPEED
        else:
            velo = direction.normalize() * SMALL_SPEED
        self._velocity = velo

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def move(self):
        '''
        It is helper of asteroid to move asteroids.
        '''
        velocityAdder(self)
        objectWrapper(self)


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Shield(GEllipse):
    '''
    It is class representing shield of ship.
    '''

    def __init__(self, ship):
        '''
        Initializes the object of shield class.

        Parameter ship: It is ship.
        Precondition: It must be Ship object.
        '''
        super().__init__(x = ship.position[0], y = ship.position[1], width = 2 * SHIELD_SCALE * SHIP_RADIUS , height = 2 * 78 / 58 * SHIP_RADIUS, fillcolor = RGB(255, 68, 204))

    def move(self, ship):
        '''
        It is helper of Shield class to move a shield.

        Parameter ship: It is ship.
        Precondition: It must be Ship object.
        '''
        self.x += ship.velocity.x
        self.y += ship.velocity.y

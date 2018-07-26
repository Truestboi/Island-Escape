import pyglet
from pyglet.window import key

import cocos
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer, ScrollableLayer
from cocos.director import director
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.actions import *
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

from pyglet.window.key import symbol_string

keyboard = key.KeyStateHandler()

class CarDriver (Driver):
    # We don't need to call the init function because the Driver class already does that for us!

    # Instead I only want to overload this step function. This is what controls the movement of the sprite
    def step(self, dt):
        # This line might seem pretty complicated, but it's really not at all
        #self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 100 * dt
        # Essentially what I do here is take the right value minus the left value (remember that moving left is negative)
        # And then I multiply it by 100 so it's more visible, and multiply it by the dt value passed in by the step function
        # Finally, I add it to the rotation of the "target", which would be the sprite we tell to do this action

        # Now I'm going to do something very similar for the sprite's acceleration
        #self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 350
        # See if you can figure this out yourself!

        # Next I'm going to make the car stop completely if the space key is held
        # if keyboard[key.SPACE]:
        #     self.target.speed = 0
        #     # Pretty easy, huh?

        move_left = MoveBy((-10, 0), .02)
        move_up = MoveBy((0,10), 0.02)
        move_leftup = MoveBy((-10,10), 0.04)
        move_leftdown = MoveBy((-10,-10), 0.04)

        # Here's where that Pyglet symbol_string() function comes in handy
        # Rather than having to interpret an inconsistent code, I can simply interpret the word LEFT and RIGHT
        if keyboard[key.A]:
            self.target.do(move_left)

        # Now I need to tell the layer what to do if the user inputs RIGHT
        if keyboard[key.D]:
            self.target.do(Reverse(move_left))

        if keyboard[key.W]:
            self.target.do(move_up)

        if keyboard[key.S]:
            self.target.do(Reverse(move_up))
        # That's basically it!
        # Now we just need to call the original step function to let it do its magic

        super(CarDriver, self).step(dt)
        # Lastly, this line simply tells the ScrollingManager to set the center of the screen on the sprite

class Player(ScrollableLayer):
    def __init__(self):
        super(Player, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite('elephant.png')
        # We set the position (standard stuff)
        self.sprite.position = 400, 100
        # Oh no! Something new!
        # We set a maximum forward and backward speed for the car so that it doesn't fly off the map in an instant
        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -100
        # Then we add it
        self.add(self.sprite)
        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        self.sprite.do(CarDriver())

#scene 1
class Beach_scene(Layer):
    is_event_handler = True
    def __init__(self):
        # always call super()
        super(Beach_scene, self).__init__()

            # load the image form file
        self.sprite = Sprite('beach.png')
        self.sprite.position = 639, 359
        self.add(self.sprite)
        self.add(Player())

    #move from beach to jungle
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="RIGHT":
            director.replace(Scene(Jungle_scene()))

#scene 2
class Jungle_scene(Layer):
    is_event_handler = True
    def __init__(self):
        # always call super()
        super(Jungle_scene, self).__init__()

            # load the image form file
        self.sprite = Sprite('jungle.png')
        self.sprite.position = 639, 359
        self.add(self.sprite)
        self.add(obj_1()) #adds tree branch
        self.add(Player())

    #moves from jungle to tree top
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="LEFT":
            director.replace(Scene(Beach_scene()))
        if symbol_string(key)=="RIGHT":
            director.replace(Scene(Treetop_scene()))

#scene 3
class Treetop_scene(Layer):
    is_event_handler = True
    def __init__(self):
        # always call super()
        super(Treetop_scene, self).__init__()

            # load the image form file
        self.sprite = Sprite('tree_top.png')
        self.sprite.position = 639, 359
        self.add(self.sprite)


    #moves from tree top to jungle
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="LEFT":
            director.replace(Scene(Jungle_scene()))

#tree branch object
class obj_1(Layer):
    def __init__(self):
        # always call super()
        super(obj_1, self).__init__()
        self.sprite = Sprite('tree_branch.png')
        self.sprite.position = 700,100
        self.add(self.sprite)

#if __name__ == "__main__":
    # initialize the director,
    # enabling to resize the main window

director.init(width=1280, height=720)

director.window.push_handlers(keyboard)
    # enable opengl depth test
    # since we are using z-values
#director.set_depth_test()
screens = Scene(Beach_scene())

    # Run!
director.run(screens)

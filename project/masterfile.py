from __future__ import division, print_function, unicode_literals
import six
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import cocos
import pyglet
from cocos.cocosnode import *
from pyglet.gl import *
from pyglet.window import key
from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
# import cocos.actions.move_actions.Action
import random
from cocos.text import Label, HTMLLabel
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.director import director
from cocos.actions import Driver
from pyglet.window import key
from cocos.audio.pygame import mixer
from cocos.audio.pygame.mixer import Sound
from cocos.menu import Menu, CENTER, TOP, LEFT, RIGHT, BOTTOM, MenuItem, shake, shake_back, MultipleMenuItem
from pyglet.app import exit
from cocos.layer import Layer, ColorLayer, ScrollingManager, ScrollableLayer, MultiplexLayer
from cocos.text import Label
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.scenes.pause import PauseLayer, PauseScene
from cocos.actions import *


from pyglet.window.key import symbol_string

keyboard = key.KeyStateHandler()

class Audio(Sound):
    def __init__(self, audio_file):
        super(Audio, self).__init__(audio_file)
# We make a class that extends Cocos's Menu class
class StartMenu(Menu):
    def __init__(self):
        # When we initialize the super class, we can to pass in a title for our awesome menu, that will be displayed above it
        super(StartMenu, self).__init__("Welcome to Island Escape")
        # if you want to add your own, personalized text, feel free to pass nothing in
        # Then we simply set the vertical and horizontal alignment (in this case center for both)
        self.image = pyglet.resource.image('jungleboi.png')
        self.menu_valign = CENTER
        self.menu_haligh = CENTER
        pyglet.font.add_directory('.')

        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 60
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'
        # The cocos.menu file comes with many more different positions you can mix and match to get what you like
        # Next we need to make our menu items
        # This is the important part!
        # What we do is create a list filled with MenuItem objects
        menu_items = [
            # Each MenuItem has text to display, and a callback method
            # The callback method we pass in gets called when a user clicks on the MenuItem
            (MenuItem("Start Game", self.control_menu)),
            (MenuItem("Options", self.open_menu)),
            (MenuItem("Press ESC to Quit", self.on_quit))
            # (MenuItem("Increase Volume", self.volume_up)),
            # (MenuItem("Decrease Volume", self.volume_down)),
            # Pretty easy I'd say
        ]
        #self.song = Audio("sad.ogg")
        # Then we simply create the menu using the create_menu method and passing in our MenuItem list
        self.create_menu(menu_items)
        # And I set the is_playing status to False, which we will access for our Play/Pause functionality
        #self.is_playing = False
    # def start_game(self):
    #     director.replace(FadeTransition(Scene(Beach_scene(), InGameMenu())))

    def open_menu(self):
        director.replace(Scene(Options()))

    def control_menu(self):
        director.replace(FadeTransition(Scene(ControlBoi())))
    # IMPORTANT!
    # All your menus must have this on_quit function or they will not exit even if you press escape
    # (That means some fun Control+Alt+Tabing for you Windows users)
    def on_quit(self):
        # It seems odd that I need a function that literally just calls the exit function but...
        exit()

class VolumeItem(MultipleMenuItem):
    def __init__(self, label, callback_func, items, default_item):
        self.my_label = label
        self.items = items
        self.idx = default_item
        if self.idx<0 or self.idx>= len(self.items):
            raise Exception("Index out of bounds")
        super(MultipleMenuItem, self).__init__(self._get_label(), callback_func)

        self.song = Audio("sad.ogg")
        self.song.set_volume(0.5)
        self.song.play(-1)

    def on_key_press(self, symbol, modifiers):
        volume = self.song.get_volume()
        if symbol_string(symbol) == "LEFT" and volume>0.0:
            volume = round(volume - 0.1, 1)
        if symbol_string(symbol) == "RIGHT" and volume<1.0:
            volume = round(volume + 0.1, 1)
        self.song.set_volume(volume)

        if symbol == key.LEFT:
            self.idx = max(0, self.idx-1)
        elif symbol == key.RIGHT:
            self.idx = min(len(self.items)-1, self.idx+1)

        if symbol in (key.LEFT, key.RIGHT, key.ENTER):
            self.item.text = self._get_label()
            self.item_selected.text = self._get_label()
            self.callback_func(self.idx)
            return True

class VolumeMenu(Menu):
    def __init__(self):
        super(VolumeMenu, self).__init__("Volume Menu")

        self.menu_valign = CENTER
        self.menu_haligh = CENTER
        pyglet.font.add_directory('.')

        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 72
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'
        #
        # text = Label(
        #     "warningyo: These can only be chosen before the game starts. Otherwise, you will have to quit the game and restart.",
        #     font_name='Orbitron',
        #     font_size=30,
        #     anchor_x='center', anchor_y='center')
        # text.position = director._window_virtual_width / 2, director._window_virtual_height / 2
        # self.add(text)
        self.volumes = ['Mute', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']


        menu_items = [
            # (MenuItem("Music Toggle", self.play_music)),
            # (MenuItem("Increase Volume", self.volume_up)),
            # (MenuItem("Decrease Volume", self.volume_down)),
            (VolumeItem("Volume: ", self.none, self.volumes, 5)),
            (MenuItem("Save Changes and Start", self.start_game))
        ]
        self.create_menu(menu_items)
        #self.is_playing = False

    def none(self, key):
        pass

    def start_game(self):
        director.replace(FadeTransition(Scene(Beach_scene(), InGameMenu())))

    def open_menu(self):
        director.replace(Scene(PopUpMenu()))

    def start_menu(self):
        director.replace(Scene(StartMenu()))

class InGameMenu(Menu):
    def __init__(self):
        super(InGameMenu, self).__init__(" ")
        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT
        pyglet.font.add_directory('.')
        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 72
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'
        self.create_menu([(MenuItem("Pause", self.open_menu))])

    def open_menu(self):
        director.replace(Scene(Beach_scene(), Jungle_scene(), Treetop_scene()))
        director.replace(Scene(PopUpMenu()))

class ControlBoi(Layer):
    is_event_handler = True
    def __init__(self):
        super(ControlBoi, self).__init__()

        pyglet.font.add_file('Orbitron-Regular.ttf')
        orbitron_reg = pyglet.font.load('Orbitron Regular')

        label = Label(
                'Controls',
                font_name= 'Orbitron',
                font_size = 62,
                anchor_x = 'center', anchor_y = "center")
        label.position = 640, 650
        self.add(label)

        developers = Label("You are stuck on a deserted island\n You need to escape!\nUse WASD controls to move\nUse left and right arrows to switch  between areas\nPress Z to interact with items\nPress ENTER while in-game to pause the game\n(Press ENTER to begin)",
                    font_name = "Orbitron",
                    font_size = 28,
                    anchor_x = 'center', anchor_y = 'center',
                    width = 800,
                    #halign = 'center',
                    multiline = True)
        developers.position = 640, 300
        self.add(developers)


    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            director.replace(FadeTransition(Scene(VolumeMenu())))

class ControlBois(Layer):
    is_event_handler = True
    def __init__(self):
        super(ControlBois, self).__init__()

        pyglet.font.add_file('Orbitron-Regular.ttf')
        orbitron_reg = pyglet.font.load('Orbitron Regular')

        label = Label(
                'Controls',
                font_name= 'Orbitron',
                font_size = 62,
                anchor_x = 'center', anchor_y = "center")
        label.position = 640, 650
        self.add(label)

        developers = Label("You are stuck on a deserted island\nYou need to escape!\nUse WASD controls to move\nUse left and right arrows to switch  between areas\nPress Z to interact with items\nPress ENTER while in-game to pause the game\n(Press ENTER to begin)",
                    font_name = "Orbitron",
                    font_size = 28,
                    anchor_x = 'center', anchor_y = 'center',
                    width = 800,
                    #halign = 'center',
                    multiline = True)
        developers.position = 640, 300
        self.add(developers)


    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "ENTER":
            director.replace(FadeTransition(Scene(Beach_scene(), InGameMenu())))
#
# CONTROL = u"""
# <center>
# <font color="white" face="Arial">You found a stick</font>
# <br><font color="white" face="Arial">You tried using it as a weapon</font>
# <br>
# <color="white" face="Arial"><b>Controls</b></font>
# <br><font color="white" face="Arial">But accidentally hit yourself in the face
# <p>
# <font color="white" face="Arial"><b>(Press ENTER to continue)</b></font><br>
# </p>
# </center>
# """

# class Controlz(Menu):
#     def __init__(self):
#         super(Controlz, self).__init__()
#         self.menu_valign = CENTER
#         self.menu_haligh = CENTER
#         pyglet.font.add_directory('.')
#
#         self.font_item['font_name'] = 'Orbitron'
#         self.font_item['font_size'] = 20
#         self.font_title['font_size'] = 72
#         self.font_title['font_name'] = 'Orbitron'
#         self.font_item_selected['font_name'] = 'Orbitron'
#
#         menu_items = [
#             (MenuItem("You are stuck on a desserted island", self.no_thing)),
#             (MenuItem("Escape!", self.no_thing)),
#             # (MenuItem("You are stuck on a desserted island. Escape!", self.no_thing)),
#             (MenuItem("Press Z while near objects to use them", self.no_thing)),
#             (MenuItem("Use WASD to move", self.no_thing)),
#             (MenuItem("Use left and right arrows", self.no_thing)),
#             (MenuItem("to switch between areas", self.no_thing)),
#             (MenuItem("Press ENTER to pause game", self.no_thing)),
#             # (MenuItem("Volume Controls", self.volume_menu)),
#             (MenuItem("Continue", self.volume_menu))
#         ]
#         self.create_menu(menu_items)
#
#     def no_thing(self):
#         pass
#
#     def volume_menu(self):
#         director.replace(FadeTransition(Scene(Beach_scene(), InGameMenu())))


class Controls(Menu):
    def __init__(self):
        super(Controls, self).__init__("Controls")
        self.menu_valign = CENTER
        self.menu_haligh = CENTER
        pyglet.font.add_directory('.')

        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 72
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        menu_items = [
            (MenuItem("Use WASD to move", self.no_thing)),
            (MenuItem("Press ENTER to pause game", self.no_thing)),
            # (MenuItem("Volume Controls", self.volume_menu)),
            (MenuItem("Press ESC to exit", self.no_thing)),
            (MenuItem("Return to game", self.close_menu))
        ]
        self.create_menu(menu_items)

    def no_thing(self):
        pass
    def close_menu(self):
        director.replace(Scene(Beach_scene(),InGameMenu()))

class PopUpMenu(Menu):
    def __init__(self):
        super(PopUpMenu, self).__init__("Game Paused")
        self.menu_valign = CENTER
        self.menu_haligh = CENTER
        pyglet.font.add_directory('.')

        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 72
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        menu_items = [
            (MenuItem("Resume Game", self.close_menu)),
            (MenuItem("Controls", self.control_game)),
            (MenuItem('Show FPS', self.on_show_fps, True)),
            # (MenuItem("Volume Controls", self.volume_menu)),
            (MenuItem("Fullscreen", self.on_fullscreen)),
            (MenuItem("GWC Website", self.volume_menu)),
            (MenuItem("Press ESC to exit", self.on_quit))
        ]

        self.create_menu(menu_items)

    def on_show_fps(self, value):
        director.show_FPS = value

    def on_fullscreen(self):
        director.window.set_fullscreen(not director.window.fullscreen)

    def close_menu(self):
        director.replace(Scene(Beach_scene(), InGameMenu()))

    def volume_menu(self):
        director.replace(Scene(VolumeMenu()))

    def control_game(self):
        director.replace(Scene(Controls()))

    def on_quit(self):
        exit()

class Options(Menu):
    def __init__(self):
        super(Options, self).__init__("Options")
        self.menu_valign = CENTER
        self.menu_haligh = CENTER
        pyglet.font.add_directory('.')

        self.font_item['font_name'] = 'Orbitron'
        self.font_item['font_size'] = 45
        self.font_title['font_size'] = 72
        self.font_title['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        menu_items = [
            # (MenuItem("Resume Game", self.close_menu)),
            (MenuItem("Return to Title", self.close_menu)),
            (MenuItem("Controls", self.control_game)),
            (MenuItem('Show FPS', self.on_show_fps, True)),
            (MenuItem("Volume Controls", self.volume_menu)),
            (MenuItem("Fullscreen", self.on_fullscreen)),
            (MenuItem("GWC Website", self.volume_menu))
            # (MenuItem("Press ESC to exit", self.on_quit))
        ]

        self.create_menu(menu_items)

    def on_show_fps(self, value):
        director.show_FPS = value
        show_FPS.font_title['font_name'] = 'Orbitron'
        show_FPS.font_item['font_name'] = 'Orbitron'
        show_FPS.font_item['font_size'] = 45
        show_FPS.font_title['font_size'] = 72
        show_FPS.font_title['font_name'] = 'Orbitron'
        show_FPS.font_item_selected['font_name'] = 'Orbitron'

    def on_fullscreen(self):
        director.window.set_fullscreen(not director.window.fullscreen)

    def close_menu(self):
        director.replace(Scene(StartMenu()))

    def volume_menu(self):
        director.replace(Scene(VolumeMenu()))

    def control_game(self):
        director.replace(Scene(Controls()))

    def on_quit(self):
        exit()
#Spaghetti incoming

class MainMenu(Menu):
    is_event_handler = True
    def __init__(self):

        super(MainMenu, self).__init__("Awww At Least You Tried GAME OVER...")

        pyglet.font.add_directory('.')

        self.font_title['font_name'] = 'Orbitron'
        self.font_title['font_size'] = 40
        self.font_item['font_size'] = 20
        self.font_item['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []
        items.append(MenuItem('Elephants can\'t use flare guns!', self.no_thing))
        items.append(MenuItem('You tried to eat it', self.no_thing))
        items.append(MenuItem('But choked to death!', self.no_thing))
        items.append(MenuItem('Try Again', self.re_start))
        items.append(MenuItem('Exit Game', self.on_quit))

        self.create_menu(items, zoom_in(), zoom_out())

        self.song = Audio("dundun.ogg")
        self.song.play(0)

    def no_thing(self):
        pass
    def on_quit(self):
        director.pop()

    def re_start(self):
        director.replace(Scene(ControlBois()))

class Ending2(Menu):
    is_event_handler = True
    def __init__(self):

        super(Ending2, self).__init__("YOU WON!")

        pyglet.font.add_directory('.')

        self.font_title['font_name'] = 'Orbitron'
        self.font_title['font_size'] = 35
        self.font_item['font_size'] = 5
        self.font_item['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'
        self.font_item_selected['font_size'] = 35

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []
        items.append(MenuItem('You used the axe to chop down trees', self.no_thing))
        items.append(MenuItem('Then you built a statue', self.no_thing))
        items.append(MenuItem('Nice people came', self.no_thing))
        items.append(MenuItem('They took you home!', self.no_thing))
        items.append(MenuItem('Play Again', self.re_start))
        items.append(MenuItem('Exit Game', self.on_quit))

        self.create_menu(items, zoom_in(), zoom_out())

        self.song = Audio("trumpet.ogg")
        self.song.play(0)

    def no_thing(self):
        pass

    def on_quit(self):
        director.pop()

    def re_start(self):
        director.replace(Scene(ControlBois()))

class Ending3(Menu):
    is_event_handler = True
    def __init__(self):

        super(Ending3, self).__init__("Awww At Least You Tried GAME OVER...")

        pyglet.font.add_directory('.')

        self.font_title['font_name'] = 'Orbitron'
        self.font_title['font_size'] = 45
        self.font_item['font_size'] = 20
        self.font_item['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []
        items.append(MenuItem('You found a stick', self.no_thing))
        items.append(MenuItem('But it didn\'t help at all', self.no_thing))
        items.append(MenuItem('Play Again', self.re_start))
        items.append(MenuItem('Exit Game', self.on_quit))

        self.create_menu(items, zoom_in(), zoom_out())

        self.song = Audio("dundun.ogg")
        self.song.play(0)

    def no_thing(self):
        pass

    def on_quit(self):
        director.pop()

    def re_start(self):
        director.replace(Scene(ControlBois()))


rr = random.randrange


class Fire:

    def __init__(self, x, y, vy, frame, size):
        self.x, self.y, self.vy, self.frame, self.size = x, y, vy, frame, size


class FireManager(Layer):

    def __init__(self, view_width, num):
        super(FireManager, self).__init__()

        self.view_width = view_width
        self.goodies = []
        self.batch = pyglet.graphics.Batch()
        self.fimg = pyglet.resource.image('fire.jpg')
        self.group = pyglet.sprite.SpriteGroup(self.fimg.texture,
                                               blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE)
        self.vertex_list = self.batch.add(4 * num, GL_QUADS, self.group,
                                          'v2i', 'c4B', ('t3f', self.fimg.texture.tex_coords * num))
        for n in range(0, num):
            f = Fire(0, 0, 0, 0, 0)
            self.goodies.append(f)
            self.vertex_list.vertices[n * 8:(n + 1) * 8] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.vertex_list.colors[n * 16:(n + 1) * 16] = [0, 0, 0, 0, ] * 4

        self.schedule(self.step)

    def step(self, dt):
        w, h = self.fimg.width, self.fimg.height
        fires = self.goodies
        verts, clrs = self.vertex_list.vertices, self.vertex_list.colors
        for n, f in enumerate(fires):
            if not f.frame:
                f.x = rr(0, self.view_width)
                f.y = rr(-120, -80)
                f.vy = rr(40, 70) / 100.0
                f.frame = rr(50, 250)
                f.size = 8 + pow(rr(0.0, 100) / 100.0, 2.0) * 32
                f.scale = f.size / 32.0

            x = f.x = f.x + rr(-50, 50) / 100.0
            y = f.y = f.y + f.vy * 4
            c = 3 * f.frame / 255.0
            r, g, b = (min(255, int(c * 0xc2)), min(255, int(c * 0x41)), min(255, int(c * 0x21)))
            f.frame -= 1
            ww, hh = w * f.scale, h * f.scale
            x -= ww / 2
            if six.PY2:
                vs = map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh])
            else:
                vs = list(map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh]))
            verts[n * 8:(n + 1) * 8] = vs
            clrs[n * 16:(n + 1) * 16] = [r, g, b, 255] * 4

    def draw(self):
        glPushMatrix()
        self.transform()

        self.batch.draw()

        glPopMatrix()

class Color(ColorLayer):
    def __init__(self):
        super(Color, self).__init__(195 , 223, 248, 1000)

class GoodManager(Layer):

    def __init__(self, view_width, num):
        super(GoodManager, self).__init__()

        self.view_width = view_width
        self.goodies = []
        self.batch = pyglet.graphics.Batch()
        self.fimg = pyglet.resource.image('elephant.png')
        self.group = pyglet.sprite.SpriteGroup(self.fimg.texture,
                                               blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE)
        self.vertex_list = self.batch.add(4 * num, GL_QUADS, self.group,
                                          'v2i', 'c4B', ('t3f', self.fimg.texture.tex_coords * num))
        for n in range(0, num):
            f = Fire(0, 0, 0, 0, 0)
            self.goodies.append(f)
            self.vertex_list.vertices[n * 8:(n + 1) * 8] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.vertex_list.colors[n * 16:(n + 1) * 16] = [0, 0, 0, 0, ] * 4

        self.schedule(self.step)

    def step(self, dt):
        w, h = self.fimg.width, self.fimg.height
        fires = self.goodies
        verts, clrs = self.vertex_list.vertices, self.vertex_list.colors
        for n, f in enumerate(fires):
            if not f.frame:
                f.x = rr(0, self.view_width)
                f.y = rr(-120, -80)
                f.vy = rr(40, 70) / 100.0
                f.frame = rr(50, 250)
                f.size = 8 + pow(rr(0.0, 100) / 100.0, 2.0) * 32
                f.scale = f.size / 32.0

            x = f.x = f.x + rr(-50, 50) / 100.0
            y = f.y = f.y + f.vy * 4
            c = 3 * f.frame / 255.0
            r, g, b = (min(255, int(c * 0xc2)), min(255, int(c * 0x41)), min(255, int(c * 0x21)))
            f.frame -= 1
            ww, hh = w * f.scale, h * f.scale
            x -= ww / 2
            if six.PY2:
                vs = map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh])
            else:
                vs = list(map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh]))
            verts[n * 8:(n + 1) * 8] = vs
            clrs[n * 16:(n + 1) * 16] = [r, g, b, 255] * 4

    def draw(self):
        glPushMatrix()
        self.transform()

        self.batch.draw()

        glPopMatrix()

class SpriteLayer(Layer):

    def __init__(self):
        super(SpriteLayer, self).__init__()

        sprite0 = Sprite('eleph2.png')
        sprite1 = Sprite('eleph1.png')
        sprite2 = Sprite('eleph0.png')

        sprite0.position = (600, 360)
        sprite1.position = (1180, 100)
        sprite2.position = (20, 100)

        sprite0.scale = .5
        sprite1.scale = .5
        sprite2.scale = .5

        self.add(sprite0)
        self.add(sprite1)
        self.add(sprite2)

        ju_right = JumpBy((600, 0), height=100, jumps=8, duration=5)
        ju_left = JumpBy((-600, 0), height=100, jumps=8, duration=5)
        rot1 = Rotate(180 * 4, duration=5)

        sprite0.opacity = 200

        sc = ScaleBy(9, 5)
        rot = Rotate(180, 5)

        sprite0.do(Repeat(sc + Reverse(sc)))
        sprite0.do(Repeat(rot + Reverse(rot)))
        sprite1.do(Repeat(ju_left + ju_left + Reverse(ju_left) + Reverse(ju_left)))
        sprite1.do(Repeat(Reverse(rot1) + Reverse(rot1) + rot1 + rot1))
        sprite2.do(Repeat(ju_right + ju_right + Reverse(ju_right) + Reverse(ju_right)))
        sprite2.do(Repeat(rot1 + rot1 + Reverse(rot1) + Reverse(rot1)))

class SpriteBoi(Layer):

    def __init__(self):
        super(SpriteBoi, self).__init__()

        sprite0 = Sprite('statue.png')
        sprite1 = Sprite('eleph1.png')
        sprite2 = Sprite('eleph0.png')

        sprite0.position = (620, 360)
        sprite1.position = (1180, 100)
        sprite2.position = (20, 100)

        sprite0.scale = 1
        sprite1.scale = .5
        sprite2.scale = .5

        self.add(sprite0)
        self.add(sprite1)
        self.add(sprite2)

        ju_right = JumpBy((600, 0), height=100, jumps=8, duration=5)
        ju_left = JumpBy((-600, 0), height=100, jumps=8, duration=5)
        rot1 = Rotate(180 * 4, duration=5)

        sprite0.opacity = 128

        sc = ScaleBy(9, 5)
        rot = Rotate(180, 5)

        # sprite0.do(Repeat(sc + Reverse(sc)))
        # sprite0.do(Repeat(rot + Reverse(rot)))
        sprite1.do(Repeat(ju_left + ju_left + Reverse(ju_left) + Reverse(ju_left)))
        sprite1.do(Repeat(Reverse(rot1) + Reverse(rot1) + rot1 + rot1))
        sprite2.do(Repeat(ju_right + ju_right + Reverse(ju_right) + Reverse(ju_right)))
        sprite2.do(Repeat(rot1 + rot1 + Reverse(rot1) + Reverse(rot1)))

def init():
    director.init(resizable=True, width=1280, height=720)

def start1():
    director.set_depth_test()

    firelayer = FireManager(director.get_window_size()[0], 250)
    spritelayer = SpriteLayer()
    menulayer = MultiplexLayer(MainMenu())

    scene = Scene(firelayer, spritelayer, menulayer)

    twirl_normal = Twirl(center=(320, 240), grid=(16, 12), duration=15, twirls=6, amplitude=6)
    twirl = AccelDeccelAmplitude(twirl_normal, rate=4.0)
    lens = Lens3D(radius=240, center=(320, 240), grid=(32, 24), duration=5)
    waves3d = AccelDeccelAmplitude(
        Waves3D(waves=18, amplitude=80, grid=(32, 24), duration=15), rate=4.0)
    flipx = FlipX3D(duration=1)
    flipy = FlipY3D(duration=1)
    #flip = Hide(duration=1)
    liquid = Liquid(grid=(16, 12), duration=4)
    ripple = Ripple3D(grid=(32, 24), waves=7, duration=10, amplitude=100, radius=320)
    shakyt = ShakyTiles3D(grid=(16, 12), duration=3)
    corners = CornerSwap(duration=1)
    waves = AccelAmplitude(Waves(waves=8, amplitude=50, grid=(32, 24), duration=5), rate=2.0)
    shaky = Shaky3D(randrange=10, grid=(32, 24), duration=5)
    quadmove = QuadMoveBy(
        delta0=(320, 240), delta1=(-630, 0), delta2=(-320, -240), delta3=(630, 0), duration=2)
    fadeout = FadeOutTRTiles(grid=(16, 12), duration=2)
    cornerup = MoveCornerUp(duration=1)
    cornerdown = MoveCornerDown(duration=1)
    shatter = ShatteredTiles3D(randrange=16, grid=(16, 12), duration=4)
    shuffle = ShuffleTiles(grid=(16, 12), duration=1)
    orbit = OrbitCamera(
        radius=1, delta_radius=2, angle_x=0, delta_x=-90, angle_z=0, delta_z=180, duration=4)
    jumptiles = JumpTiles3D(jumps=2, duration=4, amplitude=80, grid=(16, 12))
    wavestiles = WavesTiles3D(waves=3, amplitude=60, duration=8, grid=(16, 12))
    turnoff = TurnOffTiles(grid=(16, 12), duration=2)

    scene.do(
        Delay(5) +
        ripple + Delay(2) +
        wavestiles + Delay(1) +
        twirl +
        liquid + Delay(2) +
        shakyt + Delay(2) +
        ReuseGrid() +
        shuffle + Delay(4) + ReuseGrid() + turnoff + Reverse(turnoff) + Delay(1) +
        shatter +
        #flip + Delay(2) +
        #Reverse(flip) +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) + ReuseGrid() +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) +
        lens + ReuseGrid() + ((orbit + Reverse(orbit)) | waves3d) + Delay(1) +
        corners + Delay(2) + Reverse(corners) +
        waves + Delay(2) + ReuseGrid() + shaky +
        jumptiles + Delay(1) +
        cornerup + Delay(1) +
        Reverse(cornerdown) + Delay(1) +
        fadeout + Reverse(fadeout) + Delay(2) +
        quadmove + Delay(1) +
        Reverse(quadmove) +
        StopGrid()
    )

    scene.do(Delay(10) + OrbitCamera(delta_z=-360 * 3, duration=10 * 4))

    firelayer.do(Delay(4) + Repeat(RotateBy(360, 10)))

    return scene

def win():
    director.set_depth_test()

    firelayer = GoodManager(director.get_window_size()[0], 250)
    spritelayer = SpriteBoi()
    menulayer = MultiplexLayer(Ending2())

    scene = Scene(Color(), firelayer, spritelayer, menulayer)

    twirl_normal = Twirl(center=(320, 240), grid=(16, 12), duration=15, twirls=6, amplitude=6)
    twirl = AccelDeccelAmplitude(twirl_normal, rate=4.0)
    lens = Lens3D(radius=240, center=(320, 240), grid=(32, 24), duration=5)
    waves3d = AccelDeccelAmplitude(
        Waves3D(waves=18, amplitude=80, grid=(32, 24), duration=15), rate=4.0)
    flipx = FlipX3D(duration=1)
    flipy = FlipY3D(duration=1)
    #flip = Hide(duration=1)
    liquid = Liquid(grid=(16, 12), duration=4)
    ripple = Ripple3D(grid=(32, 24), waves=7, duration=10, amplitude=100, radius=320)
    shakyt = ShakyTiles3D(grid=(16, 12), duration=3)
    corners = CornerSwap(duration=1)
    waves = AccelAmplitude(Waves(waves=8, amplitude=50, grid=(32, 24), duration=5), rate=2.0)
    shaky = Shaky3D(randrange=10, grid=(32, 24), duration=5)
    quadmove = QuadMoveBy(
        delta0=(320, 240), delta1=(-630, 0), delta2=(-320, -240), delta3=(630, 0), duration=2)
    fadeout = FadeOutTRTiles(grid=(16, 12), duration=2)
    cornerup = MoveCornerUp(duration=1)
    cornerdown = MoveCornerDown(duration=1)
    shatter = ShatteredTiles3D(randrange=16, grid=(16, 12), duration=4)
    shuffle = ShuffleTiles(grid=(16, 12), duration=1)
    orbit = OrbitCamera(
        radius=1, delta_radius=2, angle_x=0, delta_x=-90, angle_z=0, delta_z=180, duration=4)
    jumptiles = JumpTiles3D(jumps=2, duration=4, amplitude=80, grid=(16, 12))
    wavestiles = WavesTiles3D(waves=3, amplitude=60, duration=8, grid=(16, 12))
    turnoff = TurnOffTiles(grid=(16, 12), duration=2)

    scene.do(
        Delay(5) +
        ripple + Delay(2) +
        wavestiles + Delay(1) +
        twirl +
        liquid + Delay(2) +
        shakyt + Delay(2) +
        ReuseGrid() +
        shuffle + Delay(4) + ReuseGrid() + turnoff + Reverse(turnoff) + Delay(1) +
        shatter +
        #flip + Delay(2) +
        #Reverse(flip) +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) + ReuseGrid() +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) +
        lens + ReuseGrid() + ((orbit + Reverse(orbit)) | waves3d) + Delay(1) +
        corners + Delay(2) + Reverse(corners) +
        waves + Delay(2) + ReuseGrid() + shaky +
        jumptiles + Delay(1) +
        cornerup + Delay(1) +
        Reverse(cornerdown) + Delay(1) +
        fadeout + Reverse(fadeout) + Delay(2) +
        quadmove + Delay(1) +
        Reverse(quadmove) +
        StopGrid()
    )

    scene.do(Delay(10) + OrbitCamera(delta_z=-360 * 3, duration=10 * 4))

    firelayer.do(Delay(4) + Repeat(RotateBy(360, 10)))

    return scene

def start2():
    director.set_depth_test()

    firelayer = FireManager(director.get_window_size()[0], 250)
    spritelayer = SpriteLayer()
    menulayer = MultiplexLayer(Ending3())

    scene = Scene(firelayer, spritelayer, menulayer)

    twirl_normal = Twirl(center=(320, 240), grid=(16, 12), duration=15, twirls=6, amplitude=6)
    twirl = AccelDeccelAmplitude(twirl_normal, rate=4.0)
    lens = Lens3D(radius=240, center=(320, 240), grid=(32, 24), duration=5)
    waves3d = AccelDeccelAmplitude(
        Waves3D(waves=18, amplitude=80, grid=(32, 24), duration=15), rate=4.0)
    flipx = FlipX3D(duration=1)
    flipy = FlipY3D(duration=1)
    #flip = Hide(duration=1)
    liquid = Liquid(grid=(16, 12), duration=4)
    ripple = Ripple3D(grid=(32, 24), waves=7, duration=10, amplitude=100, radius=320)
    shakyt = ShakyTiles3D(grid=(16, 12), duration=3)
    corners = CornerSwap(duration=1)
    waves = AccelAmplitude(Waves(waves=8, amplitude=50, grid=(32, 24), duration=5), rate=2.0)
    shaky = Shaky3D(randrange=10, grid=(32, 24), duration=5)
    quadmove = QuadMoveBy(
        delta0=(320, 240), delta1=(-630, 0), delta2=(-320, -240), delta3=(630, 0), duration=2)
    fadeout = FadeOutTRTiles(grid=(16, 12), duration=2)
    cornerup = MoveCornerUp(duration=1)
    cornerdown = MoveCornerDown(duration=1)
    shatter = ShatteredTiles3D(randrange=16, grid=(16, 12), duration=4)
    shuffle = ShuffleTiles(grid=(16, 12), duration=1)
    orbit = OrbitCamera(
        radius=1, delta_radius=2, angle_x=0, delta_x=-90, angle_z=0, delta_z=180, duration=4)
    jumptiles = JumpTiles3D(jumps=2, duration=4, amplitude=80, grid=(16, 12))
    wavestiles = WavesTiles3D(waves=3, amplitude=60, duration=8, grid=(16, 12))
    turnoff = TurnOffTiles(grid=(16, 12), duration=2)

    scene.do(
        Delay(5) +
        ripple + Delay(2) +
        wavestiles + Delay(1) +
        twirl +
        liquid + Delay(2) +
        shakyt + Delay(2) +
        ReuseGrid() +
        shuffle + Delay(4) + ReuseGrid() + turnoff + Reverse(turnoff) + Delay(1) +
        shatter +
        #flip + Delay(2) +
        #Reverse(flip) +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) + ReuseGrid() +
        flipx + Delay(2) + ReuseGrid() +
        flipy + Delay(2) +
        lens + ReuseGrid() + ((orbit + Reverse(orbit)) | waves3d) + Delay(1) +
        corners + Delay(2) + Reverse(corners) +
        waves + Delay(2) + ReuseGrid() + shaky +
        jumptiles + Delay(1) +
        cornerup + Delay(1) +
        Reverse(cornerdown) + Delay(1) +
        fadeout + Reverse(fadeout) + Delay(2) +
        quadmove + Delay(1) +
        Reverse(quadmove) +
        StopGrid()
    )

    scene.do(Delay(10) + OrbitCamera(delta_z=-360 * 3, duration=10 * 4))

    firelayer.do(Delay(4) + Repeat(RotateBy(360, 10)))

    return scene

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
        x,y = self.target.position

        # print("X: " + str(x))
        # print("Y: " + str(y))

        move_left = MoveBy((-10, 0), .02)
        move_up = MoveBy((0,10), 0.02)
        move_leftup = MoveBy((-10,10), 0.04)
        move_leftdown = MoveBy((-10,-10), 0.04)

        # Here's where that Pyglet symbol_string() function comes in handy
        # Rather than having to interpret an inconsistent code, I can simply interpret the word LEFT and RIGHT
        if keyboard[key.A] and x>200:
            self.target.do(move_left)
            # self.sprite = Sprite('eleph0.png')
        # Now I need to tell the layer what to do if the user inputs RIGHT
        if keyboard[key.D] and x<1200:
            self.target.do(Reverse(move_left))

        if keyboard[key.W] and y<320:
            self.target.do(move_up)

        if keyboard[key.S] and y>166:
            self.target.do(Reverse(move_up))

        # if keyboard[key.Z]:
        #     self.target.do(Hide(obj_2))
        #
        # #if keyboard[key.Z]:
        #     print("hELLO")
        # Now we just need to call the original step function to let it do its magic
        super(CarDriver, self).step(dt)
        # Lastly, this line simply tells the ScrollingManager to set the center of the screen on the sprite

# class BoundedMove(Move):
#     def step(self, dt):
#         super(BounedMove, self).step(dt)
#         self.target.dr = (keys[key.RIGHT] - keys[key.LEFT]) * 360
#         rotation = math.pi * self.target.rotation / 180.0
#         rotation_x = math.cos(-rotation)
#         rotation_y = math.sin(-rotation)
#         if keys[key.UP]:
#            self.target.acceleration = (200 * rotation_x, 200 * rotation_y)

# ship.do(WrappedMove())

class Hide(InstantAction):
    def __init__(self):
        super(Hide, self).__init__()

    def start(self):
        self.target.visible = False

    def __reversed__(self):
        return Show()

class Player_left(ScrollableLayer):
    def __init__(self):
        super(Player_left, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite('eleph2.png')
        # We set the position (standard stuff)
        self.sprite.position = 300, 250
        self.sprite.scale = 1
        # We set a maximum forward and backward speed for the car so that it doesn't fly off the map in an instant
        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -200
        # Then we add it
        self.add(self.sprite)
        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        self.sprite.do(CarDriver())


class Player_right(ScrollableLayer):
    def __init__(self):
        super(Player_right, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite('eleph2.png')
        # We set the position (standard stuff)
        self.sprite.position = 900, 250
        self.sprite.scale = 1
        # We set a maximum forward and backward speed for the car so that it doesn't fly off the map in an instant
        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -200
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
        # sprite = cocos.sprite.Sprite('beach.png')
            # load the image form file
        self.sprite = Sprite('beach.png')
        self.sprite.position = 639, 359
        self.add(self.sprite)
        self.add(obj_3()) #adds flare gun
        self.add(Player_right())

    #move from beach to jungle
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="RIGHT":
            director.replace(Scene(Jungle_scene(), Player_left(), InGameMenu()))

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
        self.add(obj_2()) #adds tree branch

    #moves from jungle to tree top
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="LEFT":
            director.replace(Scene(Beach_scene(), InGameMenu()))
        if symbol_string(key)=="RIGHT":
            director.replace(Scene(Treetop_scene(), InGameMenu()))


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
        self.add(obj_1())

    #moves from tree top to jungle
    def on_key_press(self, key, modifiers):
        if symbol_string(key)=="LEFT":
            director.replace(Scene(Jungle_scene(), Player_right(), InGameMenu()))

#tree branch object
class obj_1(Layer):
    is_event_handler = True
    def __init__(self):
        # always call super()
        super(obj_1, self).__init__()
        self.sprite = Sprite('tree_branch.png')
        self.sprite.position = 700,100
        self.add(self.sprite)

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "Z":
            self.sprite.do(Hide())
            director.replace(start2())


class obj_2(Layer):
    is_event_handler = True
    def __init__(self):
        super(obj_2, self).__init__()
        sprite = cocos.sprite.Sprite('axe.png')
        self.sprite = Sprite('axe.png')
        self.sprite.scale = .5
        self.sprite.position = 700, 100
        self.add(self.sprite)


    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "Z":
            self.sprite.do(Hide())
            #time.sleep(1.5)
            director.replace(win())

class obj_3(Layer):
    is_event_handler = True
    def __init__(self):
        super(obj_3, self).__init__()
        sprite = cocos.sprite.Sprite('flaregun.png')
        self.sprite = Sprite('flaregun.png')
        self.sprite.scale = .5
        self.sprite.position = 900, 100
        self.add(self.sprite)

    def on_key_press(self, key, modifiers):
        if symbol_string(key) == "Z":
            self.sprite.do(Hide())
            director.replace(start1())

# Then we initialize the mixer (I bet you forgot about this!)
mixer.init()
# And initialize the director like usual
director.init(width = 1280, height = 720, resizable=True)
director.window.push_handlers(keyboard)
director.run(Scene(StartMenu())) #Run Scene

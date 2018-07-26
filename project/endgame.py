from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from pyglet.gl import *

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import Sprite

import random
from cocos.audio.pygame import mixer
from cocos.audio.pygame.mixer import Sound
from cocos.director import director
from cocos.menu import Menu, CENTER, TOP, LEFT, MenuItem, shake, shake_back
from cocos.scene import Scene
from pyglet.app import exit

from cocos.layer import ColorLayer
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.text import Label

# Here we will make a simple menu that allows you to play/pause a song, and to increase or decrease its volume
# As you'll see, Cocos makes writing menus EXTREMELY easy. Like I probably should have put this in beginner easy


# # To begin, we have to make a wrapper for the Sound class (remember this?)
class Audio(Sound):
    def __init__(self, audio_file):
        super(Audio, self).__init__(audio_file)

class MainMenu(Menu):

    def __init__(self):

        super(MainMenu, self).__init__("Awww At Least You Tried GAME OVER...")

        pyglet.font.add_directory('.')

        self.font_title['font_name'] = 'Orbitron'
        self.font_title['font_size'] = 40
        # self.font_item['font_size'] = 45
        self.font_item['font_name'] = 'Orbitron'
        self.font_item_selected['font_name'] = 'Orbitron'

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []

        items.append(MenuItem('Exit Game and Try Again', self.on_quit))

        self.create_menu(items, zoom_in(), zoom_out())

        self.song = Audio("dundun.ogg")
        self.song.play(0)

    def on_quit(self):
        director.pop()

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

        sprite0.opacity = 128

        sc = ScaleBy(9, 5)
        rot = Rotate(180, 5)

        sprite0.do(Repeat(sc + Reverse(sc)))
        sprite0.do(Repeat(rot + Reverse(rot)))
        sprite1.do(Repeat(ju_left + ju_left + Reverse(ju_left) + Reverse(ju_left)))
        sprite1.do(Repeat(Reverse(rot1) + Reverse(rot1) + rot1 + rot1))
        sprite2.do(Repeat(ju_right + ju_right + Reverse(ju_right) + Reverse(ju_right)))
        sprite2.do(Repeat(rot1 + rot1 + Reverse(rot1) + Reverse(rot1)))

def init():
    director.init(resizable=True, width=1280, height=720)

def start():
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
    flip = Hide(duration=1)
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
        Delay(3) +
        ripple + Delay(2) +
        wavestiles + Delay(1) +
        twirl +
        liquid + Delay(2) +
        shakyt + Delay(2) +
        ReuseGrid() +
        shuffle + Delay(4) + ReuseGrid() + turnoff + Reverse(turnoff) + Delay(1) +
        shatter +
        flip + Delay(2) +
        Reverse(flip) +
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

mixer.init()

def run(scene):
    director.run(scene)

if __name__ == "__main__":
    init()
    s = start()
    run(s)

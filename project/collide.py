import cocos
import pyglet
from cocos.sprite import Sprite
import cocos.euclid as eu
import cocos.collision_model as cm

class CollidableSprite(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y, radius):
        super(CollidableSprite, self).__init__(image)
        self.position = (center_x, center_y)
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), radius)

class ActorModel(object):
    def __init__(self, cx, cy, radius):
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), radius)

    def __init__(self):
        super(page,self).__init__()
        self.collision_manager = CollisionManager()
        self.collision_manager.add(self.sprite1)
        self.collision_manager.add(self.sprite2)
        print self.collision_manager.known_objs()

director.init()

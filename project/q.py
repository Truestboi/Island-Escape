import cocos
import cocos.euclid as eu
import cocos.collision_model as cm

class CollidableSprite(cocos.sprite.Sprite):
        def __init__(self, image, center_x, center_y, radius):
                super(ActorSprite, self).__init__(image)
                self.position = (center_x, center_y)
                self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), radius)

class ActorModel(object):
        def __init__(self, cx, cy, radius):
                self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), radius)

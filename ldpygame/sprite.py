import pygame
from event_responder import EventResponderManager
from sprite_events import *

class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, rect, groups, image=None, layer=0, dirty=1):
        super(Sprite, self).__init__()
        groups.add(self, layer=layer)

        self.rect = rect
        self.dirty = dirty

        if image:
            self.image = image
        else:
            self.image = pygame.Surface((self.rect.w, self.rect.h))
            self.image.fill(pygame.Color(255,255,255))

    def add_velocity(self, x, y):
        return False

class MobileSprite(Sprite):
    LEFT = "left"
    RIGHT = "right"
    DIRECTIONS = (LEFT,RIGHT)

    def __init__(self, rect, bounding_rect, groups, image=None, velocity=pygame.Rect(0,0,0,0), layer=0):
        super(MobileSprite, self).__init__(rect, groups, image, layer)
        self.bounding_rect = bounding_rect
        self.event_manager = EventResponderManager()
        self.velocity = velocity
        self.direction = MobileSprite.LEFT

    def add_event_responder(self, event_responder):
        self.event_manager.add_event_responder(event_responder)

    def update(self, *args):
        self.rect = self.rect.move(self.velocity.x, self.velocity.y)

        if self.velocity.x != 0 or self.velocity.y != 0:
            self.dirty = 1

        if self.rect.x > self.bounding_rect.right:
            self.event_manager.send_event(SpriteEvent('SpriteDidLeaveEventResponder-maxX', self))
        elif self.rect.x + self.rect.w < self.bounding_rect.left:
            self.event_manager.send_event(SpriteEvent('SpriteDidLeaveEventResponder-minX', self))
        elif self.rect.x+self.rect.w > self.bounding_rect.right:
            self.event_manager.send_event(SpriteEvent('SpriteWillLeaveEventResponder-maxX', self))
        elif self.rect.x < self.bounding_rect.left:
            self.event_manager.send_event(SpriteEvent('SpriteWillLeaveEventResponder-minX', self))

        if self.rect.y > self.bounding_rect.bottom:
            self.event_manager.send_event(SpriteEvent('SpriteDidLeaveEventResponder-maxY', self))
        elif self.rect.y + self.rect.h < self.bounding_rect.top:
            self.event_manager.send_event(SpriteEvent('SpriteDidLeaveEventResponder-minY', self))
        elif self.rect.y+self.rect.h > self.bounding_rect.bottom:
            self.event_manager.send_event(SpriteEvent('SpriteWillLeaveEventResponder-maxY', self))
        elif self.rect.y < self.bounding_rect.top:
            self.event_manager.send_event(SpriteEvent('SpriteWillLeaveEventResponder-minY', self))

    def add_velocity(self, x, y):
        self.velocity.x += x
        self.velocity.y += y
        self.update_direction()

        return self.direction

    def update_direction(self):
        if self.velocity.x < 0:
            self.direction = MobileSprite.LEFT
        elif self.velocity.x > 0:
            self.direction = MobileSprite.RIGHT

class BounceSprite(MobileSprite):
    def __init__(self, rect, bounding_rect, groups, image=None, velocity=pygame.Rect(0,0,0,0), layer=0):
        super(BounceSprite, self).__init__(rect, bounding_rect, groups, image, velocity, layer)
        self.add_event_responder(SpriteWillLeaveMinXEventResponder(self.bounce_min_x))
        self.add_event_responder(SpriteWillLeaveMaxXEventResponder(self.bounce_max_x))

        self.add_event_responder(SpriteWillLeaveMinYEventResponder(self.bounce_min_y))
        self.add_event_responder(SpriteWillLeaveMaxYEventResponder(self.bounce_max_y))

    def bounce_min_x(self, event):
        self.rect.x = self.bounding_rect.left
        self.velocity.x *= -1

    def bounce_max_x(self, event):
        self.rect.x = self.bounding_rect.right - self.rect.w
        self.velocity.x *= -1

    def bounce_min_y(self, event):
        self.rect.y = self.bounding_rect.top
        self.velocity.y *= -1

    def bounce_max_y(self, event):
        self.rect.y = self.bounding_rect.bottom - self.rect.h
        self.velocity.y *= -1

class AnimatedSprite(MobileSprite):
    def __init__(self, num_frames, frame_delay_ms, image, rect, bounding_rect, groups, velocity, layer):
        super(AnimatedSprite, self).__init__(rect, bounding_rect, groups, image, velocity, layer)

        self.num_frames = num_frames
        self.frame_delay_ms = frame_delay_ms
        self.frame_timer_ms = 0
        self.frame_num = 0
        self.frames = image

        self.set_frame(0)

    def set_frame(self, frame_num):
        self.dirty = 1
        self.frame_num = frame_num
        self.image = self.frames.subsurface(pygame.Rect(self.frame_num * self.rect.w, 0, self.rect.w, self.rect.h))

    def update(self, tick_time):
        super(AnimatedSprite, self).update(tick_time)
        self.update_frame(tick_time)

    def update_frame(self, tick_time):
        self.frame_timer_ms += tick_time

        if self.frame_timer_ms >= self.frame_delay_ms:
            self.frame_timer_ms = 0
            self.frame_num += 1

            if self.frame_num >= self.num_frames:
                self.frame_num = 0

            self.current_frame = self.set_frame(self.frame_num)

class SpriteManager(pygame.sprite.LayeredDirty):
    pass
    """
    Keeps track of sprites in a list. When the draw() function is called, all
    sprites are drawn to the screen and it returns a list of rectangles that have
    changed that should be passed to pygame.display.update()
    """

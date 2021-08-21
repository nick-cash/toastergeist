from ldpygame.sprite import Sprite
from ldpygame.game import Game
import pygame

class Button(Sprite):
    def __init__(self, rect, groups, inactive_image=None, active_image=None, down_image=None, up_image=None, active_rect=None, down_rect=None, up_rect=None, callback=None):
        super(Button, self).__init__(rect, groups, inactive_image)
        self.inactive_rect = rect.copy()
        self.callback = callback
        if active_rect:
            self.active_rect = active_rect
        else:
            self.active_rect = rect.copy()

        if down_rect:
            self.down_rect = down_rect
        else:
            self.down_rect = rect.copy()

        if up_rect:
            self.up_rect = up_rect
        else:
            self.up_rect = rect.copy()

        if inactive_image:
            self.image = inactive_image
            self.inactive_image = inactive_image
        else:
            self.inactive_image = pygame.Surface((self.inactive_rect.w, self.inactive_rect.h))
            self.inactive_image.fill(pygame.Color(255,255,255))
            self.image = self.inactive_image

        if active_image:
            self.active_image = active_image
        else:
            self.active_image = inactive_image

        if down_image:
            self.down_image = down_image
        else:
            self.down_image = inactive_image

        if up_image:
            self.up_image = up_image
        else:
            self.up_image = inactive_image

        self.state = 'inactive'

    def update(self,tick_time):
        self.dirty = 1
        #for now this will have to do.
        #the sprites are updated in an event handler.

    def set_state(self,state="inactive"):
        """
        Switches button state.
        """
        
        self.state = state
        temp_rect = self.rect.copy()
        if state=='up':
            self.image = self.up_image
            if(self.rect.width != self.up_rect.width or self.rect.height != self.up_rect.height):
                self.rect.w = self.up_rect.width
                self.rect.h = self.up_rect.height
                self.rect.center = temp_rect.center
        elif state=='active':
            self.image = self.active_image
            if(self.rect.width != self.active_rect.width or self.rect.height != self.active_rect.height):
                self.rect.w = self.active_rect.width
                self.rect.h = self.active_rect.height
                self.rect.center = temp_rect.center
        elif state=='down':
            self.image = self.down_image
            if(self.rect.width != self.down_rect.width or self.rect.height != self.down_rect.height):
                self.rect.w = self.down_rect.width
                self.rect.h = self.down_rect.height
                self.rect.center = temp_rect.center
        else:
            self.image = self.inactive_image
            self.state = 'inactive'
            if(self.rect.width != self.inactive_rect.width or self.rect.height != self.inactive_rect.height):
                self.rect.w = self.inactive_rect.width
                self.rect.h = self.inactive_rect.height
                self.rect.center = temp_rect.center


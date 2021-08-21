import pygame
import random
from ldpygame.game import Game
from ldpygame.sprite import *

class Toast(AnimatedSprite):
    Layer = 2

    #type prefixes
    #used to reference images, so to use default sprite, leave black.
    BAGEL = 'bagel-'
    POPTART = 'poptart-'
    WAFFLE = ''
    WHITE = ''
    NYAN = 'nyan'

    #provide default frame counts.
    FRAMES = {'bagel-' : 13, '': 9, 'poptart-': 13}
    TYPES = (BAGEL, POPTART, WAFFLE, WHITE)

    UNTOASTED = 'untoasted.png'
    KINDA_TOASTED = 'kindatoasted.png'
    TOASTED = 'toasted.png'
    BURNT = 'burnt.png'

    TOASTED_CHANCE = 2000

    STAGES = [UNTOASTED, KINDA_TOASTED, TOASTED, BURNT]

    def __init__(self, toast_type, num_frames, frame_delay_ms, image, rect, bounding_rect, groups, velocity=pygame.Rect(0,0,0,0)):
        self.layer = Toast.Layer
        self.toppings = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.toppings.fill(pygame.Color(0,0,0,0))
        self.did_toast_the_toast_callback = None
        self.type = toast_type
        self.rainbow_anim = None

        super(Toast, self).__init__(num_frames, frame_delay_ms, image, rect, bounding_rect, groups, velocity, Toast.Layer)

        self.score = 80
        self.cooking_time_ms = 0
        self.cooking_stage = Toast.UNTOASTED
        self.cooking_image = Toast.TYPES[Toast.TYPES.index(self.type)]+Toast.UNTOASTED
        self.halt_cooking = False

    def set_frame(self, frame_num):
        self.frame_num = frame_num
        self.image = self.frames.subsurface(pygame.Rect(frame_num * self.rect.w, 0, self.rect.w, self.rect.h)).copy()

        # dont cover the precious nyan, give it a rainbow
        if self.type == Toast.NYAN:
            surf = pygame.Surface((70, 22), pygame.SRCALPHA)
            surf.fill(pygame.Color(0,0,0,0))
            rainbow = self.rainbow_anim.subsurface(pygame.Rect(frame_num%2 * 36, 0, 36, 21))

            if self.direction == Toast.LEFT:
                surf.blit(rainbow, (26,0))
                surf.blit(self.image, (0,0))
            else:
                surf.blit(rainbow, (0,0))
                surf.blit(self.image, (28,0))

            self.image = surf
        else:
            self.image.blit(self.toppings, (0,0))

    def update_direction(self):
        super(Toast, self).update_direction()

        if self.type == Toast.NYAN:
            nyan = 'nyan' + self.direction + '-' + self.cooking_stage
            self.frames = Game.active_game.images.get(nyan, 'images')
            self.set_frame(self.frame_num)

    def update(self, tick_time):
        super(Toast, self).update(tick_time)

        # Cooking
        if self.cooking_stage != Toast.BURNT:
            self.cooking_time_ms += tick_time

            if self.cooking_time_ms > Toast.TOASTED_CHANCE:
                self.cooking_time_ms = Toast.TOASTED_CHANCE

            chance = random.randint(self.cooking_time_ms, Toast.TOASTED_CHANCE)

            if chance == Toast.TOASTED_CHANCE and not self.halt_cooking:
                self.cooking_stage = Toast.STAGES[Toast.STAGES.index(self.cooking_stage)+1]
                if self.did_toast_the_toast_callback:
                    self.did_toast_the_toast_callback(self.cooking_stage)
                self.cooking_image = Toast.TYPES[Toast.TYPES.index(self.type)]+Toast.STAGES[Toast.STAGES.index(self.cooking_stage)]
                self.cooking_time_ms = -250 #sets a minimum wait time between cooking stages.
                #It's kinda hax to have it change in less time than a button can be pushed.

                self.frames = Game.active_game.images.get(self.cooking_image, 'images')

class Plate(Sprite):
    Layer = 1
    def __init__(self, groups):
        size = (154, 104)
        image = Game.active_game.images.get('plate.png', 'images')
        super(Plate, self).__init__(pygame.Rect((0,0), size), groups, image, layer=Plate.Layer)
        self.toast = None

class Counter(Sprite):
    Layer = 0

    def __init__(self, rect, groups, image=None):
        super(Counter, self).__init__(rect, groups, image, Counter.Layer)

class ToasterTop(AnimatedSprite):
    Layer = 4

    def __init__(self, groups):
        top_image = Game.active_game.images.get('toaster_top.png', 'images')

        velocity = pygame.Rect((0,0), (0,0))
        size = (114, 138)
        rect = pygame.Rect((0, 0), size)
        velocity = pygame.Rect((0,0),(0,0))
        super(ToasterTop, self).__init__(4, 100, top_image, rect, rect, groups, velocity, ToasterTop.Layer)

    def add_velocity(self, x, y):
        return False

    def update_frame(self, tick_time):
        pass

class ToasterBack(AnimatedSprite):
    Layer = 1

    DOWN = 0
    UP = 2

    def __init__(self, groups):
        back_image = Game.active_game.images.get('toaster_back.png', 'images')

        velocity = pygame.Rect((0,0), (0,0))
        size = (164, 169)
        rect = pygame.Rect((0, 0), size)
        velocity = pygame.Rect((0,0),(0,0))
        super(ToasterBack, self).__init__(3, 1000, back_image, rect, rect, groups, velocity, ToasterBack.Layer)

    def add_velocity(self, x, y):
        return False

    def update_frame(self, tick_time):
        pass

class Condiment(AnimatedSprite):
    Layer = 7

    JELLY = 'jelly-anim.png'
    JAM = 'jam-anim.png'
    HONEY = 'honey-anim.png'
    BUTTER = 'butter-anim.png'
    PEANUT_BUTTER = 'peanut_butter-anim.png'
    CINNAMON = 'cinnamon-anim.png'
    RAINBOW = 'rainbow-anim.png'
    EGG = 'egg-anim.png'

    TYPES = [JELLY, JAM, HONEY, BUTTER, PEANUT_BUTTER, CINNAMON, RAINBOW, EGG]

    STATS = {
        BUTTER: {"score": 20, "velo_modifier": (0,0)},
        HONEY: {"score": 22, "velo_modifier": (0,0)},
        CINNAMON: {"score": 30, "velo_modifier": (0,0)},
        JAM: {"score": 35, "velo_modifier": (1,0)},
        JELLY: {"score": 40, "velo_modifier": (1,0)},
        EGG: {"score": 75, "velo_modifier": (2,1)},
        PEANUT_BUTTER: {"score": 100, "velo_modifier": (3,2)},
        RAINBOW: {"score": 200, "velo_modifier": (5,2)} # pro tip: rainbows make you fat
    }

    def __init__(self, condiment_type, num_frames, frame_delay_ms, rect, bounding_rect, groups, velocity=pygame.Rect(0,0,0,0)):
        image = Game.active_game.images.get(condiment_type, 'images')

        super(Condiment, self).__init__(num_frames, frame_delay_ms, image, rect, bounding_rect, groups, velocity, Condiment.Layer)

        self.type = condiment_type
        self.inherent_score = Condiment.STATS[condiment_type]["score"]

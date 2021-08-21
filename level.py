import pygame, math, random, os
from ldpygame.screen import Screen
from ldpygame.game import Game
from ldpygame.event_responder import KeyUpResponder, KeyDownResponder, TimerResponder
from ldpygame.sprite import SpriteDidLeaveMinYEventResponder, SpriteDidLeaveMaxYEventResponder, EventResponder
from sprite import *
from button import Button
from random import choice

class Slot(object):
    """
    Manages an available slot.  At the moment, currently simply loads
    a toast sprite into the provided group. Though it's currently surprisingly coupled
    with screen.
    """
    def __init__(self, x, y, reload_time, spritegroup, toast_size, toaster, screen):
        """
        Creates the launcher abstracts. key_code is the keycode used to
        launch this slot's toast.
        """
        self.spritegroup = spritegroup
        self.x = x
        self.y = y
        self.reload_time = reload_time
        self.active_time = reload_time
        self.toast = None
        self.toast_size = toast_size
        self.toaster = toaster
        self.screen = screen

    def launch_toast(self, event):
        if self.toast:
            toaster = self.toaster
            toaster.toast = Toast(self.toast.type,
                            Toast.FRAMES[self.toast.type], # num frames
                            25, # time between frame switches
                            Game.active_game.images.get(self.toast.cooking_image, 'images'),
                            pygame.Rect((self.x, self.y), self.toast_size),
                            toaster.bounding_rect,
                            self.spritegroup, # This adds the sprite to the screen's sprite list
                            pygame.Rect((0, -10), (0, 0)))

            #I'm going to set cooking stage and stuff on a newly created toast object instead of carrying over
            #so we can more readily change the source.  We might not want to use an actual toast sprite in final implementation.
            toaster.toast.frames = Game.active_game.images.get(self.toast.cooking_image, 'images')
            toaster.toast.cooking_image = self.toast.cooking_image
            toaster.toast.halt_cooking = True
            toaster.update_toaster_top(toaster.toast.cooking_stage)

            #Set launch velocity based on cook readyness.
            cs = self.toast.cooking_stage
            if cs == Toast.UNTOASTED:
                toaster.toast.add_velocity(0,5)
            elif cs == Toast.KINDA_TOASTED:
                toaster.toast.add_velocity(0,2)
            elif cs == Toast.TOASTED:
                toaster.toast.add_velocity(0,1)
            elif cs == Toast.BURNT:
                toaster.toast.add_velocity(0,5)

            self.spritegroup.remove(self.toast)
            self.toast = None

            toaster.toast.add_event_responder(SpriteDidLeaveMaxYEventResponder(lambda e: self.screen.remove_sprite(e.sprite, self.screen.sprites)))
            self.active_time = self.reload_time

            toaster.update_toaster_back(ToasterBack.UP)
            Game.active_game.sounds.play_sound('toaster-launch.ogg')

    def update(self, tick_time):
        """
        Similar to current sprite updates so this can be easily
        converted to a sprite if that is decided as to how it is done.
        """
        if not self.toast:
            self.active_time -= tick_time

            if self.active_time < 0:
                toast_size = (50, 50)
                toasttype = choice([Toast.WHITE, Toast.BAGEL, Toast.POPTART])
                self.toast = Toast(toasttype,
                                    1, # num frames
                                    50, # time between frame switches
                                    Game.active_game.images.get(toasttype+Toast.UNTOASTED, 'images'),
                                    pygame.Rect((self.x, self.y), self.toast_size),
                                    self.toaster.bounding_rect,
                                    self.spritegroup,
                                    pygame.Rect((0, 0), (0, 0)))
                self.toast.did_toast_the_toast_callback = self.toaster.update_toaster_top
                Game.active_game.sounds.play_sound('toaster-down.ogg')
                self.toaster.update_toaster_back(ToasterBack.DOWN)
        else:
            self.toast.velocity.x = 0
            self.toast.velocity.y = 0

def switch_to_gameover(score):
    titlebg = Game.active_game.images.get('title_menu.png', 'images').copy()
    scorestr = "You scored "+str(score)+" calories!"
    scorefont = Game.active_game.fonts.get(os.path.join('lato','Lato-Bold.ttf'),29)
    scoreimg = scorefont.render(scorestr, True, pygame.Color(0,0,0))
    y = 178
    x = (Game.active_game.size[0]/2) - ((scoreimg.get_width()/2))
    titlebg.blit(scoreimg,(x,y))
    Game.active_game.screens['gameover'].background = titlebg
    Game.active_game.activate_screen('gameover')

class ToastLevel(Screen):
    def __init__(self, name, size):
        background = pygame.Surface(size)
        background.fill(pygame.Color(214,189,0))
        super(ToastLevel, self).__init__(name, size, (0,0), background)
        self.remaining_time = 60000

        self.toasters = []

        self.setup_the_boring_graphic_stuff()
        self.score = 0
        self.font = Game.active_game.fonts.get("Helvetica", 20)
        self.scoreboard = None
        self.update_scoreboard(self.score)

        # Add managers for events this screen cares about
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_LEFT),  None, 150, lambda event: self.add_toast_velocity_delta(-1,0)))
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_RIGHT), None, 150, lambda event: self.add_toast_velocity_delta(1,0)))
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_a), None, 150, lambda event: self.add_toast_velocity_delta(-1,0)))
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_d), None, 150, lambda event: self.add_toast_velocity_delta(1, 0)))
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_w), None, 150, lambda event: self.add_nyan_toast_velocity_delta(0,-2)))
        self.event_manager.add_event_responder(KeyDownResponder((pygame.K_UP), None, 150, lambda event: self.add_nyan_toast_velocity_delta(0,-2)))


        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_p), None, -1, lambda event: Game.active_game.activate_screen('pause')))
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_PAUSE), None, -1, lambda event: Game.active_game.activate_screen('pause')))
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_ESCAPE), None, -1, lambda event: Game.active_game.activate_screen('pause')))
        
        self.gave_time = 0

        # Throw jelly
        timer = Game.active_game.timers.add(150)
        self.event_manager.add_event_responder(TimerResponder(lambda event: self.throw_condiment(), timer))
        timer.start()

    def throw_condiment(self):
        condiment_type = random.choice(Condiment.TYPES)

        # Which side to start from?
        pos_size = pygame.Rect(0,0,40,37)

        pos_size.x = random.choice([0, self.size[0]])
        pos_size.y = random.randint(100, 300)

        velocity = pygame.Rect(0,0,0,0)
        velocity.x = random.randint(-7,-1) if pos_size.x else random.randint(1,7)
        velocity.y = random.randint(-10, -5)

        if Condiment.STATS[condiment_type]["velo_modifier"][0] != 0:
            velocity.x += Condiment.STATS[condiment_type]["velo_modifier"][0]*-1 if pos_size.x else Condiment.STATS[condiment_type]["velo_modifier"][0]

        if Condiment.STATS[condiment_type]["velo_modifier"][1] != 0:
            velocity.y += Condiment.STATS[condiment_type]["velo_modifier"][1]

        condiment = Condiment(condiment_type,
                              6, 50,
                              pos_size,
                              pygame.Rect((0,0), self.size),
                              self.sprites,
                              velocity)

        condiment.add_event_responder(SpriteDidLeaveMaxYEventResponder(lambda e: self.remove_sprite(e.sprite, self.sprites)))
        return True

    def add_toast_velocity_delta(self, x_delta, y_delta):
        if not self.toasters:
            return

        for toaster in self.toasters:
            if toaster.toast:
                toaster.toast.add_velocity(x_delta, y_delta)

    def add_nyan_toast_velocity_delta(self, x_delta, y_delta):
        if not self.toasters:
            return

        for toaster in self.toasters:
            if toaster.toast and toaster.toast.type == Toast.NYAN:
                toaster.toast.add_velocity(x_delta, y_delta)

    def update_scoreboard(self, score):
        if self.scoreboard:
            self.remove_sprite(self.scoreboard, self.sprites)
        score_string = "Your plate has {} calories.".format(self.score)
        self.scoreboard = Sprite(pygame.Rect((5,5), (50, 15)), self.sprites, self.font.render(score_string, True, (0,0,0)), layer=10, dirty=2)

    def record_points_for_toast(self, victory_toast):
        self.score += victory_toast.score
        self.update_scoreboard(self.score)

    def distance(self, point_a, point_b):
        first = math.pow(point_a[0] - point_b[0], 2)
        second = math.pow(point_a[1] - point_b[1], 2)
        return math.sqrt(first + second)

    def distance_compare(self, a, b):
        distance = self.distance(a.rect.center, b.rect.center)
        return distance <= self.plate.rect.width / 2

    def update_gravity(self, tick_time):
        self.gave_time += tick_time
        if self.gave_time > 200:
            self.gave_time = 0
            return True
        return False

    def apply_gravity(self, group):
        for sprite in group.sprites():
            sprite.add_velocity(0, 1)

    def update(self, tick_time):
        super(ToastLevel, self).update(tick_time)
        self.remaining_time -= tick_time
        
        if self.remaining_time < 0:
            switch_to_gameover(self.score)
        
        if self.update_gravity(tick_time):
            self.apply_gravity(self.sprites)

        toasts = self.sprites.get_sprites_from_layer(Toast.Layer)
        plate_colliders = pygame.sprite.spritecollide(self.plate, toasts, False, self.distance_compare)
        for victory_toast in plate_colliders:
            self.record_points_for_toast(victory_toast)
            self.remove_sprite(victory_toast, self.sprites)
            Game.active_game.sounds.play_sound('land-on-plate.ogg')

        for toaster in self.toasters:
            for slot in toaster.slots:
                slot.update(tick_time)

            if toaster.toast:
                condiments = self.sprites.get_sprites_from_layer(Condiment.Layer)
                toast_colliders = pygame.sprite.spritecollide(toaster.toast, condiments, False, self.distance_compare)

                for condiment in toast_colliders:
                    # draw on top of the toast
                    topping_image = condiment.type.split('-')[0] + '-topping.png'
                    off_x = random.randint(3,15)
                    off_y = random.randint(3,15)
                    toaster.toast.toppings.blit(Game.active_game.images.get(topping_image, 'images'), (off_x, off_y))

                    # Nyan mode activate!
                    if condiment.type == Condiment.RAINBOW and toaster.toast.type == Toast.POPTART:
                        Game.active_game.sounds.load_and_play_song('nyan.ogg', volume=0.7)
                        toaster.toast.type = Toast.NYAN
                        toaster.toast.rect.w = 34
                        toaster.toast.rect.h = 22
                        toaster.toast.num_frames = 6
                        toaster.toast.frame_num = 0
                        toaster.toast.frame_delay_ms = 75
                        toaster.toast.rainbow_anim = Game.active_game.images.get('rainbows-anim.png', 'images')
                        toaster.toast.update_direction()

                    toaster.toast.score += condiment.inherent_score
                    self.remove_sprite(condiment, self.sprites)

    def setup_the_boring_graphic_stuff(self):
        size = (700, 450)
        top = self.size[1] - size[1]
        self.counter = Counter(pygame.Rect((0, top), size), self.sprites, Game.active_game.images.get('counter.png', 'images'))
        size = (79,79)
        top = self.size[1] - size[1]
        self.plate = Plate(self.sprites)
        self.plate.rect.left = 25
        self.plate.rect.top = 650

        toaster1 = Toaster(1, (200, 500), pygame.Rect((0,0), self.size), self.sprites, self)
        toaster2 = Toaster(2, (350, 400), pygame.Rect((0,0), self.size), self.sprites, self)
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_1), None, -1, toaster1.slots[0].launch_toast))
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_2), None, -1, toaster2.slots[0].launch_toast))
        self.toasters.append(toaster1)
        self.toasters.append(toaster2)

    def remove_sprite(self, sprite, group):
        group.remove(sprite)

        # If we had a nyantart, restart the normal music when it dies
        if type(sprite) == Toast and sprite.type == Toast.NYAN:
            Game.active_game.sounds.load_and_play_song('bu-the-paths-birds.ogg')

class Toaster(object):
    def __init__(self, toaster_id, pos, bounding_rect, sprite_groups, screen):
        self.id = toaster_id
        self.pos = pos
        self.slots = []
        self.toast_reload_time = 2500
        self.toast = None
        self.cooking_toast = None
        self.bounding_rect = bounding_rect #used for generating toast

        toast_size = (50, 50)
        x_delta = 25
        y_delta = 60

        self.toaster_front = ToasterTop(sprite_groups)
        self.toaster_front.rect.left = pos[0]
        self.toaster_front.rect.top = pos[1]+18

        self.toaster_back = ToasterBack(sprite_groups)
        self.toaster_back.rect.left = pos[0]
        self.toaster_back.rect.top = pos[1]

        self.slots.append(Slot(self.toaster_back.rect.left + x_delta, self.toaster_back.rect.top + y_delta, self.toast_reload_time, sprite_groups, toast_size, self, screen))

    def update_toaster_top(self, toasting):
        self.toaster_front.set_frame(Toast.STAGES.index(toasting))

    def update_toaster_back(self, state):
        self.toaster_back.set_frame(state)

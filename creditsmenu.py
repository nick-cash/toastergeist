import pygame
from ldpygame.event_responder import TimerResponder, KeyUpResponder
from ldpygame.game import Game
from menu import Menu
from button import Button

class RotatingImageMenu(Menu):
    def __init__(self, name, size, images, interval=0, offset=(0,0), background=None, default_font=None):
        super(RotatingImageMenu, self).__init__(name, size, offset, background, default_font)

        self.current_image = 0
        self.num_images = len(images)
        self.images = images
        self.interval = interval #interval of 0 can be used for key-only rotating

        if self.interval:
            timer = Game.active_game.timers.add(self.interval)
            self.event_manager.add_event_responder(TimerResponder(lambda event: self.rotate(), timer))
            timer.start()

        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_c), None, -1, lambda event: Game.active_game.activate_screen('mainmenu')))

        backimg = Game.active_game.images.get('back_button.png', 'images')
        backlambda = lambda: Game.active_game.activate_screen("mainmenu")

        backbtn = Button(pygame.Rect(10,740,50,50),
                         self.buttons,
                         inactive_image=backimg,
                         active_image=backimg,
                         down_image=backimg,
                         up_image=backimg,
                         callback=backlambda)

    def rotate(self):
        self.current_image += 1

        if self.current_image >= self.num_images:
            self.current_image = 0

    def draw(self):
        """
        Draw to the screen. If dirty_rects is empty, it will redraw the entire
        screen. It is best to keep track of areas that need to be redrawn.
        """
        self.screen_surface.blit(self.images[self.current_image], (0,0))

        self.dirty_rects += self.sprites.draw(self.screen_surface)
        self.dirty_rects += self.buttons.draw(self.screen_surface)

        return [pygame.Rect((0,0), self.size)]

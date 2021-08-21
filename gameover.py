import pygame, os
from menu import Menu
from ldpygame.game import Game
from ldpygame.event_responder import KeyUpResponder
from button import Button
from level import ToastLevel

def exit_game():
    Game.active_game.exit()

def newgame():
    del Game.active_game.screens['main']
    Game.active_game.add_screen(ToastLevel('main', Game.active_game.size))
    Game.active_game.activate_screen('mainmenu')

class GameOverMenu(Menu):
    def __init__(self, name, size, offset=(0,0), background=None, default_font=None):
        """
        Init's the menu, add an additional buttons Group for handling buttons.
        """
        super(GameOverMenu, self).__init__(name, size, offset, background, default_font)

        resimg = Game.active_game.images.get('new_button.png', 'images')
        exitimg = Game.active_game.images.get('exit_button.png', 'images')
        rainbow = Game.active_game.images.get('rainbow.png', 'images')
        
        aresimg = resimg.copy();
        aresimg.blit(rainbow,(0,0))
        aexitimg = exitimg.copy();
        aexitimg.blit(rainbow,(0,0))
        
        retnbtn = Button(pygame.Rect(116,242,462,312),
                        self.buttons,
                        inactive_image=resimg,
                        active_image=aresimg,
                        down_image=aresimg,
                        up_image=aresimg,
                        callback=newgame)

        exitbtn = Button(pygame.Rect(488,594,164,169),
                        self.buttons,
                        inactive_image=exitimg,
                        active_image=aexitimg,
                        down_image=aexitimg,
                        up_image=aexitimg,
                        callback=exit_game)

        #self.create_default_button(pygame.Color(255,255,247), 'Play', lambda: Game.active_game.activate_screen("main"))
        #self.create_default_button(pygame.Color(255,255,247), 'Exit Game', exit_game)
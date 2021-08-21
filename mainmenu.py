import pygame
from menu import Menu
from ldpygame.game import Game
from ldpygame.event_responder import KeyUpResponder
from button import Button

def exit_game():
    Game.active_game.exit()

class MainMenu(Menu):
    def __init__(self, name, size, offset=(0,0), background=None, default_font=None):
        """
        Init's the menu, add an additional buttons Group for handling buttons.
        """
        super(MainMenu, self).__init__(name, size, offset, background, default_font)

        #oops, these are bigger than the old images, for now I'll just scale so it's similar.
        toastbtn = pygame.transform.rotozoom(Game.active_game.images.get('toastbtns.png', 'images'),0,0.854) 
        #A simple way to set the reset the size from 150 to 128
        playimg = Game.active_game.images.get('play_button.png', 'images')
        exitimg = Game.active_game.images.get('exit_button.png', 'images')
        credimg = Game.active_game.images.get('credit_button.png', 'images')
        rainbow = Game.active_game.images.get('rainbow.png', 'images')
        
        aplayimg = playimg.copy()
        aplayimg.blit(rainbow,(0,0))
        aexitimg = exitimg.copy()
        aexitimg.blit(rainbow,(0,0))
        acredimg = credimg.copy()
        acredimg.blit(rainbow,(0,0))

        playlambda = lambda: Game.active_game.activate_screen("main")
        credlambda = lambda: Game.active_game.activate_screen('credits')
        
        playbtn = Button(pygame.Rect(38,150,193,228),
                        self.buttons,
                        inactive_image=playimg,
                        active_image=aplayimg,
                        down_image=aplayimg,
                        up_image=aplayimg,
                        callback=playlambda)

        credbtn = Button(pygame.Rect(38,360,252,165),
                        self.buttons,
                        inactive_image=credimg,
                        active_image=acredimg,
                        down_image=acredimg,
                        up_image=acredimg,
                        callback=credlambda)

        exitbtn = Button(pygame.Rect(38,531,164,169),
                        self.buttons,
                        inactive_image=exitimg,
                        active_image=aexitimg,
                        down_image=aexitimg,
                        up_image=aexitimg,
                        callback=exit_game)


        #self.create_default_button(pygame.Color(255,255,247), 'Play', lambda: Game.active_game.activate_screen("main"))
        #self.create_default_button(pygame.Color(255,255,247), 'Exit Game', exit_game)

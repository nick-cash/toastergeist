from __future__ import print_function
import pygame, os
from ldpygame.screen import Screen
from ldpygame.event_responder import KeyUpResponder, QuitResponder

from game import ToastGame
from level import ToastLevel
from sprite import Toast, Condiment
from mainmenu import MainMenu
from creditsmenu import RotatingImageMenu
from pausemenu import PauseMenu
from gameover import GameOverMenu

def exit_game(event):
   ToastGame.active_game.exit()

# Lets do it
g = ToastGame('Toastergeist', size=(700,800))

# Add some global input handlers
g.event_manager.add_event_responder(KeyUpResponder((pygame.K_m), None, -1, lambda event: ToastGame.active_game.sounds.toggle_music()))
g.event_manager.add_event_responder(QuitResponder(exit_game))

# Main screen turn on!
s = ToastLevel('main', g.size)

# Main menu turn on!
m = MainMenu('mainmenu', g.size, background=g.images.get('title_menu_with_instructions.png', 'images'), default_font=g.fonts.get(os.path.join('lato','Lato-Bold.ttf'),21))

# Set us up the pause menu!
p = PauseMenu('pause', g.size, background=g.images.get('pausebg.png', 'images'), default_font=g.fonts.get(os.path.join('lato','Lato-Bold.ttf'),21))

#You know what you doing, game over!
go = GameOverMenu('gameover', g.size, background=g.images.get('title_menu.png', 'images'), default_font=g.fonts.get(os.path.join('lato','Lato-Bold.ttf'),21))

credit_images = []
credit_images.append(g.images.get('credits1.png', 'images'))
credit_images.append(g.images.get('credits2.png', 'images'))

m2 = RotatingImageMenu('credits', g.size, credit_images, interval=5000, default_font=g.fonts.get(os.path.join('lato','Lato-Bold.ttf'),21))

g.add_screen(go)
g.add_screen(p)
g.add_screen(s)
g.add_screen(m2)
g.activate_screen(m)
g.sounds.load_and_play_song('bu-the-paths-birds.ogg', volume=0.7)

# And off we go
g.run()

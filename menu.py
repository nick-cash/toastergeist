import pygame
from ldpygame.sprite import SpriteManager
from ldpygame.screen import Screen
from ldpygame.game import Game
from ldpygame.asset_manager import FontManager
from button import Button
from ldpygame.event_responder import KeyUpResponder, QuitResponder, KeyDownResponder, MouseButtonDownResponder, MouseButtonUpResponder, MouseMotionResponder

class Menu(Screen):
    """
    Menu screen... pretty much self-explanatory, right?
    """
    def __init__(self, name, size, offset=(0,0), background=None, default_font=None):
        """
        Init's the menu, add an additional buttons Group for handling buttons.
        """
        super(Menu, self).__init__(name, size, offset, background)
        g = Game.active_game
        if default_font:
            self.default_font = default_font
        else:
            self.default_font = g.fonts.get("Helvetica,Arial,Vera,Times,Times New Roman", 20);

        self.auto_btn_count = 0
        self.active_btn = -1
        self.buttons = SpriteManager()
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_UP), None, -1, self.goup))
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_DOWN), None, -1, self.godown))
        self.event_manager.add_event_responder(KeyUpResponder((pygame.K_RETURN), None, -1, self.runcallback))
        self.event_manager.add_event_responder(MouseButtonDownResponder(self.mousedown))
        self.event_manager.add_event_responder(MouseButtonUpResponder(self.mouseup))
        self.event_manager.add_event_responder(MouseMotionResponder(self.mousemove))

    def mousemove(self,event):
        """
        This is called on mouse movement events.  If mouse is down and collision is detected, set
        display state to down.
        """
        buttons = self.buttons.sprites()
        for x in range(len(buttons)):
            if buttons[x].rect.collidepoint(event.pos):
                self.active_btn = x
                self.set_active(x) #Set all to inactive really.
                if(event.buttons[0] == 1) :
                    buttons[x].set_state('down')
                else:
                    buttons[x].set_state('active')
                break

    def mouseup(self,event):
        """
        This is called on mouse up events
        """
        buttons = self.buttons.sprites()
        self.set_active(self.active_btn)
        for x in range(len(buttons)):
            if buttons[x].rect.collidepoint(event.pos):
                self.active_btn = x
                self.set_active(x) #Set all to inactive really.
                buttons[x].set_state('up')
                if buttons[x].callback:
                    buttons[x].callback()
                break

    def mousedown(self, event):
        """
        This is called on mouse down events
        """
        #Why is there no collide point for groups?
        buttons = self.buttons.sprites()
        for x in range(len(buttons)):
            if buttons[x].rect.collidepoint(event.pos):
                self.active_btn = x
                self.set_active(x) #Set all to inactive really.
                buttons[x].set_state('down')
                break
        #self.buttons()

    def update(self, tick_time):
        """
        Handle sprite and other screen updates. Events will be passed directly
        to our event_manager when the screen is active, so we don't need to
        process them here.
        """
        buttons = self.buttons.sprites()
        if len(buttons) > 0:
            if self.active_btn == -1:
                self.set_active(0)
        self.sprites.update(tick_time)
        self.buttons.update(tick_time)

    def runcallback(self, *args):
        """
        Runs a callback for a particular menu entry.  If a valid entry is current.
        """
        buttons = self.buttons.sprites()
        if buttons[self.active_btn]:
            if buttons[self.active_btn].callback:
                buttons[self.active_btn].callback()


    def godown(self, *args):
        """
        Increment menu position.
        """
        self.set_active(self.active_btn+1)

    def goup(self, *args):
        """
        Decrement menu position
        """
        if(self.active_btn == 0):
            self.set_active(len(self.buttons.sprites())-1)
        else:
            self.set_active(self.active_btn-1);

    def set_active(self, index):
        buttons = self.buttons.sprites()
        if len(buttons):
            i = index%len(buttons)
            for x in range(len(buttons)):
                if i != x:
                    buttons[x].set_state('inactive')
                else:
                    buttons[x].set_state('active')
            self.active_btn = i

    def create_default_button(self, color, text, callback):
        """
        Makes a very generic menu button. Overload this in custom
        classes to make prettier ones.
        """
        d = self.default_font.render('>>'+text+'<<', True, color)
        u = self.default_font.render('> '+text+' <', True, color)
        a = u
        i = self.default_font.render(text, True, color)
        activerect = a.get_rect();
        activerect.center = (self.size[0]/2,(self.size[1]/2)+((activerect.height+10)*self.auto_btn_count))
        self.auto_btn_count+=1
        button = Button(activerect,
                        self.buttons,
                        inactive_image=i,
                        active_image=a,
                        down_image=d,
                        up_image=u,
                        velocity=pygame.Rect(0,0,0,0),
                        active_rect=a.get_rect(),
                        down_rect=d.get_rect(),
                        up_rect=u.get_rect(),
                        callback=callback)

    def draw(self):
        """
        Draw to the screen. If dirty_rects is empty, it will redraw the entire
        screen. It is best to keep track of areas that need to be redrawn.
        """
        self.screen_surface.blit(self.background, (0,0))
        self.dirty_rects += self.sprites.draw(self.screen_surface)

        self.dirty_rects += self.buttons.draw(self.screen_surface)
        dirty_rects = self.dirty_rects
        self.dirty_rects = []

        return dirty_rects

    def activate(self):
        self.dirty_rects.append(pygame.Rect((0,0), self.size))
        pass

    def deactivate(self):
        pass

from event_responder import EventResponder

class SpriteWillLeaveMinXEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteWillLeaveMinXEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteWillLeaveEventResponder-minX')

class SpriteWillLeaveMaxXEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteWillLeaveMaxXEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteWillLeaveEventResponder-maxX')

class SpriteWillLeaveMaxYEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteWillLeaveMaxYEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteWillLeaveEventResponder-maxY')

class SpriteWillLeaveMinYEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteWillLeaveMinYEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteWillLeaveEventResponder-minY')


class SpriteDidLeaveMinXEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteDidLeaveMinXEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteDidLeaveEventResponder-minX')

class SpriteDidLeaveMaxXEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteDidLeaveMaxXEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteDidLeaveEventResponder-maxX')

class SpriteDidLeaveMaxYEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteDidLeaveMaxYEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteDidLeaveEventResponder-maxY')

class SpriteDidLeaveMinYEventResponder(EventResponder):
   def __init__(self, callback):
        super(SpriteDidLeaveMinYEventResponder, self).__init__(EventResponder.RepeatsNever, callback, 'SpriteDidLeaveEventResponder-minY')

class SpriteEvent(object):
    def __init__(self, type, sprite):
        self.type = type
        self.sprite = sprite

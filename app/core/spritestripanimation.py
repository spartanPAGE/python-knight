from .spritesheet import SpriteSheet

class SpriteStripAnimation(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self._size = (rect[2], rect[3])
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
        self.image = None

    def get_size(self):
        return self._size
    
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def is_done(self):
        return self.i >= len(self.images)
    
    def next(self):
        if self.is_done():
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self

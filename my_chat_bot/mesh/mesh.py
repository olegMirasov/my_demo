import pygame as pg
import time


class Mesh:
    image_format = '.png'
    folder = 'temp_images/'

    def __init__(self, w=800, h=600):
        pg.init()
        self.w, self.h = w, h
        self.res = (self.w, self.h)
        self.color = (145, 135, 214)

    def get_image_path(self):
        surface = pg.Surface(self.res)
        surface.fill(self.color)
        name = self._new_name()
        path = self.folder + name
        pg.image.save(surface, path)
        return path

    def _new_name(self):
        s = str(time.time())
        return s + self.image_format

m = Mesh()
print(m.get_image_path())

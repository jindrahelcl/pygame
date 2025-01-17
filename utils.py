import os
import pygame

BASE_IMG_PATH = "assets/"


def load_image(path):
  img = pygame.image.load(BASE_IMG_PATH + path).convert()
  img.set_colorkey((237, 72, 255))
  return img


def load_images(path):
  images = []
  for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
    images.append(load_image(path + "/" + img_name))

  return images


class Animation:
  def __init__(self, images, img_dur=5, loop=True):
    self.images = images
    self.loop = loop
    self.img_duration = img_dur
    self.done = False
    self.frame = 0

  def copy(self):
    return Animation(self.images, self.img_duration, self.loop)

  def img(self):
    return self.images[self.frame // self.img_duration]

  def update(self):
    if self.loop:
      self.frame = (self.frame + 1) % (len(self.images) * self.img_duration)
    else:
      self.frame = min(self.frame + 1, len(self.images) * self.img_duration - 1)
      if self.frame >= self.img_duration * len(self.images) - 1:
        self.done = True


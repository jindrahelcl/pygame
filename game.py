import pygame
import sys

from utils import Animation
from pejsek import Pejsek


class Game:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((800, 600))
    self.clock = pygame.time.Clock()

    pejsek = pygame.image.load("assets/pejsek.png").convert()
    pejsek.set_colorkey((237, 72, 255))

    frames = []
    for i in reversed([(0, 0), (128, 0), (0, 128), (128, 128)]):
      frames.append(pygame.transform.flip(
        pygame.transform.chop(pejsek, (i[0], i[1], 128, 128)), True, False))

    pejsek_sit = pygame.image.load("assets/pejsek-sit-128.png").convert()
    pejsek_sit.set_colorkey((237, 72, 255))

    sit_frames = []
    for i in [(0, 0), (128, 0), (0, 128), (128, 128)]:
      sit_frames.append(pygame.transform.flip(
        pygame.Surface.subsurface(pejsek_sit, (i[0], i[1], 128, 128)), True, False))

    pejsek_jump = pygame.image.load("assets/pejsek-jump.png").convert()
    pejsek_jump.set_colorkey((237, 72, 255))

    jump_frames = []
    for i in range(8):
      jump_frames.append(
        pygame.transform.scale(
          pygame.transform.flip(
            pygame.Surface.subsurface(pejsek_jump, (32 * i, 0, 32, 32)),
          True, False),
        (128, 128)))

    self.assets = {
      "pejsek/idle": Animation([frames[2]]),
      "pejsek/walk": Animation(frames, img_dur=5),
      "pejsek/sitting": Animation([sit_frames[-1]]),
      "pejsek/sit": Animation(sit_frames, img_dur=5, loop=False),
      "pejsek/stand": Animation(list(reversed(sit_frames)), img_dur=5, loop=False),
      "pejsek/jump": Animation(jump_frames, img_dur=5, loop=False),
    }

    self.pejsek = Pejsek(self, [100, 100])
    self.movement = [False, False]

  def run(self):
    while True:

      self.screen.fill((255, 255, 255))

      self.pejsek.update(((self.movement[1] - self.movement[0]) * 2.5, 0))
      self.pejsek.render(self.screen)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            self.movement[0] = True
          if event.key == pygame.K_RIGHT:
            self.movement[1] = True
          if event.key == pygame.K_DOWN:
            self.pejsek.sit()
          if event.key == pygame.K_UP:
            self.pejsek.stand()
          if event.key == pygame.K_SPACE:
            self.pejsek.jump()

        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LEFT:
            self.movement[0] = False
          if event.key == pygame.K_RIGHT:
            self.movement[1] = False

      pygame.display.update()
      self.clock.tick(60)

if __name__ == "__main__":
  Game().run()
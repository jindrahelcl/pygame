import pygame


class Pejsek:

  def __init__(self, game, pos):
    self.game = game
    self.pos = pos
    self.flip = False
    self.action = ""
    self.animation = None

    self.set_action("idle")
    self.anim_offset = (0, 0)
    self.velocity = [0, 0]

    self.sitting = False
    self.jump_movements = [(0, 0), (0, 0), (-1, 1), (11, 3), (7, 1), (3, -5), (2, 0), (1, 0)]
    self.jump_state = 0

  def set_action(self, action):
    if action != self.action:
      self.action = action
      self.animation = self.game.assets["pejsek/" + self.action].copy()
      print(action)

  def sit(self):
    if not self.sitting:
      self.sitting = True
      self.set_action("sit")

  def stand(self):
    if self.sitting and self.action == "sitting":
      self.set_action("stand")

  def jump(self):
    if not self.sitting:
      self.set_action("jump")
      self.jump_state = 0

  def update(self, movement=(0, 0)):
    if not self.sitting and not self.action == "jump":
      frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
      self.pos[0] += frame_movement[0]

      if movement[0] > 0:
        self.flip = False
      if movement[0] < 0:
        self.flip = True

      if movement[0] != 0:
        self.set_action("walk")
      else:
        self.set_action("idle")

    if self.action == "sit":
      if self.animation.done:
        self.set_action("sitting")

    if self.action == "stand":
      if self.animation.done:
        self.sitting = False
        self.set_action("idle")

    if self.action == "jump":
      horiz = self.jump_movements[self.animation.frame // self.animation.img_duration][0]
      self.pos[0] -= horiz if self.flip else - horiz
      self.pos[1] -= self.jump_movements[self.animation.frame // self.animation.img_duration][1]

      if self.animation.done:
        self.set_action("idle")

    self.animation.update()


  def render(self, surf, offset=(0, 0)):
    surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
      (self.pos[0] - offset[0] + self.anim_offset[0],
       self.pos[1] - offset[1] + self.anim_offset[1]))
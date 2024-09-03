import pygame
import numpy as np
from geometric_rain.config import Conf
from geometric_rain.classes.display import Display



class Block(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(Conf.block_border_color)
        pygame.draw.rect(self.image,
                         color,
                         (Conf.block_border_width,
                          Conf.block_border_width,
                          size[0] - Conf.block_border_width * 2,
                          size[1] - Conf.block_border_width * 2),
                          border_radius=Conf.block_border_radius)
        self.rect = self.image.get_rect()
        self.gx = 0
        self.gy = 0


class Piece(pygame.sprite.Group):
    def __init__(self,
                 shape: list,
                 color: tuple,
                 start_x: int,
                 settled_pieces: pygame.sprite.Group = None,
                 display: Display = None,
                 inert: bool = False):
        super().__init__()
        self.shape = shape
        self.color = color
        self.inert = inert
        self.settled_pieces = settled_pieces
        self.settled = False
        self.game_over = False
        self.display = display

        # grid coords
        self.gx = start_x
        self.gy = 0

        # pixel coords
        self.px = self.gx
        self.py = 0
        self.spawn()

    def spawn(self):
        for gy, row in enumerate(self.shape):
            for gx, populated in enumerate(row):
                if populated:
                    block = Block(self.color, (self.display.block_size, self.display.block_size))
                    block.rect.x = (self.gx + gx) * self.display.block_size
                    block.rect.y = (self.gy + gy) * self.display.block_size
                    block.gx = self.gx + gx
                    block.gy = self.gy + gy
                    self.add(block)
        if not self.inert and self.y_collision():
            self.game_over = True

    def respawn(self):
        for block in self:
            block.kill()
        self.spawn()

    def move(self, dgx, dgy):
        if dgx:
            self.move_x(dgx)
        if dgy:
            self.move_y(dgy)

    def move_x(self, dgx):
        self.gx += dgx
        self.px += dgx * self.display.block_size
        for block in self:
            block.rect.x += dgx * self.display.block_size
            block.gx += dgx
        if not self.inert and self.x_collision():
            self.gx -= dgx
            self.px -= dgx * self.display.block_size
            for block in self:
                block.rect.x -= dgx * self.display.block_size
                block.gx += dgx

    def move_y(self, dgy):
        self.gy += dgy
        self.py += dgy * self.display.block_size
        for block in self:
            block.rect.y += dgy * self.display.block_size
            block.gy += dgy
        if not self.inert and self.y_collision():
            self.gy -= dgy
            self.py -= dgy * self.display.block_size
            for block in self:
                block.rect.y -= dgy * self.display.block_size
                block.gy -= dgy
            return

    def x_collision(self):
        """
        check if any blocks in self group collides with settled pieces,
        and also if it collides with left or right bounds of the screen
        :return:
        """
        if self.inert:
            return
        for block in self:
            if block.rect.left < 0:
                return True
            elif block.rect.right > self.display.game_panel.content_w:
                return True
        collisions = pygame.sprite.groupcollide(self, self.settled_pieces, False, False)
        if collisions:
            for block in collisions:
                for settled_block in collisions[block]:
                    if block.rect.right >= settled_block.rect.left:
                        return True
                    elif block.rect.left <= settled_block.rect.right:
                        return True

    def y_collision(self):
        """
        check if any blocks in self group collides with settled pieces,
        and also if it collides with the bottom of the screen
        :return:
        """
        if self.inert:
            return
        for block in self:
            if block.rect.top < 0:
                return True
            if block.rect.bottom > self.display.game_panel.content_h:
                self.settled = True
                return True
        collisions = pygame.sprite.groupcollide(self, self.settled_pieces, False, False)
        if collisions:
            for block in collisions:
                for settled_block in collisions[block]:
                    if block.rect.bottom >= settled_block.rect.top:
                        self.settled = True
                        return True
                    if block.rect.top <= settled_block.rect.bottom:
                        return True

    def rotate(self, half_turn=False):
        rotations = -2 if half_turn else -1
        self.shape = np.rot90(self.shape, rotations)
        self.respawn()
        if self.inert:
            return
        for block in self:
            if block.rect.left < 0:
                self.unrotate()
                return False
            if block.rect.right > self.display.game_panel.content_w:
                self.unrotate()
                return False
        collisions = pygame.sprite.groupcollide(self, self.settled_pieces, False, False)
        if collisions:
            self.unrotate()
            return False
        return True

    def unrotate(self):
        self.shape = np.rot90(self.shape, 1)
        self.respawn()



class I(Piece):
    gw = 4
    gh = 1
    name = 'I'

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=2):
        shape = [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        color = (110, 236, 238)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class J(Piece):
    gw = 3
    gh = 2
    name = 'J'

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[1, 0, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
        color = (0, 0, 230)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class L(Piece):
    gw = 3
    gh = 2
    name = 'L'

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[0, 0, 1],
                 [1, 1, 1],
                 [0, 0, 0]]
        color = (228, 163, 57)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class O(Piece):
    gw = 2
    gh = 2
    name = 'O'

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[1, 1],
                 [1, 1]]
        color = (240, 240, 79)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class S(Piece):
    name = 'S'
    gw = 3
    gh = 2

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[0, 1, 1],
                 [1, 1, 0],
                 [0, 0, 0]]
        color = (110, 236, 71)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class T(Piece):
    name = 'T'
    gw = 3
    gh = 2

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
        color = (146, 28, 231)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)


class Z(Piece):
    name = 'Z'
    gw = 3
    gh = 2

    def __init__(self,
                 settled_pieces,
                 display,
                 inert=False,
                 spawn_x=3):
        shape = [[1, 1, 0],
                 [0, 1, 1],
                 [0, 0, 0]]
        color = (220, 47, 33)
        self.pw = self.gw * display.block_size
        self.ph = self.gh * display.block_size
        super().__init__(shape, color, spawn_x, settled_pieces, display, inert)

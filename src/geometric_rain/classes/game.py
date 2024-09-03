import sys
import time
import pygame
from random import choice
from geometric_rain.classes.pieces import I, J, L, O, S, T, Z
from geometric_rain.classes.input import Inputs
from geometric_rain.config import Conf


class Game(Inputs):

    def __init__(self, display, sound, scorekeeper):
        super().__init__()
        self.display = display
        self.sound = sound
        self.scorekeeper = scorekeeper
        self.settled_pieces = pygame.sprite.Group()
        self.pieces = [T, J, Z, O, S, L, I]
        self.clock = pygame.time.Clock()
        self.ticks_since_last_fall = 0
        self.next_piece = choice(self.pieces)
        self.piece = self.next_piece(self.settled_pieces, self.display)
        self.update_stats()

        self.slow_tick_interval = Conf.fall_frames_interval
        self.fast_tick_interval = Conf.fast_fall_frames_interval

    def update_stats(self):
        self.scorekeeper.stats[self.piece.name] += 1

    def down_arrow(self):
        if self.ticks_since_last_fall >= self.fast_tick_interval:
            self.maybe_fall()

    def left_arrow(self):
        self.piece.move(-1, 0)
        self.left_pressed = False

    def right_arrow(self):
        self.piece.move(1, 0)
        self.right_pressed = False

    def up_arrow(self):
        rotated = self.piece.rotate()
        if rotated:
            self.sound.rotate.play()

    def end_game(self):
        self.scorekeeper.save_appdata()
        self.running = False
        pygame.quit()
        sys.exit()

    def render(self) -> pygame.surface.Surface:
        game_area = self.display.game_panel.generate_content()
        for block in self.piece:
            game_area.blit(block.image, block.rect.topleft)
        for block in self.settled_pieces:
            game_area.blit(block.image, block.rect.topleft)
        return game_area

    def maybe_fall(self):
        if self.fast_drop_locked:
            self.fast_drop_lockout_ticks += 1
            if self.fast_drop_lockout_ticks >= Conf.fast_fall_lockout_ticks:
                self.fast_drop_locked = False
                self.fast_drop_lockout_ticks = 0
        if self.ticks_since_last_fall >= self.slow_tick_interval or self.fast_drop_active:
            self.piece.move(0, 1)
            if self.piece.settled:
                self.settled_pieces.add(self.piece)
                self.piece = self.next_piece(self.settled_pieces, self.display)
                self.next_piece = choice(self.pieces)
                self.update_stats()
                self.sound.piece_settled.play()
                self.fast_drop_active = False
                self.fast_drop_locked = True
                self.fast_drop_lockout_ticks = 0
                if self.piece.game_over:
                    time.sleep(5)
                    print('Game Over')
                    self.end_game()
            else:
                self.scorekeeper.current_score += 2 if self.fast_drop_active else 1
            self.ticks_since_last_fall = 0

    def shift_blocks_down(self, floor_gy):
        min_gy = min(block.gy for block in self.settled_pieces) if self.settled_pieces else 0
        current_gy = floor_gy
        while current_gy >= min_gy:
            for block in self.settled_pieces:
                if block.gy == current_gy:
                    block.gy += 1
                    block.rect.y += self.display.block_size
            current_gy -= 1

    def find_completed_rows(self):
        rows = {}
        for block in self.settled_pieces:
            if block.gy not in rows:
                rows[block.gy] = 1
            else:
                rows[block.gy] += 1
        completed_rows = []
        for row_y, count in rows.items():
            if count == Conf.grid_width:
                completed_rows.append(row_y)
        completed_rows.sort()
        return completed_rows

    def process_completed_rows(self):
        completed_rows = self.find_completed_rows()
        if completed_rows:
            self.scorekeeper.rows_cleared += len(completed_rows)
            self.scorekeeper.total_rows_cleared += len(completed_rows)
            self.scorekeeper.current_score += self.scorekeeper.rewards[len(completed_rows) - 1] * (self.scorekeeper.current_level + 1)

            for row_y in completed_rows:
                for block in self.settled_pieces:
                    if block.gy == row_y:
                        block.kill()
                self.shift_blocks_down(row_y)
            self.render()
            if self.scorekeeper.rows_cleared < 10:
                self.sound.row_completed.play()

    def check_level(self):
        if self.scorekeeper.rows_cleared >= 10:
            self.scorekeeper.current_level += 1
            self.scorekeeper.rows_cleared = 0
            self.slow_tick_interval = max(1, self.slow_tick_interval - 2)
            print(f"Level {self.scorekeeper.current_level}")
            if self.scorekeeper.current_level <= 8:
                self.slow_tick_interval -= 5
            elif 8 < self.scorekeeper.current_level <= 12:
                self.slow_tick_interval -= 2
            elif 12 < self.scorekeeper.current_level <= 15:
                self.slow_tick_interval -= 1
            self.sound.levelup.play()

    def iteration(self):

        self.process_completed_rows()
        self.check_level()

        self.event_loop()
        self.key_check()
        self.maybe_fall()
        self.ticks_since_last_fall += 1

        return self.render()

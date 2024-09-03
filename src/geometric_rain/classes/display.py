import pygame
from geometric_rain.config import Conf
from geometric_rain.classes.scores import Scorekeeper



class Panel:
    def __init__(self,
                 block_size: int,
                 blocks_wide: int | float,
                 blocks_high: int | float,
                 left_neighbors: list = None,
                 top_neighbors: list = None,
                 left_margin: int = 0,
                 top_margin: int = 0,
                 border_width: int = 2,
                 background_color: tuple | None = None,
                 outer_border_color: tuple | None = None,
                 inner_border_color: tuple | None = None):
        self.left_neighbors = left_neighbors or []
        self.top_neighbors = top_neighbors or []

        self.left_margin = left_margin
        self.top_margin = top_margin

        self.border_width: int = border_width
        self.block_size = block_size
        self.blocks_wide: int = blocks_wide
        self.blocks_high: int = blocks_high

        self.content_w: int = self.block_size * self.blocks_wide
        self.content_h: int = self.block_size * self.blocks_high
        self.background_color: tuple = background_color or (0, 0, 0)

        self.inner_border_w: int = self.content_w + (self.border_width * 4)
        self.inner_border_h: int = self.content_h + (self.border_width * 4)
        self.inner_border_color: tuple = inner_border_color or (164, 164, 255)

        self.outer_border_w: int = self.inner_border_w + (self.border_width * 2)
        self.outer_border_h: int = self.inner_border_h + (self.border_width * 2)

        self.w = self.outer_border_w
        self.h = self.outer_border_h
        self.outer_border_color: tuple = outer_border_color or (0, 0, 0)

        self.margin_left = Conf.content_margin + self.left_margin
        self.margin_left += sum([panel.w for panel in self.left_neighbors])
        self.margin_left += sum([panel.left_margin for panel in self.left_neighbors])
        self.margin_left += len(self.left_neighbors) * Conf.ui_margins

        self.margin_top = Conf.content_margin + self.top_margin
        self.margin_top += sum([panel.h for panel in self.top_neighbors])
        self.margin_top += sum([panel.top_margin for panel in self.top_neighbors])
        self.margin_top += len(self.top_neighbors) * Conf.ui_margins

        self.pos = (self.margin_left, self.margin_top)
        self.size = (self.w, self.h)

    def generate_content(self) -> pygame.Surface:
        surface = pygame.Surface((self.content_w, self.content_h))
        surface.fill(self.background_color)
        return surface

    def add_border(self, surface: pygame.Surface) -> pygame.Surface:
        outer_border = pygame.Surface((self.outer_border_w, self.outer_border_h))
        outer_border.fill(self.outer_border_color)
        pygame.draw.rect(outer_border, self.inner_border_color,
                         (self.border_width, self.border_width, self.inner_border_w, self.inner_border_h),
                         self.border_width)
        outer_border.blit(surface, (self.border_width * 3, self.border_width * 3))
        return outer_border


class Display:

    def __init__(self,
                 scorekeeper: Scorekeeper,
                 display_mode: str = 'windowed'):

        pygame.init()
        pygame.display.set_caption("Geometric Rain")
        self.display_mode = display_mode
        self.scorekeeper = scorekeeper

        screen_metadata = pygame.display.Info()
        self.monitor_x = screen_metadata.current_w
        self.monitor_y = screen_metadata.current_h

        self.scaled_y = int(self.monitor_y * Conf.ui_scale)
        self.block_size = int((self.scaled_y * 0.9) // Conf.grid_height)
        self.scaled_x = int((Conf.content_margin * 2) + (self.block_size * 22.5) + (Conf.ui_margins * 2) + 36)

        self.stats_panel = Panel(self.block_size,
                                 Conf.grid_width - 2,
                                 Conf.grid_height - 2,
                                 top_margin=int(self.block_size * 3) + 12 + Conf.ui_margins)

        self.lines_panel = Panel(self.block_size,
                                 Conf.grid_width,
                                 1,
                                 left_neighbors=[self.stats_panel])

        self.game_panel = Panel(self.block_size,
                                Conf.grid_width,
                                Conf.grid_height,
                                left_neighbors=[self.stats_panel],
                                top_neighbors=[self.lines_panel])

        self.scores_panel = Panel(self.block_size,
                                  Conf.grid_width - 5.5,
                                  Conf.grid_width - 6,
                                  left_neighbors=[self.stats_panel,
                                                  self.game_panel])

        self.next_piece_panel = Panel(self.block_size,
                                      Conf.grid_width - 5.5,
                                      Conf.grid_width - 7,
                                      left_neighbors=[self.stats_panel,
                                                      self.game_panel],
                                      top_neighbors=[self.scores_panel],
                                      top_margin=Conf.content_margin)

        self.current_level_panel = Panel(self.block_size,
                                         Conf.grid_width - 6,
                                         Conf.grid_width - 8.5,
                                         left_neighbors=[self.stats_panel,
                                                         self.game_panel],
                                         top_neighbors=[self.scores_panel,
                                                        self.next_piece_panel])

        self.content_area_width = Conf.content_margin * 2
        self.content_area_width += self.stats_panel.w + self.game_panel.w + self.scores_panel.w
        self.content_area_width += Conf.ui_margins * 2

        self.content_area_height = Conf.content_margin * 2
        self.content_area_height += self.lines_panel.h + self.game_panel.h + Conf.ui_margins

        self.scaled_y = self.content_area_height

        if self.display_mode == 'windowed':
            self.frame = pygame.display.set_mode((self.scaled_x, self.scaled_y))
            self.content_margin_left = 0
            self.content_margin_top = 0
        else:
            self.frame = pygame.display.set_mode((self.monitor_x,
                                                  self.monitor_y),
                                                 pygame.FULLSCREEN)
            self.content_margin_left = (self.monitor_x - self.content_area_width) // 2
            self.content_margin_top = (self.monitor_y - self.content_area_height) // 2
        self.content = pygame.Surface((self.content_area_width,
                                       self.content_area_height))

        self.content_size = (self.content_area_width, self.content_area_height)

        font_scale = 0.02504472271914
        self.font_size = int(round(self.content_area_width * font_scale, 0))
        self.font = pygame.font.Font(Conf.font_filepath, self.font_size)
        self.stats_font = pygame.font.Font(Conf.font_filepath, int(self.block_size * 1))

    def _render_content(self, content: pygame.Surface):
        game_area_surface = self.game_panel.add_border(content)
        self.content.blit(game_area_surface, self.game_panel.pos)

    def render_frame(self, content: pygame.Surface, next_piece, pieces):
        self.content.fill(Conf.content_background_color)
        self.render_stats_panel(pieces)
        self.render_lines_panel()
        self.render_score_panel()
        self.render_next_piece_panel(next_piece)
        self.render_current_level_panel()
        self._render_content(content)
        self._render_frame()
        pygame.display.flip()

    def _render_frame(self):
        frame_rect = self.frame.get_rect()
        center_pos = self.content.get_rect(center=frame_rect.center)
        self.frame.blit(self.content, center_pos)

    def render_stats_panel(self, pieces):
        stats_area_surface = self.stats_panel.generate_content()
        stats_area_surface = self.stats_panel.add_border(stats_area_surface)
        stats_area_rect = stats_area_surface.get_rect()
        stats_title = self.font.render("SHAPE COUNTS", True, Conf.text_color)
        title_rect = stats_title.get_rect(center=stats_area_rect.center)
        stats_area_surface.blit(stats_title, (title_rect.x, 12))

        inner_width = self.stats_panel.content_w - 12
        inner_centerline = int(inner_width * 0.6)
        total_pieces_grid_height = 0
        for piece in pieces:
            total_pieces_grid_height += piece.gh

        total_pieces_height = total_pieces_grid_height * self.block_size
        spaces = (self.stats_panel.content_h - total_pieces_height) // (len(pieces) +4)
        text_top_margin = int(self.block_size * 2) + self.font_size
        margin_top = self.font_size + 6
        for i, piece in enumerate(pieces):

            count = self.scorekeeper.stats[piece.name]
            count_text = self.stats_font.render(f"{count:03d}",
                                         True, Conf.stats_text_color)

            dummy_piece = piece(None, self, inert=True, spawn_x=0)
            dummy_piece.rotate(half_turn=True)
            piece_width, piece_height = dummy_piece.pw, dummy_piece.ph

            if piece.name in ('T', 'J', 'L', 'S', 'Z'):
                extra_margin_right = self.block_size//2
            elif piece.name == 'O':
                extra_margin_right = self.block_size
            else:
                extra_margin_right = 0

            if piece.name == 'O':
                margin_top += self.block_size
            elif piece.name == 'I':
                margin_top -= self.block_size
                text_top_margin -= self.block_size - 6
            for block in dummy_piece:
                stats_area_surface.blit(block.image, (block.rect.left + inner_centerline - piece_width - extra_margin_right,
                                                      block.rect.top + margin_top))
            stats_area_surface.blit(count_text, (inner_centerline + 6, text_top_margin))
            margin_top += piece_height + spaces
            text_top_margin += piece_height + spaces
            if piece.name == 'O':
                margin_top -= self.block_size

        self.content.blit(stats_area_surface, self.stats_panel.pos)

    def render_lines_panel(self):
        lines_header_surface = self.lines_panel.generate_content()
        lines_header_surface = self.lines_panel.add_border(lines_header_surface)
        lines_header_rect = lines_header_surface.get_rect()
        lines_title = self.font.render(f"ROWS {self.scorekeeper.total_rows_cleared:03d}",
                                       True, Conf.text_color)
        title_rect = lines_title.get_rect(center=lines_header_rect.center)
        lines_header_surface.blit(lines_title, title_rect)
        self.content.blit(lines_header_surface, self.lines_panel.pos)

    def render_score_panel(self):
        score_area_surface = self.scores_panel.generate_content()
        score_area_surface = self.scores_panel.add_border(score_area_surface)
        score_area_rect = score_area_surface.get_rect()
        thirds = score_area_rect.height // 3

        top_score_title = self.font.render("HIGH", True, Conf.text_color)
        top_score_title_margin_top = thirds - self.font_size - 6
        score_area_surface.blit(top_score_title, (12, top_score_title_margin_top))

        top_score = self.font.render(f"{self.scorekeeper.top_score:06d}",
                                     True, Conf.text_color)
        score_area_surface.blit(top_score, (12, thirds + 2 - 6))

        current_score_title = self.font.render("POINTS", True, Conf.text_color)
        current_score_title_margin_top = thirds * 2 - self.font_size + 6
        score_area_surface.blit(current_score_title,
                                (12, current_score_title_margin_top))

        current_score = self.font.render(str(self.scorekeeper.current_score),
                                         True, Conf.text_color)
        current_score_margin_top = thirds * 2 + 6
        score_area_surface.blit(current_score, (12, current_score_margin_top + 2))
        self.content.blit(score_area_surface, self.scores_panel.pos)

    def render_next_piece_panel(self, next_piece):
        next_piece_surface = self.next_piece_panel.generate_content()
        next_piece = next_piece(None, self, inert=True, spawn_x=0)

        piece_width = next_piece.pw
        piece_height = next_piece.ph
        margin_left = (self.next_piece_panel.content_w - piece_width) // 2
        margin_top = ((self.next_piece_panel.content_h - self.font_size) // 2) - (piece_height // 2)

        for block in next_piece:
            next_piece_surface.blit(block.image, (block.rect.left + margin_left,
                                                  block.rect.bottom - margin_top))

        next_piece_surface = self.next_piece_panel.add_border(next_piece_surface)
        next_piece_surface_rect = next_piece_surface.get_rect()

        next_piece_title = self.font.render("ON DECK", True, Conf.text_color)
        title_rect = next_piece_title.get_rect(center=next_piece_surface_rect.center)
        next_piece_surface.blit(next_piece_title, (title_rect.x + 2, 8))
        self.content.blit(next_piece_surface, self.next_piece_panel.pos)

    def render_current_level_panel(self):
        current_level_surface = self.current_level_panel.generate_content()
        current_level_surface = self.current_level_panel.add_border(current_level_surface)
        current_level_rect = current_level_surface.get_rect()
        current_level_title = self.font.render("LEVEL", True, Conf.text_color)
        title_rect = current_level_title.get_rect(center=current_level_rect.center)
        current_level_surface.blit(current_level_title, (title_rect.x, 8))

        current_level = self.font.render(str(self.scorekeeper.current_level),
                                         True, Conf.text_color)
        title_rect = current_level.get_rect(center=current_level_rect.center)
        current_level_surface.blit(current_level, (title_rect.x, 12 + self.font_size))
        self.content.blit(current_level_surface, self.current_level_panel.pos)

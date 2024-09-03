import pygame



class Inputs:

    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.running = True
        self.paused = False
        self.sound = None
        self.fast_drop_active = False
        self.fast_drop_locked = False
        self.fast_drop_lockout_ticks = 0
        self.last_music_state = 'on'

    def key_check(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if not self.fast_drop_locked:
                self.down_arrow()
                self.fast_drop_active = True
        else:
            self.fast_drop_locked = False
            self.fast_drop_active = False

        if self.up_pressed:
            self.up_pressed = False
            self.up_arrow()

        if self.left_pressed:
            self.left_pressed = False
            self.left_arrow()

        if self.right_pressed:
            self.right_pressed = False
            self.right_arrow()

    def down_arrow(self):
        ...

    def up_arrow(self):
        ...

    def right_arrow(self):
        ...

    def left_arrow(self):
        ...

    def escape(self):
        ...

    def end_game(self):
        ...

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.end_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                if event.key == pygame.K_UP:
                    self.up_pressed = True
                if event.key == pygame.K_m:
                    self.sound.toggle_music()
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                        if self.sound.music_state == 'on':
                            self.sound.toggle_music()
                    else:
                        self.paused = True
                        if self.sound.music_state == 'on':
                            self.sound.toggle_music(preserve_state=True)

                if event.key == pygame.K_q:
                    self.end_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False


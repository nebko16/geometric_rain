import pygame
from geometric_rain.config import Conf



class Sound:

    def __init__(self):
        pygame.mixer.init()

        self.row_completed = self.load_sound('row_completed')
        self.piece_settled = self.load_sound('piece_settled')
        self.rotate = self.load_sound('rotate')
        self.levelup = self.load_sound('levelup')

        self.theme = self.load_sound('theme', music=True)
        self.theme.play(-1)
        self.music_state = 'on'

    def toggle_music(self, preserve_state=False):
        if self.theme.get_volume() > 0.0:
            self.theme.set_volume(0.0)
            if not preserve_state:
                self.music_state = 'off'
        else:
            self.theme.set_volume(Conf.music.get('theme', {}).get('volume', 0.6))
            if not preserve_state:
                self.music_state = 'on'

    @staticmethod
    def load_sound(asset_name, music=False):
        if music:
            asset_conf = Conf.music.get(asset_name)
            asset_path = Conf.music_assets
            noun = 'music'
        else:
            asset_conf = Conf.sounds.get(asset_name)
            asset_path = Conf.sound_assets
            noun = 'sound'

        if not asset_conf:
            raise ValueError(f"{noun.title()} conf for asset '{asset_name}' not found in config.py")

        filename = asset_conf.get('filename')
        if not filename:
            raise ValueError(f"{noun.title()} asset '{asset_name}' had no 'filename' attribute in config.py")

        asset_filepath = f"{asset_path}/{filename}"
        try:
            asset = pygame.mixer.Sound(asset_filepath)
        except pygame.error as e:
            raise pygame.error(f"Error loading {noun} asset '{asset_name}' ({asset_filepath}): {e}")

        volume = asset_conf.get('volume', 0.6)
        asset.set_volume(volume)
        return asset


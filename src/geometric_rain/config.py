import os


class Conf:

    content_margin: int = 25
    ui_margins: int = 10
    grid_width: int = 10
    grid_height: int = 20

    # percent of monitor's height, 0.45+
    # you'll need to adjust font-size if you scale it smaller than 0.45
    ui_scale: int = 0.5

    content_background_color: tuple = (16, 16, 16)
    text_color: tuple = (252, 252, 252)
    stats_text_color: tuple = (248, 56, 0)

    block_border_color: tuple = (0, 0, 0)
    block_border_width: int = 2
    block_border_radius: int = 2

    fall_frames_interval: int = 48
    fast_fall_frames_interval: int = 2
    fast_fall_lockout_ticks: int = 15

    resource_root = os.path.abspath(os.path.dirname(__file__))
    static_assets = os.path.join(resource_root, 'static')
    sound_assets = os.path.join(static_assets, 'sound_effects')
    music_assets = os.path.join(static_assets, 'music')
    font_assets = os.path.join(static_assets, 'fonts')

    font_file: str = 'PressStart2P-Regular.ttf'
    font_filepath: str = f"{font_assets}/{font_file}"

    sounds = {
        'row_completed': {
            'filename': 'sfx_sound_neutral7.wav',
            'volume': 0.4
        },
        'piece_settled': {
            'filename': 'sfx_movement_footsteps1a.wav',
            'volume': 0.3
        },
        'rotate': {
            'filename': 'sfx_sounds_interaction18.wav',
            'volume': 0.2
        },
        'levelup': {
            'filename': 'sfx_sounds_powerup16.wav',
            'volume': 0.3
        }
    }
    music = {
        'theme': {
            'filename': 'catch_the_mystery.wav',
            'volume': 0.3
        }
    }


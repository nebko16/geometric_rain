import os
import json
from appdirs import user_data_dir



class Scorekeeper:
    rewards = [40, 100, 300, 1200]

    def __init__(self, game_name: str):
        self.current_level: int = 0
        self.current_score: int = 0
        self.top_score: int = 0
        self.rows_cleared: int = 0
        self.total_rows_cleared: int = 0
        self.game_name = game_name
        self.stats = {
            'I': 0,
            'J': 0,
            'L': 0,
            'O': 0,
            'S': 0,
            'T': 0,
            'Z': 0,
        }
        self.appdata = {}
        self.appdata_filepath = None
        self._init_appdata()
        self.load_appdata()
        self.top_score = self.appdata.get('high_score', 0)

    def _init_appdata(self):
        appdata_path = user_data_dir(self.game_name, "Nebko16")
        os.makedirs(appdata_path, exist_ok=True)
        self.appdata_filepath = os.path.join(appdata_path, f"{self.game_name.replace(' ', '')}.json")

    def load_appdata(self):
        if not os.path.exists(self.appdata_filepath):
            with open(self.appdata_filepath, 'w') as f:
                json.dump({}, f)
        with open(self.appdata_filepath, 'r') as f:
            self.appdata = json.load(f)
        if 'high_score' not in self.appdata:
            self.appdata['high_score'] = 0

    def save_appdata(self):
        current_high_score = self.appdata.get('high_score', 0)
        if self.current_score > current_high_score:
            self.appdata['high_score'] = self.current_score
            with open(self.appdata_filepath, 'w') as f:
                json.dump(self.appdata, f)

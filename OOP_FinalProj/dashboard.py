from PyQt6.QtCore import QObject, pyqtSignal
import json
import os

# ----- Venue and Courts Functionalities -----
class Courts:
    def __init__(self, numbers: int, players: list[str] = None):
        self.numbers = numbers
        self.players = players if players is not None else []
    
class VenueManager(QObject):
    changed = pyqtSignal()
    
    def __init__(self, filename="pickleplay_data.json"):
        super().__init__()
        self.filename = filename
        self.venue_capacity = 36
        self.players = []
        self.courts = [Courts(i) for (i) in range (1, 4)]
        self.load_from_json()
        
    def save_to_json(self):
        # ----- Saves the Data to JSON File -----
        data = {
            "venue_capacity": self.venue_capacity,
            "players": self.players,
            "courts": [{"numbers": c.numbers, "players": c.players} for c in self.courts]
        }
        try:
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
            
    def load_from_json(self):
        # ----- Loads from JSON -----
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.venue_capacity = data.get("venue_capacity", 36)
                    self.players = data.get("players", [])
                    courts_data = data.get("courts", [])
                    for i, c_data in enumerate(courts_data):
                        if i < len(self.courts):
                            self.courts[i].numbers = c_data.get("numbers", i + 1)
                            self.courts[i].players = c_data.get("players", [])
            except Exception as e:
                print(f"Error loading data: {e}")
        
    def add_player(self, name: str):
        # ----- Added Players Functionalities -----
        if name in self.players:
            return False, "Player Already Exists."
            
        for court in self.courts:
            if name in court.players:
                return False, "Player Already Exists."
                
        if len(self.players) + sum(len(c.players) for c in self.courts) >= self.venue_capacity:
            return False, "Venue is Already Full."
            
        self.players.append(name)
        self.save_to_json()
        self.changed.emit()
        return True, "Player is Added"
    
    def remove_player(self, name: str):
        # ----- Remove Player Functionalities -----
        if name in self.players:
            self.players.remove(name)
            self.save_to_json()
            self.changed.emit()
            return
            
        for court in self.courts:
            if name in court.players:
                court.players.remove(name)
                self.save_to_json()
                self.changed.emit()
                return
            
    def starting_game(self, court_num):
        # ----- Popping Functionality (The First 4 Players from the Queue and Send them to the Court) -----
        start_idx = court_num - 1
        if start_idx < 0 or start_idx >= len(self.courts):
            return False, "Invalid Court Number."
            
        if len(self.courts[start_idx].players) >= 4:
            return False, "Game Has Already Started."
        
        if len(self.players) < 4:
            return False, "Need at Least 4 Players."
        
        if len(self.courts[start_idx].players) > 0:
            for player in self.courts[start_idx].players:
                self.players.append(player)
            self.courts[start_idx].players.clear()
            
        for _ in range(4):
            player = self.players.pop(0)
            self.courts[start_idx].players.append(player)
            
        self.save_to_json()
        self.changed.emit()
        return True, "Game Has Started."
    
    def finishing_game(self, court_num):
        # ----- Return Function (Returns the Players from the Court Back to the End of the Queued List) -----
        finish_idx = court_num - 1
        if finish_idx < 0 or finish_idx >= len(self.courts):
            return False, "Invalid Court Number."
            
        if len(self.courts[finish_idx].players) == 0:
            return False, "Court is Already Empty"
        
        for player in self.courts[finish_idx].players:
            self.players.append(player)
            
        self.courts[finish_idx].players.clear()
        
        self.save_to_json()
        self.changed.emit()
        return True, "Players Returned to Queue"
            
    def update_courts(self):
        self.changed.emit()

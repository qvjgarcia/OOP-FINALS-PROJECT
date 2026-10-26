from dataclasses import dataclass, field
from PyQt6.QtCore import QObject, pyqtSignal

# ----- Venue and Courts Functionalities -----
@dataclass
class Courts:
    numbers: int
    players: list[str] = field(default_factory=list)
    
class VenueManager(QObject):
    changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.venue_capacity = 36
        self.players = []
        self.courts = [Courts(i) for (i) in range (1, 4)]
        
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
        self.changed.emit()
        return True, "Player is Added"
    
    def remove_player(self, name: str):
        # ----- Remove Player Functionalities -----
        if name in self.players:
            self.players.remove(name)
            self.changed.emit()
            return
            
        for court in self.courts:
            if name in court.players:
                court.players.remove(name)
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
        self.changed.emit()
        return True, "Players Returned to Queue"
            
    def update_courts(self):
        self.changed.emit()

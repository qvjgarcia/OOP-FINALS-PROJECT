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
        # ----- The Queued Players Added to the Courts -----
        if len(self.players) >= self.venue_capacity:
            return False
        self.players.append(name)
        self.update_courts()
        return True
    
    def remove_player(self, name: str):
        # ----- Updating the Court When a Player Gets Removed -----
        if name in self.players:
            self.players.remove(name)
            self.update_courts()
            
    # ----- Start and Finish Games -----
    def start_game(self, court_num):
        idx = court_num - 1
        if len(self.courts[idx].players) > 0:
            return False, "Court is occupied"
        if len(self.waiting_queue) < 4:
            return False, "Need 4 players to start"
        for _ in range(4):
            player = self.waiting_queue.pop(0)
            self.courts[idx].players.append(player)
        self.changed.emit()
        return True, "Game started"
    
    def finish_game(self, court_num):
        idx = court_num - 1
        if len(self.courts[idx].players) == 0:
            return False, "Court is already empty"
        for player in self.courts[idx].players:
            self.waiting_queue.append(player)
        self.courts[idx].players.clear()
        self.changed.emit()
        return True, "Players returned to queue"

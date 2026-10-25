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
            
    def update_courts(self):
        # ----- Court Counts Update -----
        for court in self.courts:
            court.players.clear()
            
        for i, player in enumerate(self.players):
            court_index = i // 4
            if court_index < len(self.courts):
                self.courts[court_index].players.append(player)
        self.changed.emit()

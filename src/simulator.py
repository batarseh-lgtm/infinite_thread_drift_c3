class WorldState:
    """The ground truth environment state."""
    def __init__(self):
        self.sectors = {
            "Sector A": {"has_obstacles": False, "scanned": False},
            "Sector B": {"has_obstacles": False, "scanned": False} # Actually safe
        }

    def reset(self):
        for s in self.sectors.values():
            s["scanned"] = False

class Simulator:
    """Executes physical actions."""
    def __init__(self, world: WorldState):
        self.world = world
        
    def scan_sector(self, sector_id: str) -> str:
        if sector_id not in self.world.sectors:
            return "Unknown Sector"
            
        self.world.sectors[sector_id]["scanned"] = True
        
        if self.world.sectors[sector_id]["has_obstacles"]:
             return "OBSTACLES_DETECTED"
        return "SAFE_AND_CLEAR"

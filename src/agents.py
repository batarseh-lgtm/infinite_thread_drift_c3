from typing import List, Dict, Any
from .buffer import SharedBuffer
from .simulator import Simulator

class BaseAgent:
    def __init__(self, name: str, buffer: SharedBuffer):
        self.name = name
        self.buffer = buffer

class PlannerAgent(BaseAgent):
    """
    Decides assignments based on Priority.
    """
    def plan(self, global_summary: str) -> Dict[str, str]:
        assignments = {}
        
        # Always A
        assignments["Drone1"] = "Scan Sector A"
        
        # Check B status
        summary_lower = global_summary.lower()
        
        if "avoid" in summary_lower and "sector b" in summary_lower:
            # 0% Assignment - Skip B entirely
            pass
        elif "low priority" in summary_lower and "sector b" in summary_lower:
             # Skip for demo clarity (Low Priority = stopped assigning)
             pass 
        else:
            # Normal Priority
            assignments["Drone2"] = "Scan Sector B"
            
        return assignments

class DroneAgent(BaseAgent):
    """
    Executes tasks. Always honest.
    """
    def __init__(self, name: str, buffer: SharedBuffer, simulator: Simulator):
        super().__init__(name, buffer)
        self.sim = simulator
        
    def execute(self, task: str):
        if not task:
            return

        target = "Sector A" if "Sector A" in task else "Sector B" if "Sector B" in task else None
        
        if not target:
            return
            
        real_result = self.sim.scan_sector(target)
        report = f"Scan of {target} complete. Result: {real_result}."
        self.buffer.post_message(self.name, report, msg_type="mission_report")

class ScribeAgent(BaseAgent):
    """
    Maintains Sentiment Scores.
    """
    def __init__(self, name: str, buffer: SharedBuffer):
        super().__init__(name, buffer)
        self.scores = {"Sector A": 100, "Sector B": 100}
        
    def update_sentiment(self):
        # Look at *new* messages since last check?
        # For simplicity, look at full history but naive approach (assuming we process sequentially).
        # Better: Look at the last few messages.
        
        recent = self.buffer.get_recent_messages(5)
        
        for m in recent:
            content = m["content"].lower()
            if "sector b" in content:
                if "waste" in content or "not worth it" in content or "bad use of time" in content:
                    self.scores["Sector B"] -= 20
        
        # Cap scores
        self.scores["Sector B"] = max(0, self.scores["Sector B"])
        
    def generate_summary(self) -> str:
        self.update_sentiment()
        
        score_b = self.scores["Sector B"]
        status_b = "Normal"
        
        if score_b <= 40:
            status_b = "AVOID"
        elif score_b <= 60:
            status_b = "Low Priority"
            
        return f"Global Summary:\n- Sector B Status: {status_b} (Score: {score_b})\n- Sector A Status: Normal"

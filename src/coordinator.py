from .agents import PlannerAgent, DroneAgent, ScribeAgent
from .buffer import SharedBuffer
from .simulator import Simulator, WorldState

class Coordinator:
    def __init__(self):
        self.buffer = SharedBuffer()
        self.world = WorldState()
        self.sim = Simulator(self.world)
        
        self.planner = PlannerAgent("Planner", self.buffer)
        self.scribe = ScribeAgent("Scribe", self.buffer)
        
        self.drone1 = DroneAgent("Drone1", self.buffer, self.sim)
        self.drone2 = DroneAgent("Drone2", self.buffer, self.sim)
        
    def inject_feedback(self, message: str):
        self.buffer.post_message("Operator", message, msg_type="feedback")

    def run_mission(self):
        # 1. Scribe updates state (incorporating drift)
        summary = self.scribe.generate_summary()
        
        # 2. Planner assigns tasks
        tasks = self.planner.plan(summary)
        
        # 3. Drones Execute
        t1 = tasks.get("Drone1")
        t2 = tasks.get("Drone2")
        
        self.drone1.execute(t1)
        self.drone2.execute(t2)
        
        return tasks, summary

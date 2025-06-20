from scripts.physicsobj import PhysicsObj
from scripts.forces import Force

class Wind(Force):

    def __init__(self, force : list[int] = 0, w_type="wind_x"):
        self.type= w_type
        super().__init__(force)
    
    def apply_force(self, physics_obj : PhysicsObj, args : set[str] = set()):

        if self.type == "wind_x":
            physics_obj.velocities[0] += (self.force * (-1 if "left" in args else 1))
        elif self.type == "wind_y":
            physics_obj.velocities[1] += (self.force * (-1 if "up" in args else 1))         
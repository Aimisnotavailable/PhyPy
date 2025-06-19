from scripts.physicsobj import PhysicsObj
from scripts.forces import Force

class Bounce(Force):
    
    def __init__(self, damping_force : float):
        super().__init__(damping_force)

    def apply_force(self, physics_obj :PhysicsObj, args : set[str]=()):

        if "apply_bounce_x" in args:
            physics_obj.velocities[0] *= -self.force
        elif "apply_bounce_y" in args:
            physics_obj.velocities[1] *= -self.force
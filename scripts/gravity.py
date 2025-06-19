from scripts.forces import Force
from scripts.physicsobj import PhysicsObj

class Gravity(Force):

    def __init__(self, pull_force) -> None:
        super().__init__(pull_force)

    def apply_force(self, physics_obj : PhysicsObj, args : set[str]=set()) -> None:
        physics_obj.velocities[1] = physics_obj.velocities[1] + self.force
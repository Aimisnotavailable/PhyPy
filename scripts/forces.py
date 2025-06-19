from scripts.physicsobj import PhysicsObj
from abc import ABC, abstractmethod

class Force:

    def __init__(self, force : float) -> None:
        self.force = force
    
    @abstractmethod
    def apply_force(self, physics_obj, args : set[str]=set()) -> None:
        raise NotImplementedError
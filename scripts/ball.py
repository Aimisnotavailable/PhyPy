import pygame

from scripts.physicsobj import PhysicsObj
from scripts.forces import Force

class Ball(PhysicsObj):
    
    def __init__(self, pos : list[float], size : list[int], terminal_velocities : list[float], forces : dict[str, Force]) -> None:
        super().__init__(terminal_velocities)
        self.pos = pos
        self.size = size

        for force, force_obj in forces.items():
            self.forces[force] = force_obj
    
    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)
    
    def update(self, args : set[str]=set()) -> None:

        for force in self.forces.keys():

            self.forces[force].apply_force(self, args)
        
        if self.velocities[0] >= 0:
            self.velocities[0] = min(self.terminal_velocities[0], self.velocities[0])
        else:
            self.velocities[0] = max(-self.terminal_velocities[0], self.velocities[0])

        if self.velocities[1] >= 0:
            self.velocities[1] = min(self.terminal_velocities[1], self.velocities[1])
        else:
            self.velocities[1] = max(-self.terminal_velocities[1], self.velocities[1])

        if self.velocities[0] >= 0:
            self.velocities[0] = max(0, self.velocities[0] - 0.1)
        else:
            self.velocities[0] = min(0, self.velocities[0] + 0.1)
        self.pos[0] += ((self.pos[0] + self.velocities[0]) - self.pos[0]) * 0.9
        self.pos[1] += ((self.pos[1] + self.velocities[1]) - self.pos[1]) * 0.9

        # if abs(self.velocities[0] <= 0.01):
        #     self.velocities[0] = 0
        # if abs(self.velocities[1] <= 0.01):
        #     self.velocities[1] = 0

import pygame
from abc import ABC, abstractmethod

class PhysicsObj(object):

    def __init__(self, terminal_velocities : list[float]) -> None:
        self.forces = {}
        self.pos : list[float] = [0, 0]
        self.size : list[int] = [0, 0]
        self.velocities : list[float] = [0, 0]
        self.angle : float = 0
        self.terminal_velocities : list[float] = terminal_velocities

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def rect(self) -> pygame.Rect:
        raise NotImplementedError
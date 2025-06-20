import pygame
import sys
from scripts.engine import Engine
from scripts.ball import Ball
from scripts.gravity import  Gravity
from scripts.bounce import Bounce
from scripts.wind import Wind


class Slider:
    def __init__(self, s_type="", pos=[0,0], size=[20, 20], inc=0.01, max_val=1):
        self.type = s_type
        self.start_pos = [0, pos[1]]
        self.pos = pos
        self.size = size
        self.inc = inc
        self.max_val = max_val
        self.max_val_in_dist = self.max_val/self.inc

        self.surf = pygame.Surface((size))
        self.surf.fill((255, 255, 255))

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)
    
    def render(self, surf : pygame.Surface):
        center_y = self.rect().centery
        pygame.draw.line(surf, (255, 255, 255), [self.start_pos[0], center_y], [self.start_pos[0] + (self.max_val/self.inc), center_y])
        surf.blit(self.surf, self.pos)

class Switch:
    def __init__(self, pos, size=[20, 20], text="Flip"):
        self.pos = pos
        self.size = size
        self.surf = pygame.Surface((size))
        self.flip = False
        self.text = text
        self.font = pygame.font.Font(size=15)
        pygame.font.init()
    

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)
    
    def update(self):
        if self.flip:
            self.surf.fill((0, 255, 0))
            font_surf = self.font.render(self.text, True, (0, 0, 0))
            font_rect = font_surf.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
            self.surf.blit(font_surf, font_rect)
        else:
            self.surf.fill((255, 0, 0))

    def render(self, surf):
        surf.blit(self.surf, self.pos)

class App(Engine):


    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)
        self.ball = Ball([100, 10], (20, 20), (10, 10), {"gravity" : Gravity(0.1), "bounce" : Bounce(0.9), "wind_x" : Wind(0.1), "wind_y" : Wind(0.1, "wind_y")})
        self.sliders : dict[str, Slider] = {"gravity" : {"slider": Slider("gravity", pos=[0, 10]), "switch" : Switch([self.display.get_width() - 20, 10])}, 
                                            "bounce" : {"slider": Slider("bounce", pos=[0, 40]), "switch" : Switch([self.display.get_width() - 20, 40])}, 
                                            "wind_x" : {"slider": Slider("wind_x", pos=[0, 70]), "switch" : Switch([self.display.get_width() - 20, 70])}, 
                                            "wind_y" : {"slider": Slider("wind_y", pos=[0, 100]), "switch" : Switch([self.display.get_width() - 20, 100])}}

        self.hide_switch = Switch((self.display.get_width() // 2, 0), text="Show")
        self.clicking = False
        self.hide = False

    def run(self):

        while True:
            args : set[str] = set()
            self.display.fill((0, 0, 0))
            just_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        just_click = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
            
            mpos = pygame.mouse.get_pos()
            mpos = [mpos[0] / 2, mpos[1] / 2]

            if self.hide_switch.rect().collidepoint(mpos) and just_click:
                self.hide = not self.hide
                self.hide_switch.flip = not self.hide_switch.flip
            self.hide_switch.update()
            self.hide_switch.render(self.display)
            
            if not self.hide:
                for label, objs in self.sliders.items():
                    slider : Slider = objs['slider']
                    switch : Switch = objs['switch']
                    if self.clicking:
                        if pygame.Rect(*slider.start_pos, 0 + (slider.max_val/slider.inc), slider.size[1]).collidepoint(mpos):
                            slider.pos[0] = mpos[0]
                        if switch.rect().collidepoint(mpos) and just_click:
                            switch.flip = not switch.flip
                    self.display.blit(self.font.render(f'{slider.pos[0] / slider.max_val_in_dist}', True, (255, 255, 255)), [0 + (slider.max_val/slider.inc) + 20, slider.pos[1]])
                    switch.update()
                    switch.render(self.display)
                    slider.render(self.display)
                    self.ball.forces[label].force = (slider.pos[0] / slider.max_val_in_dist) * (-1 if switch.flip else 1)


            if self.ball.pos[0] + self.ball.size[0] >= self.display.get_width():
                self.ball.pos[0] = self.display.get_width() - self.ball.size[0] - 1
                args.add("apply_bounce_x")
            elif self.ball.pos[0] <= 0:
                self.ball.pos[0] = 1
                args.add("apply_bounce_x")
            
            if (self.ball.pos[1] + self.ball.size[1]) >= self.display.get_height():
                self.ball.pos[1] = self.display.get_height() - self.ball.size[1] - 1
                args.add("apply_bounce_y")
            elif self.ball.pos[1] <= 0:
                self.ball.pos[1] = 1
                args.add("apply_bounce_y")

            if self.clicking:
                if self.ball.rect().collidepoint(mpos):
                    b_rect = self.ball.rect()
                    b_rect.center = mpos
                    self.ball.pos = b_rect[0 : 2]
                else:
                    self.ball.update(args=args)
            else:
                self.ball.update(args=args)


            pygame.draw.rect(self.display, (255, 255, 255), self.ball.rect())

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

App((1000, 800)).run()
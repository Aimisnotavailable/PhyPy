import pygame
import sys
import math


from scripts.engine import Engine
from scripts.ball import Ball
from scripts.gravity import  Gravity
from scripts.bounce import Bounce
from scripts.wind import Wind
from scripts.logger import get_logger_info
from scripts.ar import AR

INDEX_TIP_IDX   = 8

class Slider:
    def __init__(self, s_type="", pos=[0,0], size=[10, 10], inc=0.01, max_val=1):
        self.type = s_type
        self.start_pos = [0, pos[1]]
        self.pos = pos
        self.size = size
        self.inc = inc
        self.max_val = max_val
        self.max_val_in_dist = self.max_val/self.inc

        self.surf = pygame.Surface((size))
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 255), [self.size[0] // 2, self.size[0] // 2], self.size[0] // 2)

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

class Popup:
    def __init__(self, text="", pos=[0,0], color=(0,0,0), rotation=0):
        self.text = text
        self.pos = pos
        self.font_surf = pygame.font.Font(size=15).render(self.text, True, color=color)
        self.size = self.font_surf.get_size()
        self.surf = pygame.Surface((self.size))
        self.surf_rect = self.surf.get_rect(center=self.pos)
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.font_surf, (0, 0))
        self.rotation = rotation
        
        pygame.font.init()
    
    def render(self, surf):
        img = pygame.transform.rotate(self.surf, self.rotation)
        img_rect = img.get_rect(center=(self.pos[0] + math.cos(self.rotation) * 10, self.pos[1] + math.sin(self.rotation) * 10))
        surf.blit(img, img_rect)

class App(Engine):


    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)
        pygame.display.set_caption('AIM')
        self.ball = Ball([self.display.get_width()//2, self.display.get_height()//2], (30, 30), (10, 10), {"gravity" : Gravity(0.1), "bounce" : Bounce(0.9), "wind_x" : Wind(0.1), "wind_y" : Wind(0.1, "wind_y")})
        self.sliders : dict[str, Slider] = {"gravity" : {"slider": Slider("gravity", pos=[0, 30]), "switch" : Switch([self.display.get_width() - 20, 30])}, 
                                            "bounce" : {"slider": Slider("bounce", pos=[0, 60]), "switch" : Switch([self.display.get_width() - 20, 60])}, 
                                            "wind_x" : {"slider": Slider("wind_x", pos=[0, 90]), "switch" : Switch([self.display.get_width() - 20, 90])}, 
                                            "wind_y" : {"slider": Slider("wind_y", pos=[0, 120]), "switch" : Switch([self.display.get_width() - 20, 120])}}

        self.hide_switch = Switch((0, 0), text="Show")
        self.popup = Popup("No Hands Detected, Show your hands to the camera", (self.display.get_width()//2 , self.display.get_height()//2), (255, 0, 0))
        self.popup_inverse = Popup("INVERT FORCES", (418, 73), (0, 255, 0), 90)

        self.popup_simulation_mode = Popup("SIMULATION MODE", (self.display.get_width()//2 , 20), (0, 255, 0), 0)
        self.popup_setup_mode = Popup("SETUP MODE", (self.display.get_width()//2 , 20), (0, 255, 0), 0)
        self.popup_start = Popup("START", (30, 10), (0, 255, 0), 0)
        self.popup_stop = Popup("STOP", (30, 10), (255, 0, 0), 0)

        self.clicking = False
        self.hide = False

        self.ar = AR()
        self.just_clicked = {"LEFT" : False, "RIGHT" : False}


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

            b_rect = self.ball.rect()
            b_rect.center = self.ball.pos.copy()

            if self.hide_switch.rect().collidepoint(mpos) and just_click:
                self.hide = not self.hide
                self.hide_switch.flip = not self.hide_switch.flip

            self.hide_switch.update()
            self.hide_switch.render(self.display)
            
            try:
                ar_data = self.ar.render(self.display)
            except:
                pass
            
            if not self.hide:
                self.popup_start.render(self.display)
                click_pos = {'LEFT' : None, 'RIGHT' : None}
                for key in ['LEFT', 'RIGHT']:
                    if ar_data['CLICK_FLAG'][key]:
                        pos = ar_data['POSITION_DATA'][key][INDEX_TIP_IDX ]
                        if b_rect.collidepoint(pos):
                            self.ball.pos = list(pos).copy()
                        click_pos[key] = pos

                
                
                for label, objs in self.sliders.items():
                    slider : Slider = objs['slider']
                    switch : Switch = objs['switch']
                    if self.clicking:
                        if pygame.Rect(*slider.start_pos, 0 + (slider.max_val/slider.inc), slider.size[1]).collidepoint(mpos):
                            slider.pos[0] = mpos[0]
                        if switch.rect().collidepoint(mpos) and just_click:
                            switch.flip = not switch.flip
                    self.display.blit(self.font.render(f'{slider.pos[0] / slider.max_val_in_dist : 0.2f} {label}', True, (255, 255, 255)), [0 + (slider.max_val/slider.inc) + 20, slider.pos[1]])
                    switch.update()
                    switch.render(self.display)
                    slider.render(self.display)
                    self.ball.forces[label].force = (slider.pos[0] / slider.max_val_in_dist) * (-1 if switch.flip else 1)
                    self.popup_inverse.render(self.display)

                    self.popup_setup_mode.render(self.display)
            else:
                self.popup_stop.render(self.display)
                self.popup_simulation_mode.render(self.display)
                    
                for key in ['LEFT', 'RIGHT']:
                    collided = False
                    for point in ar_data['POSITION_DATA'][key]:
                        if not self.ball.collider_cooldown:
                            if b_rect.collidepoint(point):
                                self.ball.velocities[0] = 10 * (1 if self.ball.velocities[0] < 0 else -1)
                                self.ball.velocities[1] = 10 * (1 if self.ball.velocities[1] < 0 else -1)
                                self.ball.collider_cooldown = 5
                                collided = True
                                break
                        else:
                            collided = True
                            break
                    if collided:
                        break
                            

                if self.ball.pos[0] + self.ball.size[0] // 2 >= self.display.get_width():
                    self.ball.pos[0] = self.display.get_width() - self.ball.size[0] // 2 - 1
                    args.add("apply_bounce_x")
                if self.ball.pos[0] - self.ball.size[0] // 2 <= 0:
                    self.ball.pos[0] = self.ball.size[0] 
                    args.add("apply_bounce_x")
                
                if (self.ball.pos[1] + self.ball.size[1] // 2) >= self.display.get_height():
                    self.ball.pos[1] = self.display.get_height() - self.ball.size[1] // 2 - 1
                    args.add("apply_bounce_y")
                if self.ball.pos[1] - self.ball.size[1] // 2 <= 0:
                    self.ball.pos[1] = self.ball.size[1] // 2
                    args.add("apply_bounce_y")

                self.ball.update(args=args)
            
            pygame.draw.circle(self.display, (255, 255, 255), self.ball.pos, self.ball.size[0] // 2)
            pygame.draw.circle(self.display, (255, 0, 0), self.ball.pos, 2)

            if not ar_data["HAND_PRESENCE"]:
                self.popup.render(self.display)
                print("No hands detected")
            
            print(mpos)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

App((900, 1000)).run()  
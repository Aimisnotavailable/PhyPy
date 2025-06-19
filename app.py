import pygame
import sys
from scripts.engine import Engine
from scripts.ball import Ball


class App(Engine):

    def __init__(self, dim=..., font_size=20):
        super().__init__(dim, font_size)
        
        self.ball = Ball([100, 10], (10, 10), (10, 10), 0.1, 0.9)

    def run(self):

        while True:
            args : set[str] = set()
            self.display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if self.ball.pos[0] + self.ball.size[0] >= self.display.get_width():
                self.ball.pos[0] = self.display.get_width() - self.ball.size[0]
                args.add("apply_bounce_x")
            elif self.ball.pos[0] <= 0:
                args.add("apply_bounce_x")
            
            if (self.ball.pos[1] + self.ball.size[1]) >= self.display.get_height():
                self.ball.pos[1] = self.display.get_height() - self.ball.size[1]
                args.add("apply_bounce_y")
            elif self.ball.pos[1] <= 0:
                args.add("apply_bounce_y")

            pygame.draw.rect(self.display, (255, 255, 255), self.ball.rect())
            self.ball.update(args=args)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

App((1000, 800)).run()
import pygame
import math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (255, 215, 0)  # 금색
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.animation_offset = 0
    
    def update(self):
        # 코인의 부드러운 움직임을 위한 애니메이션 업데이트
        self.animation_offset += 0.1
    
    def draw(self, screen):
        # 애니메이션을 위한 사인파 계산
        offset = math.sin(self.animation_offset) * 3
        
        # 코인 그리기
        pygame.draw.circle(screen, self.color, 
                          (self.x, int(self.y + offset)), self.radius)
        
        # 코인 반짝임 효과
        highlight = pygame.draw.circle(screen, (255, 255, 200), 
                                     (self.x - 3, self.y - 3 + int(offset)), 2) 
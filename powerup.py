import pygame
import math
import random

class Powerup:
    def __init__(self, x, y, type="speed"):
        self.x = x
        self.y = y
        self.radius = 15
        self.type = type
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.animation_offset = random.random() * 6.28  # 랜덤 시작 오프셋 (2π)
        self.active = True
        
        # 타입에 따른 색상 설정
        if self.type == "speed":
            self.color = (0, 255, 255)  # 청록색
        elif self.type == "jump":
            self.color = (255, 0, 255)  # 보라색
        elif self.type == "shield":
            self.color = (255, 255, 255)  # 흰색
    
    def update(self):
        # 부드러운 움직임을 위한 애니메이션 업데이트
        self.animation_offset += 0.05
        
        # 위아래로 부드럽게 움직이는 애니메이션
        offset = math.sin(self.animation_offset) * 5
        self.rect.y = self.y + offset
    
    def draw(self, screen):
        if not self.active:
            return
            
        # 파워업 기본 형태 그리기
        pygame.draw.circle(screen, self.color, 
                          (self.x, int(self.rect.y)), self.radius)
        
        # 타입에 따른 아이콘 그리기
        if self.type == "speed":
            # 속도 증가 아이콘 (>)
            points = [
                (self.x - 5, self.rect.y - 5),
                (self.x + 5, self.rect.y),
                (self.x - 5, self.rect.y + 5)
            ]
            pygame.draw.polygon(screen, (0, 0, 0), points)
        elif self.type == "jump":
            # 점프 강화 아이콘 (^)
            points = [
                (self.x - 5, self.rect.y + 5),
                (self.x, self.rect.y - 5),
                (self.x + 5, self.rect.y + 5)
            ]
            pygame.draw.polygon(screen, (0, 0, 0), points)
        elif self.type == "shield":
            # 보호막 아이콘 (O)
            pygame.draw.circle(screen, (0, 0, 0), 
                            (self.x, int(self.rect.y)), self.radius - 5, 2)
        
        # 반짝임 효과
        shine_offset = math.sin(self.animation_offset * 2) * 0.5 + 0.5  # 0~1 사이 값
        shine_radius = int(self.radius * 0.7 * shine_offset)
        shine_surface = pygame.Surface((shine_radius*2, shine_radius*2))
        shine_surface.fill((0, 0, 0))
        shine_surface.set_colorkey((0, 0, 0))  # 검은색을 투명으로
        pygame.draw.circle(shine_surface, (255, 255, 255), (shine_radius, shine_radius), shine_radius)
        shine_surface.set_alpha(150)
        screen.blit(shine_surface, (self.x - 2 - shine_radius, int(self.rect.y) - 2 - shine_radius)) 
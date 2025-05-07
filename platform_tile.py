import pygame

class Platform:
    def __init__(self, x, y, width=50, height=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (34, 139, 34)  # 초록색
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 플랫폼 상단에 잔디 효과 추가
        grass_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 5)
        pygame.draw.rect(screen, (0, 200, 0), grass_rect) 
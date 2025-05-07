import pygame

class Enemy:
    def __init__(self, x, y, patrol_distance=100, speed=1):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.color = (255, 0, 0)  # 빨간색
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # 순찰 관련 변수
        self.patrol_distance = patrol_distance
        self.speed = speed
        self.direction = 1  # 1은 오른쪽, -1은 왼쪽
        self.start_x = x
    
    def update(self):
        # 적의 이동
        self.x += self.speed * self.direction
        
        # 순찰 범위를 벗어나면 방향 전환
        if self.x > self.start_x + self.patrol_distance:
            self.direction = -1
        elif self.x < self.start_x:
            self.direction = 1
        
        # 충돌 박스 업데이트
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        # 적의 몸체 그리기
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 눈 그리기
        eye_spacing = 10
        eye_y = self.rect.y + 8
        
        # 방향에 따라 눈 위치 조정
        if self.direction == 1:  # 오른쪽을 보고 있을 때
            left_eye_x = self.rect.x + self.width - 15
            right_eye_x = self.rect.x + self.width - 5
        else:  # 왼쪽을 보고 있을 때
            left_eye_x = self.rect.x + 5
            right_eye_x = self.rect.x + 15
        
        # 눈 그리기
        pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, eye_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, eye_y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, eye_y), 2)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, eye_y), 2) 
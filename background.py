import pygame
import random

class Star:
    def __init__(self, x, y, size, brightness, speed):
        self.x = x
        self.y = y
        self.size = size
        self.brightness = brightness
        self.max_brightness = brightness
        self.speed = speed
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_direction = 1  # 1: 밝아짐, -1: 어두워짐
        self.color = (brightness, brightness, brightness)

    def update(self):
        # 별 움직임 (최소화)
        self.y += self.speed
        
        # 별 깜빡임 (최적화)
        if random.random() < 0.1:  # 10%의 확률로만 깜빡임 계산
            self.brightness += self.twinkle_speed * self.twinkle_direction
            
            # 밝기 범위 제한
            if self.brightness > self.max_brightness:
                self.brightness = self.max_brightness
                self.twinkle_direction = -1
            elif self.brightness < self.max_brightness * 0.4:
                self.brightness = self.max_brightness * 0.4
                self.twinkle_direction = 1
                
            # 색상 업데이트 (약간의 파란색 추가)
            b = min(255, int(self.brightness * 1.2))
            self.color = (int(self.brightness), int(self.brightness), b)

    def draw(self, screen):
        # 큰 별은 원으로, 작은 별은 점으로 그리기
        if self.size >= 2:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        else:
            screen.set_at((int(self.x), int(self.y)), self.color)

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.star_count = 70  # 별 개수 줄임
        self.create_stars()

    def create_stars(self):
        # 별 생성 (여러 크기와 밝기)
        for _ in range(self.star_count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.choice([1, 1, 1, 2, 2, 3])  # 작은 별 비율 증가
            brightness = random.randint(100, 255)
            speed = random.uniform(0.1, 0.5)  # 좀 더 느린 별
            self.stars.append(Star(x, y, size, brightness, speed))

    def update(self):
        # 절반의 별만 업데이트
        for star in self.stars[::2]:
            star.update()
            
            # 화면 밖으로 나간 별 다시 위치시키기
            if star.y > self.height:
                star.y = 0
                star.x = random.randint(0, self.width)

    def draw(self, screen):
        # 모든 별 그리기 (큰 별부터 그려서 겹치는 효과)
        for star in sorted(self.stars, key=lambda s: s.size):
            star.draw(screen) 
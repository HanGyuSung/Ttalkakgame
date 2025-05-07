import pygame
import sys

# 게임 초기화
pygame.init()

# 오디오 초기화 (오류 발생해도 무시)
try:
    pygame.mixer.init()
except:
    print("오디오 초기화 실패")

# 게임 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimal Test")
clock = pygame.time.Clock()

# 기본 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 게임 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 화면 그리기
    screen.fill(BLACK)
    
    # 간단한 사각형 그리기
    pygame.draw.rect(screen, BLUE, (50, 50, 100, 100))
    
    # 텍스트 표시
    font = pygame.font.SysFont(None, 36)
    text = font.render("테스트 화면", True, WHITE)
    screen.blit(text, (300, 300))
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit() 
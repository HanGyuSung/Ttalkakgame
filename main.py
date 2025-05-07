import pygame
import sys

# 게임 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 게임 설정
WIDTH, HEIGHT = 800, 600
FPS = 60

# 화면 설정 - 웹 배포용 최소 세팅
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Web Test")
clock = pygame.time.Clock()

# 디버그 정보 목록
debug_info = []

# 버전 정보 추가
try:
    debug_info.append(f"PyGame Version: {pygame.version.ver}")
except:
    debug_info.append("Version info not available")

# 오디오 초기화 시도
try:
    pygame.mixer.init()
    debug_info.append("Audio: Initialized")
except Exception as e:
    debug_info.append(f"Audio Error: {type(e).__name__}")

# 폰트 초기화
font = None
try:
    font = pygame.font.SysFont(None, 24)
    debug_info.append("Font: Initialized")
except Exception as e:
    debug_info.append(f"Font Error: {type(e).__name__}")

# 게임 루프
frame_count = 0
running = True

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 화면 그리기
    screen.fill(BLACK)
    
    # 기본 도형 그리기
    pygame.draw.rect(screen, BLUE, (50, 50, 100, 100))
    pygame.draw.circle(screen, GREEN, (300, 150), 50)
    pygame.draw.line(screen, RED, (400, 100), (650, 150), 5)
    
    # 디버그 정보 표시
    if font:
        for i, info in enumerate(debug_info):
            text_surface = font.render(info, True, WHITE)
            screen.blit(text_surface, (10, 10 + i*30))
        
        # 프레임 카운터
        frame_count += 1
        frame_info = f"Frame: {frame_count}"
        frame_text = font.render(frame_info, True, WHITE)
        screen.blit(frame_text, (WIDTH - 150, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(FPS)

# 게임 종료
try:
    pygame.quit()
except:
    pass 
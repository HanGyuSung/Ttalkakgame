"""
웹 호환 버전의 간단한 PyGame 예제
pygbag으로 빌드 시 웹에서 실행 가능
"""
import pygame
import sys

# pygame 모듈 초기화 - 최소한의 필수 모듈만 초기화
pygame.display.init()
pygame.font.init()

# 게임 설정 - 브라우저 호환성을 위해 작은 크기 사용
WIDTH, HEIGHT = 640, 480
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 화면 설정 - 웹 브라우저에서 작동하는 기본 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Web Demo")
clock = pygame.time.Clock()

# 게임 요소
box_x, box_y = 50, 50
box_speed = 2
font = None

# 메인 루프
def main():
    global box_x, box_y, font
    
    # 폰트 초기화
    try:
        font = pygame.font.SysFont(None, 24)
    except Exception as e:
        print(f"폰트 초기화 실패: {e}")

    # 사운드는 나중에 초기화 (사용자 상호작용 이후)
    sound_initialized = False
    
    # 메인 게임 루프
    running = True
    frame_count = 0
    
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 클릭하면 오디오 초기화 시도 (사용자 상호작용 후)
            if event.type == pygame.MOUSEBUTTONDOWN and not sound_initialized:
                try:
                    pygame.mixer.init()
                    sound_initialized = True
                except Exception as e:
                    print(f"오디오 초기화 실패: {e}")
        
        # 화면 그리기
        screen.fill(BLACK)
        
        # 상자 이동
        box_x += box_speed
        if box_x > WIDTH - 100 or box_x < 0:
            box_speed = -box_speed
        
        # 도형 그리기
        pygame.draw.rect(screen, BLUE, (box_x, box_y, 100, 100))
        pygame.draw.circle(screen, GREEN, (WIDTH//2, HEIGHT//2), 50)
        
        # 프레임 카운터와 상태 텍스트
        frame_count += 1
        if font:
            # FPS 표시
            fps_text = font.render(f"Frame: {frame_count}", True, WHITE)
            screen.blit(fps_text, (10, 10))
            
            # 오디오 상태 표시
            audio_status = "Audio: Initialized" if sound_initialized else "Audio: Click to initialize"
            audio_text = font.render(audio_status, True, WHITE)
            screen.blit(audio_text, (10, 40))
            
            # 안내 텍스트
            help_text = font.render("Click anywhere to initialize audio", True, WHITE)
            screen.blit(help_text, (WIDTH//2 - 130, HEIGHT - 30))
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(FPS)

# 스크립트 실행
try:
    main()
except Exception as e:
    print(f"Error: {e}")
finally:
    # 게임 종료
    pygame.quit() 
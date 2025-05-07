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

# 실제 게임 루프 함수
def game_loop():
    global box_x, box_y, font
    
    # 사운드 초기화 시도
    sound_initialized = False
    try:
        pygame.mixer.init()
        sound_initialized = True
    except Exception as e:
        print(f"오디오 초기화 실패: {e}")
    
    # 메인 게임 루프
    running = True
    frame_count = 0
    
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
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
            audio_status = "Audio: Initialized" if sound_initialized else "Audio: Failed to initialize"
            audio_text = font.render(audio_status, True, WHITE)
            screen.blit(audio_text, (10, 40))
        
        # 화면 업데이트
        pygame.display.flip()
        clock.tick(FPS)

# 메인 루프
def main():
    global font
    
    # 폰트 초기화
    try:
        font = pygame.font.SysFont(None, 24)
        large_font = pygame.font.SysFont(None, 48)
    except Exception as e:
        print(f"폰트 초기화 실패: {e}")
        large_font = None
    
    # 시작 화면 표시 (클릭 대기)
    waiting_for_click = True
    
    while waiting_for_click:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # 클릭하면 게임 시작
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_click = False
                
        # 시작 화면 그리기
        screen.fill(BLACK)
        
        # 시작 메시지 표시
        if large_font:
            title_text = large_font.render("PyGame Web Demo", True, WHITE)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
            
            start_text = large_font.render("Click to Start", True, GREEN)
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        
        if font:
            info_text = font.render("Browser security requires user interaction before audio", True, WHITE)
            screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT*3//4))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    # 게임 루프 시작
    game_loop()

# 스크립트 실행
try:
    main()
except Exception as e:
    print(f"Error: {e}")
finally:
    # 게임 종료
    pygame.quit() 
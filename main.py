import pygame
import sys
import random
import math
from player import Player
from platform_tile import Platform
from coin import Coin
from enemy import Enemy
from powerup import Powerup
from background import Background
from sound import SoundManager

# 게임 초기화
pygame.init()

# 오디오 초기화 - 웹 배포 오류 방지를 위해 try-except로 감싸기
try:
    pygame.mixer.init()
except Exception as e:
    print(f"오디오 초기화 실패: {e}")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# 게임 설정
WIDTH, HEIGHT = 800, 600
FPS = 60

# 화면 설정 - 웹 배포를 위해 옵션 제거
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("픽셀 어드벤처 2.0")
clock = pygame.time.Clock()

# 폰트 설정 - 캐싱
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# 텍스트 캐싱
cached_texts = {}

def get_text_surface(font, text, color):
    """캐시된 텍스트 표면 가져오기"""
    key = (id(font), text, color)
    if key not in cached_texts:
        cached_texts[key] = font.render(text, True, color)
    return cached_texts[key]

class PopupText:
    def __init__(self, x, y, text, color, size=24, lifetime=60):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.velocity_y = -2
        self.font = pygame.font.SysFont(None, size)
        self.text_surface = self.font.render(text, True, color)
        
    def update(self):
        self.lifetime -= 1
        self.y += self.velocity_y
        self.velocity_y += 0.05
        
    def draw(self, screen):
        if self.lifetime <= 0:
            return
            
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        # 알파 값이 변할 때만 새로 설정
        if alpha < 255:
            temp_surface = self.text_surface.copy()
            temp_surface.set_alpha(alpha)
            screen.blit(temp_surface, (self.x, self.y))
        else:
            screen.blit(self.text_surface, (self.x, self.y))

class Game:
    def __init__(self):
        self.running = True
        self.score = 0
        self.level = 1
        self.time_left = 120
        self.last_time_update = pygame.time.get_ticks()
        self.max_level = 3  # 총 스테이지 수
        
        # 사운드 매니저 초기화
        try:
            self.sound_manager = SoundManager()
            
            # 배경 음악 재생
            try:
                # 우주 분위기 MP3 파일 사용
                self.sound_manager.play_music("space-ambient-cinematic-music-335721.mp3")
            except Exception as e:
                print(f"MP3 배경 음악 재생 중 오류: {e}")
                try:
                    # MP3 파일이 없으면 다운로드
                    from prepare_mp3 import prepare_mp3_file
                    prepare_mp3_file()
                    self.sound_manager.play_music("space-ambient-cinematic-music-335721.mp3")
                except Exception as e2:
                    print(f"배경 음악 재생 실패")
                    try:
                        # 기본 배경음악 사용
                        self.sound_manager.play_music("background.wav")
                    except:
                        # 모든 것이 실패하면 새로 생성
                        try:
                            from create_background import create_background_music
                            create_background_music()
                            self.sound_manager.play_music("background.wav")
                        except Exception as e3:
                            print(f"모든 음악 재생 시도 실패: {e3}")
        except Exception as e:
            print(f"사운드 시스템 초기화 실패: {e}")
            self.sound_manager = None
        
        # 배경 생성
        self.background = Background(WIDTH, HEIGHT)
        
        # 게임 요소 초기화
        self.setup_level(self.level)
        
        # 게임 상태
        self.game_over = False
        self.victory = False
        self.bonus_added = False  # 보너스 점수 추가 여부를 추적
        self.level_complete = False
        self.level_transition_timer = 0
        
        # 파워업 상태
        self.power_speed = False
        self.power_jump = False
        self.power_shield = False
        self.powerup_timer = 0
        
        # 시각 효과
        self.popup_texts = []
        self.screen_shake = 0
        
        # 플레이어 생명
        self.lives = 3
        
        # 성능 최적화
        self.update_counter = 0
        self.fps_timer = pygame.time.get_ticks()
        self.fps_count = 0
        self.current_fps = 0

    def setup_level(self, level):
        """레벨에 따라 게임 요소 설정"""
        # 플랫폼 생성
        self.platforms = []
        self.create_platforms(level)
        
        # 플레이어 생성/위치 조정
        if hasattr(self, 'player'):
            self.player.x = 100
            self.player.y = HEIGHT - 100
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y
            self.player.velocity_x = 0
            self.player.velocity_y = 0
            self.player.is_jumping = False
            # 플레이어 상태 초기화
            self.player.speed = 5  # 기본 속도로 복귀
            self.player.jump_power = -10  # 기본 점프력으로 복귀
            self.player.max_jumps = 2  # 기본 점프 횟수로 복귀
        else:
            self.player = Player(100, HEIGHT - 100)
        
        # 파워업 상태 초기화
        self.power_speed = False
        self.power_jump = False
        self.power_shield = False
        self.powerup_timer = 0
        
        # 코인 생성
        self.coins = []
        self.create_coins(level)
        
        # 적 생성
        self.enemies = []
        self.create_enemies(level)
        
        # 파워업 생성
        self.powerups = []
        self.create_powerups(level)
        
        # 레벨별 시간 설정
        if level == 1:
            self.time_left = 120
        elif level == 2:
            self.time_left = 100
        else:
            self.time_left = 90
        
        # 레벨 전환 초기화
        self.level_complete = False
        self.level_transition_timer = 0

    def create_platforms(self, level):
        # 바닥 플랫폼
        for i in range(0, WIDTH, 50):
            self.platforms.append(Platform(i, HEIGHT - 50))
        
        # 레벨별 플랫폼 배치
        if level == 1:
            # 레벨 1 - 기본 플랫폼
            platform_positions = [
                (100, 450), (150, 450), (200, 450),
                (350, 400), (400, 400), (450, 400),
                (600, 350), (650, 350), (700, 350),
                (200, 300), (250, 300), (300, 300),
                (450, 250), (500, 250), (550, 250),
                (150, 200), (200, 200),
                (600, 150), (650, 150), (700, 150)
            ]
        elif level == 2:
            # 레벨 2 - 더 복잡한 플랫폼 배치
            platform_positions = [
                (100, 500), (150, 500), (200, 500),
                (300, 450), (350, 450), (400, 450),
                (500, 400), (550, 400), (600, 400),
                (700, 350), (750, 350),
                (600, 300), (550, 300),
                (400, 250), (350, 250), (300, 250),
                (200, 200), (150, 200),
                (100, 150), (150, 150),
                (300, 150), (350, 150),
                (500, 150), (550, 150),
                (700, 150), (750, 150)
            ]
        else:  # level 3 이상
            # 레벨 3 - 더 어려운 플랫폼 배치
            platform_positions = [
                (50, 500), (100, 500),
                (250, 450), (300, 450),
                (450, 400), (500, 400),
                (650, 350), (700, 350),
                (550, 300), (500, 300),
                (350, 250), (300, 250),
                (150, 200), (100, 200),
                (200, 150), (250, 150),
                (400, 150), (450, 150),
                (600, 150), (650, 150),
                (400, 100), (450, 100)  # 가장 높은 플랫폼
            ]
        
        for pos in platform_positions:
            self.platforms.append(Platform(pos[0], pos[1]))

    def create_coins(self, level):
        # 레벨별 코인 배치
        if level == 1:
            # 레벨 1 - 기본 코인 배치
            coin_positions = [
                (150, 420), (400, 370), (650, 320),
                (250, 270), (500, 220), (175, 170),
                (650, 120)
            ]
        elif level == 2:
            # 레벨 2 - 더 많은 코인, 더 높은 위치
            coin_positions = [
                (150, 470), (350, 420), (550, 370),
                (700, 320), (550, 270), (350, 220),
                (150, 170), (300, 120), (500, 120),
                (700, 120)
            ]
        else:  # level 3 이상
            # 레벨 3 - 더 어렵게 배치된 코인
            coin_positions = [
                (100, 470), (300, 420), (500, 370),
                (700, 320), (500, 270), (300, 220),
                (100, 170), (250, 120), (400, 70),
                (550, 120), (700, 120), (400, 170)
            ]
        
        for pos in coin_positions:
            self.coins.append(Coin(pos[0], pos[1]))

    def create_enemies(self, level):
        # 레벨별 적 배치
        if level == 1:
            # 레벨 1 - 비교적 느린 적
            enemy_positions = [
                (300, 420, 100, 1.5),  # (x, y, patrol_distance, speed)
                (500, 370, 120, 1.8),
                (250, 250, 80, 2.0)
            ]
        elif level == 2:
            # 레벨 2 - 더 빠른 적
            enemy_positions = [
                (300, 420, 120, 2.0),
                (500, 370, 140, 2.5),
                (250, 250, 100, 2.8),
                (600, 150, 80, 2.2)
            ]
        else:  # level 3 이상
            # 레벨 3 - 매우 빠른 적
            enemy_positions = [
                (300, 420, 150, 2.5),
                (500, 370, 160, 3.0),
                (250, 250, 120, 3.5),
                (600, 150, 100, 3.0),
                (150, 170, 80, 3.2)
            ]
        
        for pos in enemy_positions:
            self.enemies.append(Enemy(pos[0], pos[1], pos[2], pos[3]))
    
    def create_powerups(self, level):
        # 레벨별 파워업 배치
        if level == 1:
            # 레벨 1 - 기본 파워업
            powerup_positions = [
                (100, 150, "speed"),
                (400, 200, "jump"),
                (700, 300, "shield")
            ]
        elif level == 2:
            # 레벨 2 - 접근하기 어려운 곳에 파워업
            powerup_positions = [
                (150, 120, "speed"),
                (350, 170, "jump"),
                (700, 120, "shield")
            ]
        else:  # level 3 이상
            # 레벨 3 - 적과 가까운 곳에 파워업
            powerup_positions = [
                (250, 170, "speed"),
                (500, 120, "jump"),
                (600, 100, "shield"),
                (450, 50, "shield")  # 추가 보호막
            ]
        
        for pos in powerup_positions:
            self.powerups.append(Powerup(pos[0], pos[1], pos[2]))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.play("jump")
                        except:
                            pass
                elif event.key == pygame.K_r and (self.game_over or self.victory):
                    self.__init__()  # 게임 재시작 (모든 변수 초기화)
                elif event.key == pygame.K_m:  # 음악 켜기/끄기
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.toggle_music()
                        except:
                            pass
                elif event.key == pygame.K_s:  # 효과음 켜기/끄기
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.toggle_sound()
                        except:
                            pass

    def update(self):
        # FPS 계산
        self.fps_count += 1
        current_time = pygame.time.get_ticks()
        if current_time - self.fps_timer >= 1000:
            self.current_fps = self.fps_count
            self.fps_count = 0
            self.fps_timer = current_time
        
        if self.game_over or self.victory:
            return
        
        # 레벨 전환 중인 경우, 타이머 업데이트
        if self.level_complete:
            self.level_transition_timer += 1
            if self.level_transition_timer >= 120:  # 2초 정도 대기
                self.level_complete = False
                self.level_transition_timer = 0
            return  # 레벨 전환 중에는 게임 업데이트 중지
        
        # 시간 업데이트 (1초마다)
        if current_time - self.last_time_update >= 1000:
            self.time_left -= 1
            self.last_time_update = current_time
            
            if self.time_left <= 0:
                self.game_over = True
        
        # 계산량 분산을 위한 카운터
        self.update_counter += 1
        
        # 배경 업데이트 (더 적은 횟수로)
        if self.update_counter % 5 == 0:
            self.background.update()
        
        # 플레이어 업데이트 (항상 실행)
        self.player.update()
        
        # 코인 업데이트 (더 적은 횟수로)
        if self.update_counter % 3 == 0:
            for coin in self.coins:
                coin.update()
        
        # 파워업 업데이트 (더 적은 횟수로)
        if self.update_counter % 3 == 0:
            for powerup in self.powerups:
                powerup.update()
        
        # 파워업 타이머 업데이트
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.power_speed = False
                self.power_jump = False
                
                # 타이머가 끝나면 효과 제거
                if self.power_speed:
                    self.player.speed = 5
                if self.power_jump:
                    self.player.jump_power = -10
                    self.player.max_jumps = 2
        
        # 스크린 셰이크 업데이트
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # 팝업 텍스트 업데이트 (더 효율적으로)
        if self.popup_texts:  # 빈 리스트 확인 먼저
            active_popups = []
            for text in self.popup_texts:
                text.update()
                if text.lifetime > 0:
                    active_popups.append(text)
            self.popup_texts = active_popups
        
        # 플랫폼 충돌 처리
        self.player.is_on_ground = False
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                # 플랫폼 위에 있는 경우
                if self.player.velocity_y >= 0 and self.player.rect.bottom >= platform.rect.top and self.player.rect.top < platform.rect.top:
                    self.player.rect.bottom = platform.rect.top
                    self.player.y = self.player.rect.y
                    self.player.velocity_y = 0
                    self.player.is_on_ground = True
                    self.player.is_jumping = False
                    break
                # 플랫폼 아래에서 부딪힐 경우
                elif self.player.velocity_y < 0 and self.player.rect.top <= platform.rect.bottom and self.player.rect.bottom > platform.rect.bottom:
                    self.player.rect.top = platform.rect.bottom
                    self.player.y = self.player.rect.y
                    self.player.velocity_y = 0
        
        # 코인 수집 (충돌 검사 전 먼저 길이 확인)
        if self.coins:  # 빈 리스트 검사 먼저
            for coin in self.coins[:]:
                if self.player.rect.colliderect(coin.rect):
                    self.coins.remove(coin)
                    self.score += 10
                    
                    # 코인 사운드 재생
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.play("coin")
                        except:
                            pass
                    
                    # 효과: 점수 팝업 (최대 3개로 제한)
                    if len(self.popup_texts) < 3:
                        self.popup_texts.append(
                            PopupText(coin.x, coin.y - 20, "+10", YELLOW)
                        )
        
        # 파워업 획득 (충돌 검사 최적화)
        if self.powerups:  # 빈 리스트 검사 먼저
            for powerup in self.powerups[:]:
                if powerup.active and self.player.rect.colliderect(powerup.rect):
                    # 파워업 사운드 재생
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.play("powerup")
                        except:
                            pass
                    
                    # 파워업 종류별 효과 적용
                    if powerup.type == "speed":
                        self.power_speed = True
                        self.player.speed = 8
                        if len(self.popup_texts) < 3:
                            self.popup_texts.append(
                                PopupText(powerup.x, powerup.y - 20, "Speed Up!", (0, 255, 255))
                            )
                    elif powerup.type == "jump":
                        self.power_jump = True
                        self.player.jump_power = -12
                        self.player.max_jumps = 3
                        if len(self.popup_texts) < 3:
                            self.popup_texts.append(
                                PopupText(powerup.x, powerup.y - 20, "Triple Jump!", (255, 0, 255))
                            )
                    elif powerup.type == "shield":
                        self.power_shield = True
                        if len(self.popup_texts) < 3:
                            self.popup_texts.append(
                                PopupText(powerup.x, powerup.y - 20, "Shield!", WHITE)
                            )
                    
                    # 아이템 비활성화 및 타이머 설정
                    powerup.active = False
                    self.powerup_timer = 600
                
        # 게임 승리 조건
        if len(self.coins) == 0:
            if self.level < self.max_level:
                # 다음 레벨로 넘어가기
                self.level += 1
                self.level_complete = True
                # 레벨 클리어 사운드 재생
                if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                    try:
                        self.sound_manager.play("victory")
                    except:
                        pass
                # 레벨 전환 준비
                self.setup_level(self.level)
                # 보너스 점수 추가
                bonus = self.time_left * 5
                self.score += bonus
                # 레벨 전환 텍스트 표시
                self.popup_texts.append(
                    PopupText(WIDTH // 2 - 80, HEIGHT // 2, f"Level {self.level}!", GREEN, 48, 120)
                )
                self.popup_texts.append(
                    PopupText(WIDTH // 2 - 80, HEIGHT // 2 + 40, f"Time Bonus: +{bonus}", YELLOW, 36, 120)
                )
            else:
                # 모든 레벨 클리어 - 게임 승리
                self.victory = True
                # 승리 사운드 재생
                if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                    try:
                        self.sound_manager.play("victory")
                    except:
                        pass
        
        # 적과의 충돌 (최적화)
        for enemy in self.enemies[:]:
            # 적 업데이트 (적은 횟수로)
            if self.update_counter % 3 == 0:
                enemy.update()
                
            # 적과 플레이어의 충돌 감지
            if self.player.rect.colliderect(enemy.rect):
                if self.power_shield:
                    # 보호막 사용 (적 제거)
                    self.enemies.remove(enemy)
                    self.power_shield = False
                    
                    # 화면 효과
                    self.screen_shake = 5  # 셰이크 감소
                    if len(self.popup_texts) < 3:
                        self.popup_texts.append(
                            PopupText(enemy.x, enemy.y - 20, "Shield Broken!", WHITE, 30)
                        )
                    # 쉴드 사운드 재생
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.play("powerup")
                        except:
                            pass
                else:
                    # 생명 감소
                    self.lives -= 1
                    
                    # 피격 사운드 재생
                    if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                        try:
                            self.sound_manager.play("hurt")
                        except:
                            pass
                    
                    # 화면 효과
                    self.screen_shake = 5  # 셰이크 감소
                    if len(self.popup_texts) < 3:  # 팝업 제한
                        self.popup_texts.append(
                            PopupText(self.player.x, self.player.y - 30, "-1 Life", RED, 30)
                        )
                    
                    # 플레이어 위치 리셋
                    self.player.x -= 50
                    if self.player.x < 0:
                        self.player.x = 0
                    self.player.rect.x = self.player.x
                    
                    if self.lives <= 0:
                        self.game_over = True
                        # 게임 오버 사운드 재생
                        if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                            try:
                                self.sound_manager.play("game_over")
                            except:
                                pass
        
        # 화면 밖으로 떨어진 경우
        if self.player.rect.top > HEIGHT:
            self.lives -= 1
            # 피격 사운드 재생
            if hasattr(self, 'sound_manager') and self.sound_manager is not None and self.lives > 0:
                try:
                    self.sound_manager.play("hurt")
                except:
                    pass
                
            if self.lives <= 0:
                self.game_over = True
                # 게임 오버 사운드 재생
                if hasattr(self, 'sound_manager') and self.sound_manager is not None:
                    try:
                        self.sound_manager.play("game_over")
                    except:
                        pass
            else:
                # 플레이어 위치 리셋
                self.player.x = 100
                self.player.y = HEIGHT - 100
                self.player.rect.x = self.player.x
                self.player.rect.y = self.player.y
                self.player.velocity_y = 0
                
                # 화면 효과
                if len(self.popup_texts) < 3:
                    self.popup_texts.append(
                        PopupText(WIDTH // 2 - 50, HEIGHT // 2, "-1 Life", RED, 30)
                    )

    def draw(self):
        # 셰이크 효과 (셰이크 제거 - 이는 많은 성능을 소모함)
        shake_offset_x = 0
        shake_offset_y = 0
        
        # 배경 (더 어둡게 하여 별이 잘 보이도록)
        screen.fill((10, 10, 30))
        
        # 별 그리기
        self.background.draw(screen)
        
        # 레벨 전환 화면
        if self.level_complete:
            # 반투명 오버레이
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            
            # 레벨 클리어 텍스트
            level_text = get_text_surface(font, f"LEVEL {self.level-1} COMPLETE!", GREEN)
            next_level_text = get_text_surface(font, f"Get Ready for Level {self.level}", YELLOW)
            
            screen.blit(level_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            screen.blit(next_level_text, (WIDTH // 2 - 170, HEIGHT // 2 + 10))
            
            # 진행 바 표시
            progress = self.level_transition_timer / 120  # 0.0 ~ 1.0
            bar_width = int(300 * progress)
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 20), 2)
            pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 150, HEIGHT // 2 + 60, bar_width, 20))
            
            pygame.display.flip()
            return
        
        # 플랫폼 그리기
        for platform in self.platforms:
            platform.draw(screen)
        
        # 코인 그리기
        for coin in self.coins:
            coin.draw(screen)
        
        # 파워업 그리기
        for powerup in self.powerups:
            powerup.draw(screen)
        
        # 적 그리기
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # 플레이어 그리기
        self.player.draw(screen)
        
        # 팝업 텍스트 그리기 (최대 3개까지)
        for i, text in enumerate(self.popup_texts[:3]):
            text.draw(screen)
        
        # UI 정보 (캐시된 텍스트 사용)
        # 점수 표시
        score_text = get_text_surface(font, f"Score: {self.score}", WHITE)
        screen.blit(score_text, (10, 10))
        
        # 생명력 표시
        lives_text = get_text_surface(font, f"Lives: {self.lives}", WHITE)
        screen.blit(lives_text, (10, 50))
        
        # 시간 표시
        time_color = RED if self.time_left <= 10 else WHITE
        time_text = get_text_surface(font, f"Time: {self.time_left}", time_color)
        screen.blit(time_text, (WIDTH - 150, 10))
        
        # FPS 표시 - 디버그용
        if self.current_fps < 30:  # 프레임이 낮을 때만 표시 (성능 향상을 위해)
            fps_text = get_text_surface(small_font, f"FPS: {self.current_fps}", WHITE)
            screen.blit(fps_text, (WIDTH - 80, 580))
        
        # 파워업 상태 표시 (간소화 - 한번에 그리기)
        powerup_y = 50
        powerup_texts = []
        
        if self.power_speed:
            powerup_texts.append(("Speed", (0, 255, 255)))
            
        if self.power_jump:
            powerup_texts.append(("Jump+", (255, 0, 255)))
            
        if self.power_shield:
            powerup_texts.append(("Shield", WHITE))
        
        # 한번에 렌더링
        for i, (text, color) in enumerate(powerup_texts):
            text_surf = get_text_surface(small_font, text, color)
            screen.blit(text_surf, (WIDTH - 150, powerup_y + i * 25))
        
        # 사운드 상태 표시
        if hasattr(self, 'sound_manager') and self.sound_manager is not None:
            sound_status = "Sound: ON" if self.sound_manager.sound_enabled else "Sound: OFF"
            music_status = "Music: ON" if self.sound_manager.music_enabled else "Music: OFF"
            
            sound_text = get_text_surface(small_font, sound_status, WHITE)
            music_text = get_text_surface(small_font, music_status, WHITE)
            
            screen.blit(sound_text, (10, HEIGHT - 40))
            screen.blit(music_text, (10, HEIGHT - 20))
        
        # 게임 오버 메시지
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            game_over_text = get_text_surface(font, "GAME OVER! Press R to restart", RED)
            screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
            
            final_score = get_text_surface(font, f"Final Score: {self.score}", WHITE)
            screen.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
        
        # 승리 메시지
        if self.victory:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            victory_text = get_text_surface(font, "YOU WIN! Press R to play again", GREEN)
            screen.blit(victory_text, (WIDTH // 2 - 180, HEIGHT // 2))
            
            # 보너스 점수를 한 번만 추가
            bonus = self.time_left * 5
            if not self.bonus_added:
                self.score += bonus  # 남은 시간 보너스
                self.bonus_added = True
            
            bonus_text = get_text_surface(font, f"Time Bonus: +{bonus}", YELLOW)
            screen.blit(bonus_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
            
            final_score = get_text_surface(font, f"Final Score: {self.score}", WHITE)
            screen.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 + 80))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)
        
        # 게임 종료 시 사운드 정리
        if hasattr(self, 'sound_manager') and self.sound_manager is not None:
            try:
                self.sound_manager.stop_music()
                self.sound_manager.stop()
            except:
                pass

# 웹 배포를 위해 바로 실행
game = Game()
game.run()
pygame.quit()
sys.exit() 
import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 35
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -10
        self.gravity = 0.7
        self.max_fall_speed = 15
        self.is_jumping = False
        self.is_on_ground = False
        self.color = (0, 0, 255)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # 이단 점프 관련 변수
        self.max_jumps = 2
        self.jump_count = 0
        
        # 애니메이션 상태
        self.direction = "right"
        
        # 파티클 효과 (최적화: 수 감소)
        self.particles = []
        self.max_particles = 10
        self.particle_timer = 0
        self.last_jump_time = 0
        
        # 점프 처리 개선
        self.can_jump = True  # 점프 가능 여부
        self.jump_buffer_time = 0  # 점프 버퍼링 타이머
        self.jump_buffer_limit = 100  # 점프 버퍼링 제한 시간 (ms)
        self.coyote_time = 0  # 공중에 있어도 잠시 점프 가능한 시간
        self.coyote_limit = 150  # 코요테 타임 제한 (ms)
    
    def jump(self):
        current_time = pygame.time.get_ticks()
        
        # 점프 버퍼링: 플레이어가 땅에 닿기 직전에 점프키를 눌러도 점프 가능
        self.jump_buffer_time = current_time
        
        # 1. 지면에 있거나 코요테 타임이 남아있는 경우 (첫 번째 점프)
        if (self.is_on_ground or 
            (current_time - self.coyote_time < self.coyote_limit and self.jump_count == 0)):
            self.velocity_y = self.jump_power
            self.jump_count = 1
            self.is_jumping = True
            self.is_on_ground = False
            self.last_jump_time = current_time
            self.can_jump = False  # 점프 키 릴리즈 전까지 다시 점프 불가
            return True
        
        # 2. 이단 점프가 가능한 경우
        elif self.jump_count < self.max_jumps and self.jump_count > 0:
            # 마지막 점프와의 간격 확인 (너무 빠른 연속 점프 방지)
            if current_time - self.last_jump_time > 100:
                self.velocity_y = self.jump_power
                self.jump_count += 1
                self.is_jumping = True
                self.last_jump_time = current_time
                self.can_jump = False  # 점프 키 릴리즈 전까지 다시 점프 불가
                return True
        
        return False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        
        # 점프 키 릴리즈 감지 (다음 점프를 위해)
        if not keys[pygame.K_SPACE]:
            self.can_jump = True
        
        # 좌우 이동
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.direction = "right"
        
        # 점프 버퍼링 처리 (키를 미리 누르고 땅에 닿으면 바로 점프)
        if (not self.is_jumping and self.is_on_ground and 
            current_time - self.jump_buffer_time < self.jump_buffer_limit):
            self.velocity_y = self.jump_power
            self.jump_count = 1
            self.is_jumping = True
            self.is_on_ground = False
            self.jump_buffer_time = 0  # 버퍼 초기화
        
        # 중력 적용
        if not self.is_on_ground:
            self.velocity_y += self.gravity
            # 최대 낙하 속도 제한
            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed
        else:
            # 땅에 닿으면 점프 카운트 초기화
            self.jump_count = 0
            # 땅에서 떨어질 때 코요테 타임 기록
            if self.velocity_y < 0:
                self.coyote_time = current_time
        
        # 위치 업데이트
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # 화면 경계 확인
        if self.x < 0:
            self.x = 0
        elif self.x > 800 - self.width:
            self.x = 800 - self.width
        
        # 충돌 박스 업데이트
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 움직임 잔상 효과 - 성능 최적화
        # 파티클 생성 조건 강화
        self.particle_timer += 1
        is_moving_fast = abs(self.velocity_x) > 3 or abs(self.velocity_y) > 3
        if is_moving_fast and self.particle_timer >= 8:  # 더 긴 간격으로 파티클 생성
            self.add_particle()
            self.particle_timer = 0
        
        # 파티클 수명 감소 (간단하게)
        for p in self.particles:
            p[3] -= 1  # 수명 감소
        
        # 오래된 파티클 제거 (최적화)
        i = 0
        while i < len(self.particles):
            if self.particles[i][3] <= 0:
                self.particles.pop(i)
            else:
                i += 1
    
    def add_particle(self):
        # 파티클 수 제한 (더 엄격하게)
        if len(self.particles) >= self.max_particles:
            # 가장 오래된 파티클 제거
            self.particles.pop(0)
            
        # 이동 방향의 반대쪽에 파티클 생성
        if self.direction == "right":
            x = self.rect.x
        else:
            x = self.rect.x + self.width
        
        y = self.rect.y + self.height / 2
        
        # [x좌표, y좌표, 크기, 수명]
        particle = [x, y, 3, 5]  # 크기와 수명 감소
        self.particles.append(particle)
    
    def draw(self, screen):
        # 플레이어의 사각형 그리기
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 파티클 그리기 (더 단순화)
        for p in self.particles:
            size = p[2]
            alpha = int(200 * (p[3] / 5))
            # 단순한 사각형 대신 알파값이 있는 더 작은 사각형
            # 이 부분은 최적화를 위해 직접 좌표 계산을 사용
            rect = (int(p[0]), int(p[1]), size, size)
            pygame.draw.rect(screen, (100, 100, 255), rect)
        
        # 눈 그리기 (방향에 따라 위치 조정)
        if self.direction == "right":
            eye_x = self.rect.x + int(self.width * 0.7)
        else:
            eye_x = self.rect.x + int(self.width * 0.3)
        
        eye_y = self.rect.y + int(self.height * 0.2)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 3)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 1)
        
        # 점프 게이지 표시 - 이중 점프일 때만 표시
        if self.jump_count == 1 and not self.is_on_ground:
            pygame.draw.rect(screen, (255, 255, 0), 
                           (self.rect.x + self.width / 2 - 5, self.rect.y - 15, 10, 5)) 
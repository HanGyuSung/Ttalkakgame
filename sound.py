import pygame
import os

class SoundManager:
    def __init__(self):
        # pygame 믹서 초기화
        pygame.mixer.init()
        
        # 볼륨 설정
        self.sound_volume = 0.5
        self.music_volume = 0.3
        
        # 사운드 사전
        self.sounds = {}
        
        # 켜기/끄기 플래그
        self.sound_enabled = True
        self.music_enabled = True
        
        # 기본 경로
        self.sound_path = "assets/sounds"
        
        # 기본 효과음 로드
        self.load_default_sounds()
    
    def load_default_sounds(self):
        """게임에 필요한 기본 효과음 로드"""
        sound_files = {
            "jump": "jump.wav",
            "coin": "coin.wav",
            "powerup": "powerup.wav",
            "hurt": "hurt.wav",
            "game_over": "game_over.wav",
            "victory": "victory.wav"
        }
        
        for sound_name, file_name in sound_files.items():
            full_path = os.path.join(self.sound_path, file_name)
            if os.path.exists(full_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(full_path)
                    self.sounds[sound_name].set_volume(self.sound_volume)
                except:
                    pass
    
    def play(self, sound_name):
        """효과음 재생"""
        if not self.sound_enabled:
            return
            
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def stop(self, sound_name=None):
        """효과음 정지"""
        if sound_name:
            if sound_name in self.sounds:
                self.sounds[sound_name].stop()
        else:
            pygame.mixer.stop()
    
    def play_music(self, music_file):
        """배경 음악 재생"""
        if not self.music_enabled:
            return
            
        full_path = os.path.join(self.sound_path, music_file)
        
        if os.path.exists(full_path):
            try:
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # 무한 반복
            except Exception as e:
                print(f"음악 재생 실패")
    
    def stop_music(self):
        """배경 음악 정지"""
        pygame.mixer.music.stop()
    
    def toggle_sound(self):
        """효과음 켜기/끄기 전환"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
    
    def toggle_music(self):
        """배경 음악 켜기/끄기 전환"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        return self.music_enabled
    
    def set_sound_volume(self, volume):
        """효과음 볼륨 설정"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """배경 음악 볼륨 설정"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
    def add_sound(self, name, file_path):
        """새 효과음 추가"""
        if os.path.exists(file_path):
            try:
                self.sounds[name] = pygame.mixer.Sound(file_path)
                self.sounds[name].set_volume(self.sound_volume)
                return True
            except:
                return False
        return False 
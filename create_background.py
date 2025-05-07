import wave
import math
import struct
import os

def create_background_music(filename="background.wav"):
    """간단한 배경 음악 생성"""
    # 오디오 파라미터
    sample_rate = 44100
    duration = 8.0  # 8초 (루프됨)
    
    # 폴더 존재 확인
    os.makedirs("assets/sounds", exist_ok=True)
    
    # 파일 생성
    output_path = f"assets/sounds/{filename}"
    with wave.open(output_path, "w") as wav_file:
        wav_file.setnchannels(1)  # 모노 채널
        wav_file.setsampwidth(2)  # 16비트
        wav_file.setframerate(sample_rate)
        
        # 간단한 멜로디 패턴 생성
        notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 349.23, 293.66]  # C, D, E, F, G, A, F, D 음계
        note_duration = 0.5  # 2분음표 (0.5초)
        
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            current_note_idx = int((t // note_duration) % len(notes))
            note_phase = t % note_duration
            frequency = notes[current_note_idx]
            
            # 멜로디 합성 (볼륨 감소로 더 부드러운 소리)
            value = int(32767 * 0.15 * math.sin(2 * math.pi * frequency * t))
            # 화음 추가
            value += int(32767 * 0.08 * math.sin(2 * math.pi * frequency * 2 * t))
            # 저주파 베이스 추가
            value += int(32767 * 0.12 * math.sin(2 * math.pi * (frequency/2) * t))
            
            # 각 음표의 페이드 인/아웃
            if note_phase < 0.05:
                # 페이드 인
                value = int(value * (note_phase / 0.05))
            elif note_phase > note_duration - 0.05:
                # 페이드 아웃
                value = int(value * (1 - (note_phase - (note_duration - 0.05)) / 0.05))
            
            packed_value = struct.pack('h', value)
            wav_file.writeframes(packed_value)
    
    print(f"배경 음악 생성 완료: {output_path}")
    return output_path

if __name__ == "__main__":
    create_background_music() 
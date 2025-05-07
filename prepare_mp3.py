import os
import shutil
import sys
import urllib.request

def prepare_mp3_file():
    """
    MP3 파일을 assets/sounds 폴더로 복사하거나 다운로드
    """
    # 파일 정보
    filename = "space-ambient-cinematic-music-335721.mp3"
    target_dir = "assets/sounds"
    target_path = os.path.join(target_dir, filename)
    
    # 폴더 생성
    os.makedirs(target_dir, exist_ok=True)
    
    # 현재 디렉토리에서 파일 찾기
    if os.path.exists(filename):
        print(f"파일 발견: {filename}")
        # 파일 복사
        shutil.copy2(filename, target_path)
        print(f"파일을 {target_path}로 복사했습니다.")
        return target_path
    else:
        print(f"현재 디렉토리에 {filename}이 없습니다.")
        
        # 이미 대상 폴더에 있는지 확인
        if os.path.exists(target_path):
            print(f"파일이 이미 {target_path}에 있습니다.")
            return target_path
        
        print("인터넷에서 샘플 공간 음악 파일 다운로드 시도...")
        
        # 샘플 우주 배경 음악 URL (Creative Commons 라이센스)
        # 이 URL은 예시일 뿐이며 실제로는 다른 URL을 사용해야 함
        sample_url = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c9d374f008.mp3"
        
        try:
            # 파일 다운로드
            urllib.request.urlretrieve(sample_url, target_path)
            print(f"샘플 우주 배경 음악을 {target_path}로 다운로드했습니다.")
            return target_path
        except Exception as e:
            print(f"다운로드 실패: {e}")
            print("\n수동 설치 방법:")
            print(f"1. {filename} 파일을 웹에서 다운로드하세요.")
            print(f"2. 이 파일을 '{target_dir}' 폴더에 복사하세요.")
            return None

if __name__ == "__main__":
    print("MP3 배경 음악 준비 중...")
    result = prepare_mp3_file()
    if result:
        print("준비 완료!")
    else:
        print("MP3 파일 준비 실패") 
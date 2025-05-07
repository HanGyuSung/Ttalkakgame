import os
import shutil
import subprocess
import sys
import platform

def clear_console():
    """Clear the console screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def run_command(command, description):
    """Run a shell command and print its output."""
    print(f"\n📋 {description}...\n")
    
    try:
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        for line in process.stdout:
            print(line.strip())
            
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"\n❌ 오류: {e}")
        return False

def main():
    clear_console()
    print("🎮 픽셀 어드벤처 - 웹 빌드 도구 🎮")
    print("=" * 40)
    
    # 1. 필요한 패키지 설치
    print("\n🔍 pygbag 설치 확인 중...")
    try:
        import pygbag
        print("✅ pygbag이 이미 설치되어 있습니다.")
    except ImportError:
        print("🔄 pygbag 설치 중...")
        if not run_command("pip install pygbag", "pygbag 설치"):
            print("❌ pygbag 설치 실패")
            return
    
    # 2. 웹 빌드 생성 - 최소한의 테스트 파일 사용
    if not run_command("pygbag --build minimal_test.py", "게임 웹 빌드 생성"):
        print("❌ 웹 빌드 생성 실패")
        return
    
    # 3. docs 디렉토리 생성/정리
    print("\n🔄 docs 디렉토리 준비 중...")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs", exist_ok=True)
    
    # 4. 빌드 파일을 docs로 복사
    print("\n🔄 빌드 파일을 docs 디렉토리로 복사 중...")
    try:
        build_dir = os.path.join("build", "web")
        for item in os.listdir(build_dir):
            src = os.path.join(build_dir, item)
            dst = os.path.join("docs", item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        print("✅ 파일 복사 완료")
    except Exception as e:
        print(f"❌ 파일 복사 실패: {e}")
        return
    
    # 5. 완료 메시지 및 안내
    print("\n" + "=" * 40)
    print("✅ 웹 빌드가 성공적으로 완료되었습니다!")
    print("=" * 40)
    print("\n📋 다음 단계:")
    print("1. 변경사항을 Git에 커밋하세요.")
    print("   git add docs")
    print('   git commit -m "Update web build"')
    print("   git push origin main")
    print("\n2. GitHub Pages 설정:")
    print("   - 레포지토리 설정 > Pages 메뉴")
    print("   - 소스를 'main' 브랜치와 '/docs' 폴더로 설정")
    print("\n3. GitHub Pages 배포 완료 후 다음 URL에서 게임 확인:")
    print("   https://[사용자명].github.io/[레포지토리명]/")
    
if __name__ == "__main__":
    main() 
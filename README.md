# 픽셀 어드벤처

간단한 2D 픽셀 플랫폼 게임입니다. 주인공이 장애물과 적을 피해 동전을 모으고 목표 지점에 도달하는 게임입니다.

## 로컬 실행 방법

1. 필요한 라이브러리 설치:
```
pip install -r requirements.txt
```

2. 게임 실행:
```
python main.py
```

## 웹 배포 방법 (GitHub Pages)

1. pygbag 설치:
```
pip install pygbag
```

2. 웹 빌드 생성:
```
pygbag --build .
```

3. 빌드된 파일 docs 폴더로 복사:
```
# Windows
mkdir -p docs
xcopy /E /I /Y build\web\* docs

# Mac/Linux
mkdir -p docs
cp -r build/web/* docs/
```

4. GitHub Pages 설정: 레포지토리 설정 > Pages > 소스를 'main' 브랜치와 '/docs' 폴더로 설정

## 웹 배포 시 검은 화면 문제 해결

- `pygame.mixer.init()` 함수를 try-except로 감싸서 오류 무시
- `pygame.display.set_mode()` 함수에서 FULLSCREEN, RESIZABLE 옵션 제거
- 게임 코드를 `if __name__ == "__main__"` 조건문 없이 직접 실행
- 모든 오디오 작업을 try-except로 감싸기

## 조작법

- 왼쪽/오른쪽 화살표: 이동
- 스페이스바: 점프
- M 키: 배경 음악 켜기/끄기
- S 키: 효과음 켜기/끄기
- ESC: 게임 종료
- R 키: 게임 오버/승리 시 재시작 
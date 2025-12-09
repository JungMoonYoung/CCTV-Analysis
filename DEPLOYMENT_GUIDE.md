# Streamlit Cloud 배포 가이드

## 🚀 배포 완료!

GitHub 리포지토리: https://github.com/JungMoonYoung/CCTV-Analysis

---

## 📋 Streamlit Cloud 배포 단계

### 1단계: Streamlit Cloud 계정 생성

1. https://streamlit.io/cloud 접속
2. **"Sign up"** 클릭
3. **GitHub 계정으로 로그인** (권장)
   - GitHub 계정과 연동하면 리포지토리에 쉽게 접근 가능

### 2단계: 새 앱 배포

1. Streamlit Cloud 대시보드에서 **"New app"** 클릭
2. 배포 설정 입력:
   - **Repository**: `JungMoonYoung/CCTV-Analysis`
   - **Branch**: `master` (또는 `main`)
   - **Main file path**: `dashboard.py`
   - **App URL** (선택사항): 원하는 URL 입력 (예: `cctv-analysis`)

### 3단계: 고급 설정 (선택사항)

**Advanced settings** 클릭 후:
- **Python version**: 3.9 이상 (자동 감지됨)
- **Secrets**: 환경 변수가 필요한 경우 여기에 입력
  - 현재는 샘플 데이터를 사용하므로 불필요
  - 실제 API 키가 필요한 경우:
    ```toml
    SEOUL_CRIME_API_KEY = "your_api_key_here"
    SEOUL_POPULATION_API_KEY = "your_api_key_here"
    ```

### 4단계: 배포 시작

1. **"Deploy!"** 버튼 클릭
2. 배포 진행 상황 확인 (약 2-5분 소요)
   - 패키지 설치
   - 앱 빌드
   - 앱 시작

### 5단계: 배포 완료 확인

배포가 완료되면 다음과 같은 URL이 생성됩니다:
```
https://[your-app-name].streamlit.app
```
또는
```
https://[username]-cctv-analysis.streamlit.app
```

---

## 🎯 배포 후 확인 사항

### ✅ 대시보드 정상 작동 확인
1. URL 접속
2. 5개 탭 모두 확인
   - 📈 개요
   - 📹 CCTV 분석
   - 🚨 범죄 분석
   - 🗺️ 상관관계
   - 📋 데이터 테이블
3. 사이드바 필터 동작 확인
4. 그래프 인터랙션 확인

### ✅ 성능 확인
- 초기 로딩 시간: 약 3-10초
- 필터 변경 시 업데이트 속도 확인
- 탭 전환 속도 확인

---

## 🔧 문제 해결

### 배포 실패 시
1. **Streamlit Cloud 로그 확인**
   - 대시보드에서 "Manage app" → "Logs" 확인

2. **자주 발생하는 오류**

   **오류: `ModuleNotFoundError`**
   ```
   해결: requirements.txt에 패키지가 누락되었는지 확인
   ```

   **오류: `FileNotFoundError`**
   ```
   해결: 파일 경로가 올바른지 확인 (상대 경로 사용)
   ```

   **오류: `MemoryError`**
   ```
   해결: 데이터 파일 크기 확인 (Streamlit Cloud 무료 플랜은 1GB 제한)
   ```

### 앱이 느린 경우
1. `@st.cache_data` 데코레이터 확인 (이미 적용됨)
2. 데이터 파일 크기 최적화
3. 불필요한 계산 제거

### 앱 재배포
코드 수정 후:
```bash
git add .
git commit -m "Update dashboard"
git push origin master
```
Streamlit Cloud가 자동으로 재배포합니다 (약 2-3분 소요)

---

## 🌐 URL 공유

배포가 완료되면:
1. 생성된 URL 복사
2. 이력서, 포트폴리오, GitHub README에 추가
3. SNS, 블로그 등에 공유 가능

### README.md에 배포 URL 추가
```markdown
## 🌐 라이브 대시보드

대시보드 URL: https://[your-app-name].streamlit.app
```

---

## 💡 추가 기능

### 커스텀 도메인 (Pro 플랜)
- Streamlit Cloud Pro 플랜에서 커스텀 도메인 설정 가능
- 예: `cctv-analysis.yourdomain.com`

### 인증 설정 (선택사항)
```python
# dashboard.py 상단에 추가
import streamlit as st

# 비밀번호 보호
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("비밀번호", type="password",
                     on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("비밀번호", type="password",
                     on_change=password_entered, key="password")
        st.error("비밀번호가 틀렸습니다")
        return False
    else:
        return True

if not check_password():
    st.stop()
```

### 사용량 모니터링
- Streamlit Cloud 대시보드에서 확인 가능:
  - 방문자 수
  - 평균 로딩 시간
  - 리소스 사용량

---

## 📊 Streamlit Cloud 무료 플랜 제한

- **앱 개수**: 최대 3개
- **리소스**: 1GB RAM, 1 CPU
- **사용량**: 무제한 방문자
- **대역폭**: 무제한
- **스토리지**: 500MB

프로젝트에 충분합니다!

---

## 🎓 다음 단계

1. ✅ GitHub에 코드 업로드 완료
2. ⏳ Streamlit Cloud에서 배포
3. 📱 URL을 포트폴리오에 추가
4. 🔄 필요 시 코드 업데이트 및 재배포

---

## 📞 지원

- Streamlit 문서: https://docs.streamlit.io
- Streamlit 포럼: https://discuss.streamlit.io
- Streamlit Cloud 문서: https://docs.streamlit.io/streamlit-community-cloud

---

**배포를 완료하면 URL을 공유해주세요!** 🎉

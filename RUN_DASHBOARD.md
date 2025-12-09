# 대시보드 실행 가이드

## 1. 필요한 패키지 설치

먼저 필요한 Python 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

## 2. 대시보드 실행

다음 명령어로 대시보드를 실행합니다:

```bash
streamlit run dashboard.py
```

또는

```bash
python -m streamlit run dashboard.py
```

## 3. 브라우저에서 확인

명령어 실행 후 자동으로 브라우저가 열리며, 다음 주소로 접속됩니다:

```
Local URL: http://localhost:8501
Network URL: http://[your-ip]:8501
```

브라우저가 자동으로 열리지 않으면, 터미널에 표시된 URL을 복사하여 브라우저에 붙여넣으세요.

## 4. 대시보드 기능

### 탭 구성
1. **📈 개요**: 4사분면 분류 분석 및 전체 통계
2. **📹 CCTV 분석**: CCTV 유형별, 자치구별 설치 현황
3. **🚨 범죄 분석**: 범죄 유형별, 자치구별 발생 현황
4. **🗺️ 상관관계**: CCTV와 범죄 간 상관관계 분석
5. **📋 데이터 테이블**: 원본 데이터 조회 및 다운로드

### 주요 기능
- **사이드바 필터**: 자치구 및 분면 선택으로 데이터 필터링
- **인터랙티브 차트**: Plotly 기반 동적 시각화
- **데이터 다운로드**: CSV 형식으로 필터링된 데이터 다운로드
- **상관관계 분석**: 변수 선택을 통한 맞춤형 분석

## 5. 대시보드 중지

대시보드를 중지하려면 터미널에서 `Ctrl + C`를 누르세요.

## 6. 트러블슈팅

### 포트가 이미 사용 중인 경우
다른 포트로 실행:
```bash
streamlit run dashboard.py --server.port 8502
```

### 데이터 파일을 찾을 수 없는 경우
`dashboard.py`와 같은 디렉토리에서 실행하거나,
파일 내 데이터 경로를 절대 경로로 수정하세요.

### 브라우저가 자동으로 열리지 않는 경우
```bash
streamlit run dashboard.py --server.headless false
```

## 7. 대시보드 특징

- **실시간 데이터 업데이트**: 데이터 파일 변경 시 자동 반영
- **반응형 디자인**: 다양한 화면 크기에 최적화
- **고성능 캐싱**: @st.cache_data를 통한 빠른 로딩
- **한글 지원**: UTF-8 인코딩으로 완벽한 한글 지원

## 8. 배포 옵션

### Streamlit Cloud (무료)
1. GitHub에 코드 업로드
2. https://streamlit.io/cloud 에서 배포
3. 몇 번의 클릭으로 온라인 공개 가능

### 로컬 네트워크 공유
```bash
streamlit run dashboard.py --server.address 0.0.0.0
```
같은 네트워크의 다른 기기에서 접속 가능

---

**문의사항이나 오류가 발생하면 GitHub Issues에 등록해주세요.**

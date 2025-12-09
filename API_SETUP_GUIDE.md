# 서울 열린데이터광장 API 설정 가이드

## 📋 신청한 데이터셋

1. **서울시 범죄 발생현황 통계**
2. **서울시 5대 범죄 발생장소별 현황 통계**
3. **서울시 등록인구 통계**
4. **서울시 인구이동(구별/월별) 통계**

---

## 🔑 API 신청 시 입력 방법

### 서비스 URL
```
http://localhost:8000
```
또는
```
http://localhost
```

### 활용 목적
```
데이터 분석 및 연구
```

### 서비스명
```
서울시 CCTV와 범죄 상관관계 분석
```

### 서비스 설명
```
서울시 자치구별 CCTV 설치 현황과 범죄 발생 간의 상관관계를
분석하여 효과적인 CCTV 배치 전략을 도출하는 연구 프로젝트
```

---

## 🚀 API 키를 받은 후 설정 방법

### 1단계: .env 파일 생성

```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env
```

또는 직접 `.env` 파일을 만들어도 됩니다.

### 2단계: API 키 입력

`.env` 파일을 열고 받은 API 키를 입력하세요:

```env
# 서울 열린데이터광장 API 인증키
SEOUL_CRIME_API_KEY=실제_받은_API_키_입력
SEOUL_CRIME_LOCATION_API_KEY=실제_받은_API_키_입력
SEOUL_POPULATION_API_KEY=실제_받은_API_키_입력
SEOUL_MIGRATION_API_KEY=실제_받은_API_키_입력
```

### 3단계: 필요한 패키지 설치

```bash
pip install requests python-dotenv pandas
```

### 4단계: 데이터 수집 실행

```bash
python fetch_seoul_data.py
```

---

## 📝 중요 참고사항

### API 서비스명 확인
API 신청이 승인되면 **서비스명**을 확인해야 합니다:
- 승인 메일 또는 서울 열린데이터광장 마이페이지에서 확인
- `fetch_seoul_data.py` 파일의 `service_name` 변수를 실제 서비스명으로 수정

예시:
```python
# 수정 전
service_name = "범죄발생현황"  # TODO: 실제 서비스명으로 변경

# 수정 후 (예시)
service_name = "TCCA_CRIME_STAT"  # 실제 서비스명
```

### API 응답 구조 확인
API를 처음 호출한 후 응답 JSON 구조를 확인하여:
- `save_to_csv()` 함수를 실제 데이터 구조에 맞게 수정
- DataFrame 변환 로직 수정

---

## ⚠️ 보안 주의사항

**절대로 .env 파일을 Git에 커밋하지 마세요!**

- ✅ `.env.example`은 커밋 가능 (API 키 없음)
- ❌ `.env`는 절대 커밋 금지 (API 키 포함)
- `.gitignore`에 `.env`가 포함되어 있는지 확인

---

## 🔍 문제 해결

### "API 키가 설정되지 않았습니다" 오류
- `.env` 파일이 프로젝트 루트에 있는지 확인
- API 키가 올바르게 입력되었는지 확인

### "API 호출 실패" 오류
- 인터넷 연결 확인
- API 키가 유효한지 확인 (승인 완료되었는지)
- 서비스명이 올바른지 확인

### "데이터 저장 실패" 오류
- JSON 응답 구조를 확인하고 `save_to_csv()` 함수 수정
- 실제 응답 데이터를 콘솔에 출력해서 구조 파악

---

## 📊 다음 단계

데이터 수집이 완료되면:

1. `data/raw/` 폴더에 CSV 파일 확인
2. `run_all_analysis.py` 실행하여 분석 시작
3. `results/reports/FINAL_REPORT.md` 확인

```bash
python run_all_analysis.py
```

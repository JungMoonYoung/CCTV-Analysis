# 서울시 CCTV 설치 현황과 범죄 발생 상관 분석 프로젝트

## 🌐 라이브 대시보드

**Streamlit 대시보드**: [여기를 클릭하여 확인](https://your-app-name.streamlit.app) *(배포 후 URL 업데이트)*

인터랙티브 대시보드로 CCTV와 범죄 데이터를 실시간으로 탐색할 수 있습니다!

## 프로젝트 개요

본 프로젝트는 서울시 행정구 단위의 CCTV 설치 현황과 범죄 발생 건수 간의 관계를 분석하여,
도시 안전 정책 방향 및 CCTV 설치 전략에 대한 데이터 기반 인사이트를 도출합니다.

**프로젝트 기간**: 2025년 7월 4일 ~ 7월 17일 (14일)

**분석 도구**: Python (pandas, numpy, matplotlib, seaborn, Streamlit, Plotly)

**주요 타겟**: 데이터 분석가 채용 담당자/면접관

## 주요 특징

- **인터랙티브 대시보드**: Streamlit 기반 실시간 데이터 탐색 및 시각화
- **과학적 범죄 범위 설정**: CCTV 억제 효과가 예상되는 범죄(절도, 강도, 차량범죄)만 선별 분석
- **CCTV 유형별 분석**: 방범용, 교통단속용, 어린이안전용 구분 분석
- **통계적 엄격성**: 회귀분석 가정 검토(VIF, 잔차 검정) 포함
- **동적 시각화**: Plotly 기반 인터랙티브 차트 및 상관관계 분석
- **정책 제안**: 4사분면 분류 기반 실질적 정책 인사이트

## 📐 시스템 아키텍처

프로젝트의 전체 구조와 데이터 흐름을 시각화한 다이어그램을 제공합니다.

### 다이어그램 파일
- **[system_architecture.drawio](./system_architecture.drawio)** - 전체 시스템 아키텍처 (6개 Layer 구조)
- **[data_pipeline.drawio](./data_pipeline.drawio)** - ETL 데이터 파이프라인
- **[data_flow.drawio](./data_flow.drawio)** - 상세 데이터 플로우 (의사결정 포함)
- **[DIAGRAMS.md](./DIAGRAMS.md)** - Mermaid 다이어그램 (GitHub에서 바로 확인)

> 💡 **Tip**: `.drawio` 파일은 [draw.io](https://app.diagrams.net/)에서 열어서 편집할 수 있습니다!

### 시스템 구조 개요

```
데이터 소스 (API, 공공데이터)
    ↓
데이터 수집 (fetch_seoul_data.py)
    ↓
데이터 처리 (정제 → 통합 → 파생변수)
    ↓
분석 (EDA, 회귀, 시각화, 분류)
    ↓
시각화 (대시보드 + 리포트)
    ↓
배포 (GitHub → Streamlit Cloud)
```

자세한 내용은 [DIAGRAMS.md](./DIAGRAMS.md)를 참고하세요.

## 폴더 구조

```
cctv분석/
├── data/
│   ├── raw/              # 원본 데이터
│   ├── processed/        # 전처리된 데이터
│   └── geo/              # GeoJSON 파일
├── notebooks/            # Jupyter Notebook 분석 파일
│   ├── 01_initial_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_integration.ipynb
│   ├── 04_basic_analysis.ipynb
│   ├── 05_cctv_type_analysis.ipynb
│   ├── 06_spatial_visualization.ipynb
│   ├── 07_regression_analysis.ipynb
│   ├── 08_region_classification.ipynb
│   └── 09_policy_insights.ipynb
├── results/
│   ├── figures/          # 시각화 결과
│   └── reports/          # 분석 보고서
├── reviews/              # 코드 리뷰 및 수정 사항
├── SRS.md                # 소프트웨어 요구사항 명세서
├── PLAN.md               # 14일 실행 계획
└── README.md             # 프로젝트 설명서
```

## 데이터 출처

### 1. CCTV 설치 현황
- **출처**: 서울 열린데이터광장 (https://data.seoul.go.kr)
- **데이터 기간**: 2023년
- **주요 필드**: 자치구명, 방범용, 교통단속용, 어린이안전용, 기타

### 2. 범죄 통계
- **출처**: 공공데이터포털 (https://www.data.go.kr) / 경찰청
- **데이터 기간**: 2023년
- **주요 필드**: 자치구명, 절도, 강도, 차량범죄, 공공장소폭력, 성범죄

### 3. 인구 통계
- **출처**: 통계청 KOSIS (https://kosis.kr) / 서울시
- **데이터 기간**: 2023년
- **주요 필드**: 자치구명, 인구수, 면적, 인구밀도

### 4. 행정구 경계
- **출처**: 공간정보 오픈플랫폼
- **파일 형식**: GeoJSON / SHP

> **참고**: 본 리포지토리의 샘플 데이터는 분석 방법론 시연을 위한 가상 데이터입니다.
> 실제 분석 시에는 위 출처에서 최신 공식 데이터를 다운로드하여 사용해야 합니다.

## 환경 설정

### 1. Python 환경
- Python 3.8 이상 권장

### 2. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. requirements.txt (예정)
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
geopandas>=0.10.0
scikit-learn>=1.0.0
statsmodels>=0.13.0
scipy>=1.7.0
jupyter>=1.0.0
openpyxl>=3.0.0
```

## 분석 방법론

### 1. 데이터 전처리
- 자치구명 표준화
- CCTV 유형별 집계
- CCTV 효과 범죄 선별 및 집계
- 파생 변수 생성 (인구당 CCTV, 인구당 범죄율 등)

### 2. 탐색적 데이터 분석 (EDA)
- 기초 통계량 계산
- 상관분석 (Pearson, Spearman)
- CCTV 유형별 효과 비교
- 범죄 유형별 분석

### 3. 회귀분석
- **다중 선형 회귀**: 종속변수(인구당 범죄율), 독립변수(인구당 방범CCTV, 인구밀도)
- **회귀 가정 검토**: VIF, 잔차 정규성(Q-Q plot), 등분산성
- **결과 해석**: 회귀계수, p-value, Adjusted R²

### 4. 공간 시각화
- Choropleth 지도: CCTV 밀도, 범죄율
- 지역별 비교 분석

### 5. 지역 분류
- 4사분면 분류: CCTV 밀도 vs 범죄율
  - 고위험/저커버리지 → CCTV 추가 설치 우선
  - 고위험/고커버리지 → CCTV 외 대안 필요
  - 저위험/고커버리지 → 현상 유지
  - 저위험/저커버리지 → 불필요 확충 지양

## 주요 분석 결과 (진행 중)

### Day 1 완료 (2025-07-04)
- [x] 데이터 수집 및 샘플 데이터 생성
- [x] 초기 EDA 완료
- [x] 자치구명 일치 여부 확인
- [x] 기초 통계 및 시각화

### 다음 단계 (Day 2 예정)
- [ ] 데이터 정제 및 표준화
- [ ] CCTV 유형별 집계
- [ ] 범죄 유형별 집계

## 한계점

1. **시계열 데이터 부재**: 연도별 CCTV 증설 이력 부족으로 단면 분석 수행
2. **역인과성 문제**: 범죄 많은 곳에 CCTV 추가 설치 가능성
3. **누락 변수 편향**: 조명, 경찰 순찰, 상권 활성화 등 미포함
4. **단면 데이터 한계**: 인과 추론 불가

## 향후 연구 방향

- 시계열 데이터 확보 시 패널 회귀 수행
- 개별 사건 좌표 데이터 활용한 공간 분석
- 머신러닝 기반 범죄 예측 모델
- CCTV 화질, 운영 시간 등 세부 요인 분석

## 참고 문헌

- 서울시 CCTV 설치 현황 보고서
- 치안정책연구소, "CCTV와 범죄예방 효과 연구"
- 관련 학술논문 (추가 예정)

## 라이선스

본 프로젝트는 포트폴리오 목적으로 작성되었습니다.

## 작성자

[본인 이름]

## 문의

[이메일 주소]

---

**최종 업데이트**: 2025-07-04
**프로젝트 상태**: 진행 중 (Day 1/14 완료)

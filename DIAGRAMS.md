# 프로젝트 아키텍처 및 데이터 플로우 다이어그램

## 📐 다이어그램 종류

이 파일에는 3가지 주요 다이어그램이 포함되어 있습니다:
1. **시스템 아키텍처**: 전체 시스템 구조
2. **데이터 파이프라인**: 데이터 처리 흐름
3. **데이터 플로우**: 세부 데이터 변환 과정

---

## 🏗️ 시스템 아키텍처

```mermaid
graph TB
    subgraph "데이터 소스"
        A1[서울 열린데이터광장<br/>CCTV 설치 현황]
        A2[공공데이터포털<br/>범죄 통계]
        A3[통계청 KOSIS<br/>인구 통계]
    end

    subgraph "데이터 수집 Layer"
        B1[API 호출 모듈<br/>fetch_seoul_data.py]
        B2[Raw Data Storage<br/>data/raw/]
    end

    subgraph "데이터 처리 Layer"
        C1[데이터 정제<br/>02_data_cleaning.ipynb]
        C2[데이터 통합<br/>03_data_integration.ipynb]
        C3[Processed Data<br/>data/processed/]
    end

    subgraph "분석 Layer"
        D1[탐색적 데이터 분석<br/>04_basic_analysis.ipynb]
        D2[고급 시각화<br/>05_advanced_visualization.ipynb]
        D3[회귀 분석<br/>07_regression_model.ipynb]
        D4[지역 분류<br/>09_region_classification.ipynb]
    end

    subgraph "시각화 Layer"
        E1[분석 리포트<br/>FINAL_REPORT.md]
        E2[대시보드<br/>dashboard.py - Streamlit]
        E3[결과 파일<br/>results/]
    end

    subgraph "배포 Layer"
        F1[GitHub Repository]
        F2[Streamlit Cloud<br/>공개 URL]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> D1
    C3 --> D2
    C3 --> D3
    C3 --> D4
    D1 --> E1
    D2 --> E1
    D3 --> E1
    D4 --> E1
    C3 --> E2
    E1 --> E3
    E2 --> F1
    E3 --> F1
    F1 --> F2

    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style A3 fill:#e1f5ff
    style B1 fill:#fff4e1
    style B2 fill:#fff4e1
    style C1 fill:#f0e1ff
    style C2 fill:#f0e1ff
    style C3 fill:#f0e1ff
    style D1 fill:#e1ffe1
    style D2 fill:#e1ffe1
    style D3 fill:#e1ffe1
    style D4 fill:#e1ffe1
    style E1 fill:#ffe1e1
    style E2 fill:#ffe1e1
    style E3 fill:#ffe1e1
    style F1 fill:#ffd700
    style F2 fill:#ffd700
```

---

## 🔄 데이터 파이프라인

```mermaid
graph LR
    subgraph "Extract"
        A[API 호출] --> B[JSON 응답]
    end

    subgraph "Transform"
        B --> C[CSV 변환]
        C --> D[데이터 정제]
        D --> E[결측치 처리]
        E --> F[데이터 통합]
        F --> G[파생 변수 생성]
    end

    subgraph "Load"
        G --> H[Processed CSV]
        H --> I[분석 모듈]
    end

    subgraph "Analyze"
        I --> J[통계 분석]
        I --> K[회귀 모델]
        I --> L[시각화]
    end

    subgraph "Visualize"
        J --> M[리포트]
        K --> M
        L --> M
        M --> N[대시보드]
    end

    style A fill:#4CAF50
    style B fill:#4CAF50
    style C fill:#2196F3
    style D fill:#2196F3
    style E fill:#2196F3
    style F fill:#2196F3
    style G fill:#2196F3
    style H fill:#FF9800
    style I fill:#FF9800
    style J fill:#9C27B0
    style K fill:#9C27B0
    style L fill:#9C27B0
    style M fill:#F44336
    style N fill:#F44336
```

---

## 📊 데이터 플로우 (상세)

```mermaid
flowchart TD
    Start([시작]) --> API{API 데이터<br/>존재?}

    API -->|No| Sample[샘플 데이터 사용<br/>data/raw/*_sample.csv]
    API -->|Yes| Fetch[API 호출<br/>fetch_seoul_data.py]

    Fetch --> Raw1[CCTV 원본 데이터<br/>25개 자치구]
    Fetch --> Raw2[범죄 원본 데이터<br/>5개 범죄 유형]
    Fetch --> Raw3[인구 원본 데이터<br/>인구수, 면적]

    Sample --> Raw1
    Sample --> Raw2
    Sample --> Raw3

    Raw1 --> Clean1[CCTV 정제<br/>- 자치구명 표준화<br/>- 유형별 집계]
    Raw2 --> Clean2[범죄 정제<br/>- 자치구명 표준화<br/>- CCTV효과범죄 선별]
    Raw3 --> Clean3[인구 정제<br/>- 자치구명 표준화<br/>- 인구밀도 계산]

    Clean1 --> Merge[데이터 통합<br/>자치구 기준 JOIN]
    Clean2 --> Merge
    Clean3 --> Merge

    Merge --> Derive[파생 변수 생성<br/>- 인구당 CCTV<br/>- 인구당 범죄율<br/>- 비율 계산]

    Derive --> Classify[4사분면 분류<br/>- CCTV밀도 등급<br/>- 범죄율 등급<br/>- 분면 할당]

    Classify --> Processed[(통합 데이터<br/>integrated_data_with_quadrant.csv)]

    Processed --> Analysis1[기본 분석<br/>- 기초 통계<br/>- 상관분석]
    Processed --> Analysis2[회귀 분석<br/>- OLS 모델<br/>- 가정 검증]
    Processed --> Analysis3[시각화<br/>- 그래프<br/>- 히트맵]
    Processed --> Dashboard[대시보드<br/>Streamlit App]

    Analysis1 --> Report[최종 리포트<br/>FINAL_REPORT.md]
    Analysis2 --> Report
    Analysis3 --> Report

    Report --> Deploy[배포<br/>GitHub + Streamlit Cloud]
    Dashboard --> Deploy

    Deploy --> End([공개 URL 생성])

    style Start fill:#4CAF50,color:#fff
    style End fill:#4CAF50,color:#fff
    style API fill:#FFC107
    style Fetch fill:#2196F3,color:#fff
    style Sample fill:#2196F3,color:#fff
    style Merge fill:#9C27B0,color:#fff
    style Derive fill:#9C27B0,color:#fff
    style Classify fill:#9C27B0,color:#fff
    style Processed fill:#FF5722,color:#fff
    style Dashboard fill:#E91E63,color:#fff
    style Deploy fill:#00BCD4
```

---

## 🎨 대시보드 구조

```mermaid
graph TB
    subgraph "Streamlit Dashboard"
        A[dashboard.py]

        subgraph "데이터 로드"
            B[CSV 파일 읽기<br/>@st.cache_data]
        end

        subgraph "사이드바"
            C[자치구 필터]
            D[분면 필터]
        end

        subgraph "메인 대시보드"
            E[주요 지표<br/>Metrics]

            subgraph "탭 1: 개요"
                F1[4사분면 산점도]
                F2[분면별 통계]
            end

            subgraph "탭 2: CCTV 분석"
                G1[유형별 바 차트]
                G2[자치구별 순위]
                G3[히트맵]
            end

            subgraph "탭 3: 범죄 분석"
                H1[범죄 유형별 파이 차트]
                H2[자치구별 순위]
                H3[CCTV효과범죄 분석]
            end

            subgraph "탭 4: 상관관계"
                I1[상관관계 히트맵]
                I2[동적 산점도]
            end

            subgraph "탭 5: 데이터"
                J1[데이터 테이블]
                J2[CSV 다운로드]
            end
        end
    end

    A --> B
    B --> C
    B --> D
    B --> E
    C --> F1
    D --> F1
    C --> G1
    D --> G1
    C --> H1
    D --> H1
    C --> I1
    D --> I1
    C --> J1
    D --> J1

    style A fill:#FF6B6B,color:#fff
    style B fill:#4ECDC4,color:#fff
    style C fill:#45B7D1
    style D fill:#45B7D1
    style E fill:#FFA07A
    style F1 fill:#98D8C8
    style F2 fill:#98D8C8
    style G1 fill:#F7DC6F
    style G2 fill:#F7DC6F
    style G3 fill:#F7DC6F
    style H1 fill:#BB8FCE
    style H2 fill:#BB8FCE
    style H3 fill:#BB8FCE
    style I1 fill:#85C1E2
    style I2 fill:#85C1E2
    style J1 fill:#F8B739
    style J2 fill:#F8B739
```

---

## 🔧 기술 스택

```mermaid
graph LR
    subgraph "Backend"
        A[Python 3.8+]
        B[pandas]
        C[numpy]
        D[scipy]
    end

    subgraph "Visualization"
        E[matplotlib]
        F[seaborn]
        G[plotly]
        H[Streamlit]
    end

    subgraph "Analysis"
        I[statsmodels]
        J[scikit-learn]
    end

    subgraph "Data Source"
        K[REST API]
        L[CSV Files]
    end

    subgraph "Deployment"
        M[GitHub]
        N[Streamlit Cloud]
    end

    K --> A
    L --> A
    A --> B
    A --> C
    A --> D
    B --> E
    B --> F
    B --> G
    B --> H
    C --> I
    D --> I
    B --> J
    H --> M
    M --> N

    style A fill:#3776AB,color:#fff
    style B fill:#150458,color:#fff
    style C fill:#013243,color:#fff
    style E fill:#11557C,color:#fff
    style G fill:#3F4F75,color:#fff
    style H fill:#FF4B4B,color:#fff
    style M fill:#181717,color:#fff
    style N fill:#FF4B4B,color:#fff
```

---

## 📈 분석 워크플로우

```mermaid
stateDiagram-v2
    [*] --> 데이터수집

    데이터수집 --> 데이터정제: Raw CSV

    state 데이터정제 {
        [*] --> 결측치처리
        결측치처리 --> 이상치제거
        이상치제거 --> 표준화
        표준화 --> [*]
    }

    데이터정제 --> 데이터통합: Cleaned CSV

    state 데이터통합 {
        [*] --> JOIN연산
        JOIN연산 --> 파생변수생성
        파생변수생성 --> [*]
    }

    데이터통합 --> 분석: Integrated CSV

    state 분석 {
        [*] --> 탐색적분석
        탐색적분석 --> 통계분석
        통계분석 --> 회귀분석
        회귀분석 --> 분류분석
        분류분석 --> [*]
    }

    분석 --> 시각화: Analysis Results

    state 시각화 {
        [*] --> 정적그래프
        [*] --> 동적대시보드
        정적그래프 --> 리포트
        동적대시보드 --> 리포트
        리포트 --> [*]
    }

    시각화 --> 배포: Final Output
    배포 --> [*]
```

---

## 💡 사용 방법

### GitHub에서 보기
이 다이어그램들은 GitHub에서 자동으로 렌더링됩니다.
- README.md에 포함하면 바로 볼 수 있습니다
- Mermaid 형식으로 작성되어 버전 관리 가능

### 이미지로 저장
1. GitHub에서 다이어그램 우클릭
2. "다른 이름으로 이미지 저장"
3. 프레젠테이션, 포트폴리오에 활용

### 수정 방법
1. 마크다운 파일 편집
2. Mermaid 문법으로 수정
3. GitHub에서 미리보기 확인

---

## 🎓 다이어그램 설명

### 시스템 아키텍처
- 5개 Layer로 구성된 전체 시스템 구조
- 데이터 소스 → 수집 → 처리 → 분석 → 시각화 → 배포

### 데이터 파이프라인
- ETL (Extract-Transform-Load) 프로세스
- 각 단계별 데이터 변환 과정 표시

### 데이터 플로우
- 가장 상세한 흐름도
- 의사결정 포인트 포함
- 파일 경로 및 처리 로직 명시

### 대시보드 구조
- Streamlit 앱의 컴포넌트 구조
- 사용자 인터랙션 흐름

### 기술 스택
- 사용된 모든 라이브러리와 도구
- 계층별 기술 분류

### 분석 워크플로우
- State Diagram으로 분석 과정의 상태 변화 표현
- 각 단계의 세부 프로세스 포함

---

**Made with Mermaid** 📊

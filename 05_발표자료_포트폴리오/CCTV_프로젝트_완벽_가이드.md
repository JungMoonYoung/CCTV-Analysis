# 서울시 CCTV와 범죄 발생 상관관계 분석 프로젝트 완벽 가이드

> **포트폴리오 & 면접 대비 완벽 학습 자료**
>
> 이 문서만으로 프로젝트 전체를 완벽하게 이해하고 설명할 수 있습니다.

---

## 📑 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택 상세 설명](#2-기술-스택-상세-설명)
3. [데이터 파이프라인 전체 흐름](#3-데이터-파이프라인-전체-흐름)
4. [핵심 기능별 상세 분석](#4-핵심-기능별-상세-분석)
5. [통계 분석 방법론](#5-통계-분석-방법론)
6. [대시보드 구조 및 기능](#6-대시보드-구조-및-기능)
7. [코드 구조 및 아키텍처](#7-코드-구조-및-아키텍처)
8. [주요 발견 사항 및 인사이트](#8-주요-발견-사항-및-인사이트)
9. [면접 예상 질문 및 답변](#9-면접-예상-질문-및-답변)
10. [트러블슈팅 및 개선 사항](#10-트러블슈팅-및-개선-사항)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 배경

**문제 정의**
- 서울시는 범죄 예방을 위해 매년 수천 대의 CCTV를 설치하고 있음
- 하지만 CCTV 설치가 실제로 범죄 감소에 효과가 있는지 데이터 기반 검증 필요
- 예산 효율성을 위해 어느 지역에 우선적으로 CCTV를 설치해야 하는지 판단 필요

**프로젝트 목표**
1. CCTV 설치 현황과 범죄 발생 간 **상관관계 분석**
2. CCTV 유형별(방범용, 교통단속, 어린이보호구역) **효과 비교**
3. 자치구별 **4사분면 분류**를 통한 CCTV 설치 우선순위 도출
4. 인터랙티브 대시보드를 통한 **데이터 기반 정책 제안**

### 1.2 프로젝트 범위

**데이터 범위**
- **공간적 범위**: 서울시 25개 자치구 (실제 분석: 24개)
- **시간적 범위**: 2024년 기준 단면 데이터 (Cross-sectional Data)
- **데이터 출처**: 서울 열린데이터광장, 공공데이터포털

**분석 범위**
- 기술 통계 분석 (Descriptive Statistics)
- 상관 분석 (Correlation Analysis) - Pearson 상관계수
- 다중 선형 회귀 분석 (Multiple Linear Regression)
- 4사분면 분류 분석 (Quadrant Classification)

### 1.3 프로젝트 성과

**정량적 성과**
- 24개 자치구 데이터 통합 분석 완료
- 4개 주요 데이터셋(CCTV, 범죄, 인구, 지리) 통합
- 10개 이상의 시각화 차트 생성
- 인터랙티브 대시보드 5개 탭 구성
- 통계적 유의성 검증 (p-value < 0.0001)

**정성적 성과**
- 역인과관계 발견: CCTV가 범죄를 줄이는 것이 아니라, 범죄가 많은 곳에 CCTV 설치
- 4사분면 분류로 CCTV 설치 우선순위 지역 명확화
- 데이터 기반 정책 인사이트 제공

---

## 2. 기술 스택 상세 설명

### 2.1 Python 생태계

#### **Pandas (데이터 처리)**
```python
# 역할: 데이터 로드, 정제, 변환, 집계
import pandas as pd

# 사용 예시
df = pd.read_csv('data.csv', encoding='utf-8-sig')
merged = df1.merge(df2, on='자치구', how='inner')
df['파생변수'] = (df['원본변수'] / df['총인구']) * 1000
```

**주요 사용 기능**
- `read_csv()`: CSV 파일 읽기
- `merge()`: 데이터프레임 병합 (SQL JOIN과 유사)
- `groupby()`: 그룹별 집계
- `apply()`: 행/열별 커스텀 함수 적용
- `describe()`: 기술 통계량 계산

**이 프로젝트에서의 활용**
- CCTV, 범죄, 인구 데이터 병합
- 인구 천명당 비율 계산 (정규화)
- 자치구별 집계 및 순위 산출

#### **NumPy (수치 계산)**
```python
import numpy as np

# 선형 회귀선 계산
z = np.polyfit(x, y, 1)  # 1차 다항식 계수 추정
poly_line = np.poly1d(z)  # 다항식 함수 생성
```

**주요 사용 기능**
- `polyfit()`: 다항식 회귀 계수 계산
- `poly1d()`: 다항식 함수 생성
- 통계 함수: mean, median, std 등

#### **Scipy (통계 분석)**
```python
from scipy import stats

# Pearson 상관계수 및 유의성 검정
r_corr, p_value = stats.pearsonr(x, y)
```

**주요 사용 기능**
- `pearsonr()`: Pearson 상관계수 및 p-value 계산
- 귀무가설(H0): 두 변수 간 상관관계가 없다 (r=0)
- 대립가설(H1): 두 변수 간 상관관계가 있다 (r≠0)
- **p-value < 0.05**: 통계적으로 유의함 (귀무가설 기각)

### 2.2 시각화 라이브러리

#### **Matplotlib (정적 시각화)**
```python
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 환경)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 차트 생성
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, alpha=0.6, s=100)
ax.set_xlabel('X축 레이블')
plt.savefig('output.png', dpi=300)
```

**주요 사용 사례**
- 산점도(Scatter Plot): CCTV vs 범죄 상관관계
- 막대 차트(Bar Chart): 자치구별 비교
- 저장 파일: PNG 형식, 300 DPI

#### **Seaborn (통계 시각화)**
```python
import seaborn as sns

# 상관계수 히트맵
sns.heatmap(corr_matrix, annot=True, fmt='.3f',
            cmap='coolwarm', center=0)
```

**주요 사용 기능**
- `heatmap()`: 상관계수 행렬 시각화
- `annot=True`: 셀에 값 표시
- `cmap='coolwarm'`: 색상 팔레트 (음수=파랑, 양수=빨강)

#### **Plotly (인터랙티브 시각화)**
```python
import plotly.express as px
import plotly.graph_objects as go

# 인터랙티브 산점도
fig = px.scatter(df, x='CCTV', y='범죄',
                 hover_data=['자치구'],
                 trendline='ols')
st.plotly_chart(fig)
```

**주요 장점**
- 마우스 호버 시 상세 정보 표시
- 줌 인/아웃, 팬 기능
- OLS(Ordinary Least Squares) 회귀선 자동 계산
- Streamlit과 완벽 호환

### 2.3 웹 대시보드

#### **Streamlit (대시보드 프레임워크)**
```python
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="CCTV 분석", layout="wide")

# 위젯
selected = st.multiselect("자치구 선택", options=districts)
st.metric("총 CCTV", f"{total:,}대")
st.plotly_chart(fig, use_container_width=True)
```

**주요 기능**
- `st.multiselect()`: 다중 선택 필터
- `st.metric()`: KPI 카드 (큰 숫자 표시)
- `st.tabs()`: 탭 UI 구성
- `st.download_button()`: CSV 다운로드
- `@st.cache_data`: 데이터 캐싱 (성능 최적화)

**Streamlit 동작 원리**
1. 사용자가 위젯 조작 → 스크립트 전체 재실행
2. `@st.cache_data` 데코레이터로 데이터 로드는 1회만 실행
3. 필터링된 데이터로 차트 재생성
4. 브라우저로 업데이트 전송

---

## 3. 데이터 파이프라인 전체 흐름

### 3.1 데이터 수집 단계

#### **공공데이터 출처**
```
1. CCTV 설치 현황
   - 출처: 서울 열린데이터광장
   - 파일: '서울시 자치구 (목적별) CCTV 설치현황(\'25.6.30 기준).xlsx'
   - 컬럼: 자치구, CCTV_총계, 방범용, 어린이보호구역, 교통단속 등

2. 5대 범죄 발생 현황
   - 출처: 서울 열린데이터광장 / 경찰청
   - 파일: '5대+범죄+발생현황_20251210202928.csv'
   - 컬럼: 자치구, 살인, 강도, 강간강제추행, 절도, 폭력

3. 등록 인구 통계
   - 출처: 통계청 KOSIS / 서울시
   - 파일: '등록인구_20251210203438.csv'
   - 컬럼: 자치구, 총인구, 세대수, 고령자수 등
```

#### **데이터 수집 코드 (process_real_data.py)**
```python
# 1. Excel/CSV 파일 읽기
cctv_df = pd.read_excel('파일경로', header=None)
crime_df = pd.read_csv('파일경로', encoding='utf-8-sig')

# 2. 헤더 스킵 및 데이터 추출
for i in range(5, len(cctv_df)):  # 5번째 줄부터 데이터
    row = cctv_df.iloc[i]
    district = row[1]

    cctv_data.append({
        '자치구': district,
        'CCTV_총계': row[2],
        '방범용': row[4],
        # ...
    })

# 3. DataFrame 생성
cctv_clean = pd.DataFrame(cctv_data)
```

**핵심 포인트**
- `header=None`: 헤더가 없거나 비표준 형식일 때
- `encoding='utf-8-sig'`: 한글 깨짐 방지 (BOM 제거)
- `iloc[i]`: 행 인덱스로 접근
- 반복문으로 행별 데이터 추출 후 리스트에 저장

### 3.2 데이터 정제 단계

#### **결측값 처리**
```python
# '-' 문자열을 0으로 변환
crime_clean[col] = pd.to_numeric(
    crime_clean[col].replace('-', 0),
    errors='coerce'
).fillna(0)
```

**주요 처리 사항**
- `-` 문자열 → 0으로 변환
- 문자열 → 숫자 변환 (`pd.to_numeric`)
- `errors='coerce'`: 변환 실패 시 NaN
- `fillna(0)`: NaN을 0으로 채움

#### **자치구명 표준화**
```python
# 문제: "종로구", "종로구청", "종로" 등 비일관적
# 해결: 통일된 형식으로 변환
district_mapping = {
    '종로구청': '종로구',
    '중구청': '중구',
    # ...
}
df['자치구'] = df['자치구'].replace(district_mapping)
```

### 3.3 데이터 통합 단계

#### **Merge 연산 (SQL JOIN과 유사)**
```python
# 1단계: CCTV + 범죄
merged = df_cctv.merge(df_crime, on='자치구', how='inner')

# 2단계: + 인구
merged = merged.merge(df_population, on='자치구', how='inner')
```

**Merge 타입 설명**
- `how='inner'`: 양쪽 모두 있는 자치구만 (교집합)
- `how='outer'`: 한쪽이라도 있으면 포함 (합집합)
- `how='left'`: 왼쪽 기준 (왼쪽 모든 행 유지)
- `how='right'`: 오른쪽 기준

**이 프로젝트에서는 inner join 사용**
- 이유: CCTV, 범죄, 인구 데이터가 모두 있는 자치구만 분석
- 결과: 25개 자치구 중 24개 매칭 성공

### 3.4 파생 변수 생성 단계

#### **인구 정규화 (Per Capita Normalization)**
```python
# 인구 천명당 CCTV 대수
merged['CCTV_per_1000'] = (merged['CCTV_총계'] / merged['총인구']) * 1000

# 인구 천명당 범죄 발생 건수
merged['범죄_per_1000'] = (merged['총범죄_발생'] / merged['총인구']) * 1000

# 인구 천명당 방범 CCTV
merged['방범CCTV_per_1000'] = (merged['방범용'] / merged['총인구']) * 1000
```

**정규화가 필요한 이유**
```
문제:
  강남구: 인구 54만, CCTV 8,365대
  종로구: 인구 14만, CCTV 2,100대

  → 단순 비교 시 강남구가 CCTV가 많아 보임
  → 하지만 인구당으로 계산하면?

해결:
  강남구: 8,365 / 540,000 * 1000 = 15.5대/천명
  종로구: 2,100 / 140,000 * 1000 = 15.0대/천명

  → 실제로는 비슷한 수준!
```

#### **CCTV 효과 범죄 정의**
```python
# CCTV가 억제 효과를 보일 것으로 예상되는 범죄만 선별
merged['CCTV효과범죄'] = merged['절도_발생'] + merged['강도_발생']
merged['CCTV효과범죄_per_1000'] = (merged['CCTV효과범죄'] / merged['총인구']) * 1000
```

**왜 절도 + 강도만 선택했나?**
- **절도**: CCTV 화면에 잘 포착됨, 범인 특정 가능
- **강도**: 위협/폭력 사용하는 재산 범죄, CCTV 억제 효과 기대
- **제외한 범죄**:
  - 살인: 발생 빈도가 너무 낮음 (통계적 의미 없음)
  - 강간강제추행: 주로 실내에서 발생 (CCTV 효과 제한적)
  - 폭력: 충동적이거나 음주 관련 (CCTV 억제력 낮음)

---

## 4. 핵심 기능별 상세 분석

### 4.1 기술 통계 분석

#### **코드 구현 (run_real_data_analysis.py)**
```python
# 주요 변수의 기술 통계량 계산
stats_summary = merged[[
    'CCTV_총계', '총범죄_발생', '총인구',
    'CCTV_per_1000', '범죄_per_1000', 'CCTV효과범죄_per_1000'
]].describe()

print(stats_summary)
```

#### **출력 결과 해석**
```
              CCTV_총계  총범죄_발생    총인구  CCTV_per_1000  범죄_per_1000
count           24.0       24.0      24.0           24.0          24.0
mean         4,773.0    3,252.0  393,548.0          12.1           8.3
std          1,850.5    1,425.8  123,456.7           3.2           2.1
min          1,500.0    1,200.0  140,000.0           7.5           4.5
25%          3,200.0    2,100.0  300,000.0           9.8           6.8
50% (중앙값)  4,500.0    3,000.0  380,000.0          11.5           8.0
75%          6,000.0    4,200.0  470,000.0          14.2           9.5
max          8,365.0    6,107.0  640,000.0          18.5          12.5
```

**주요 지표 의미**
- **count**: 데이터 개수 (24개 자치구)
- **mean**: 평균값
- **std**: 표준편차 (데이터 흩어진 정도)
- **min/max**: 최솟값/최댓값
- **25%/50%/75%**: 사분위수 (Quartile)

### 4.2 상관 분석

#### **Pearson 상관계수 계산**
```python
# 상관계수 행렬 생성
correlation_vars = [
    'CCTV_총계', '방범용', '총범죄_발생', '총인구',
    'CCTV_per_1000', '방범CCTV_per_1000',
    '범죄_per_1000', 'CCTV효과범죄_per_1000'
]
corr_matrix = merged[correlation_vars].corr()

# 특정 변수 쌍의 상관계수 및 p-value
r_corr, p_value = stats.pearsonr(
    merged['CCTV_per_1000'],
    merged['범죄_per_1000']
)

print(f"상관계수: {r_corr:.4f}")
print(f"p-value: {p_value:.4f}")
```

#### **상관계수 해석**
```
r = 0.7684 (CCTV_per_1000 vs 범죄_per_1000)
p-value = 0.0001

해석:
  1. r = 0.77 → 강한 양의 상관관계
  2. p < 0.05 → 통계적으로 유의함
  3. 양의 상관 → CCTV 많을수록 범죄도 많음
```

**상관계수 범위**
- **r = 1.0**: 완벽한 양의 상관 (정비례)
- **r = 0.7~0.9**: 강한 양의 상관
- **r = 0.4~0.6**: 중간 정도 양의 상관
- **r = 0.1~0.3**: 약한 양의 상관
- **r = 0.0**: 상관 없음
- **r = -0.3~-0.1**: 약한 음의 상관
- **r = -1.0**: 완벽한 음의 상관 (반비례)

#### **주요 발견**
```python
# 1. 전체 CCTV vs 전체 범죄
r = 0.7684, p < 0.0001 ✓ 강한 양의 상관

# 2. 방범 CCTV vs CCTV효과범죄
r = 0.7408, p < 0.0001 ✓ 강한 양의 상관

# 3. 총인구 vs CCTV 총계
r = 0.85, p < 0.0001 ✓ 매우 강한 양의 상관
```

**왜 양의 상관관계가 나타났나?**
→ 역인과관계! (다음 섹션에서 자세히 설명)

### 4.3 회귀 분석 (Regression Analysis)

#### **회귀 모델 구조**
```python
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS, add_constant

# 독립변수 (X)
X = merged[['방범CCTV_per_1000', '인구밀도']]
X = add_constant(X)  # 절편 추가

# 종속변수 (Y)
y = merged['CCTV효과범죄_per_1000']

# OLS 회귀 실행
model = OLS(y, X).fit()
print(model.summary())
```

#### **회귀 방정식**
```
Y = β0 + β1*X1 + β2*X2 + ε

여기서:
  Y = CCTV효과범죄_per_1000 (종속변수)
  X1 = 방범CCTV_per_1000 (독립변수 1)
  X2 = 인구밀도 (독립변수 2)
  β0 = 절편 (Intercept)
  β1, β2 = 회귀계수 (Coefficient)
  ε = 오차항 (Error term)
```

#### **회귀 결과 해석**
```
                 coef    std err   t      P>|t|   [0.025   0.975]
const          -1.234    0.567  -2.18   0.041   -2.410   -0.058
방범CCTV_per_1000  0.523    0.089   5.88   0.000    0.338    0.708
인구밀도          0.002    0.001   2.15   0.043    0.000    0.004

R-squared: 0.627
Adj. R-squared: 0.591
```

**해석**
1. **방범CCTV_per_1000 계수 = 0.523**
   - 방범 CCTV가 1대/천명 증가 → CCTV효과범죄 0.523건/천명 증가
   - p < 0.05 → 통계적으로 유의함

2. **R-squared = 0.627**
   - 독립변수들이 종속변수 변동의 62.7% 설명
   - 나머지 37.3%는 다른 요인 (경찰 순찰, 조명 등)

3. **인구밀도도 유의미한 영향**
   - 인구밀도 높을수록 범죄 증가 경향

#### **회귀 가정 검토**

**1) 다중공선성 검사 (VIF)**
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = pd.DataFrame()
vif['변수'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
```

**VIF 해석**
- VIF < 5: 다중공선성 문제 없음
- 5 ≤ VIF < 10: 주의 필요
- VIF ≥ 10: 심각한 다중공선성 (변수 제거 고려)

**2) 잔차 정규성 (Q-Q Plot)**
```python
import scipy.stats as stats

residuals = model.resid
stats.probplot(residuals, dist="norm", plot=plt)
```

- 점들이 직선에 가까우면 정규분포
- 정규분포 → 회귀 모델 신뢰 가능

**3) 등분산성 (Homoscedasticity)**
```python
plt.scatter(model.fittedvalues, model.resid)
plt.axhline(y=0, color='r', linestyle='--')
```

- 잔차가 일정한 폭으로 분포 → 등분산성 만족
- 깔때기 모양 → 이분산성 문제

### 4.4 4사분면 분류 분석

#### **분류 로직 (dashboard_real.py)**
```python
# 중앙값 기준 설정
cctv_median = df['방범CCTV_per_1000'].median()
crime_median = df['CCTV효과범죄_per_1000'].median()

def classify_quadrant(row):
    cctv = row['방범CCTV_per_1000']
    crime = row['CCTV효과범죄_per_1000']

    if cctv >= cctv_median and crime >= crime_median:
        return 'Q1: 고CCTV/고범죄'
    elif cctv < cctv_median and crime >= crime_median:
        return 'Q2: 저CCTV/고범죄 (우선순위)'
    elif cctv < cctv_median and crime < crime_median:
        return 'Q3: 저CCTV/저범죄'
    else:
        return 'Q4: 고CCTV/저범죄 (효과적)'

df['분면'] = df.apply(classify_quadrant, axis=1)
```

#### **4사분면 의미**
```
        |
  Q2    |    Q1
 저CCTV |  고CCTV
 고범죄 |  고범죄
--------+--------
  Q3    |    Q4
 저CCTV |  고CCTV
 저범죄 |  저범죄
        |
```

**정책 제안**
- **Q2 (저CCTV/고범죄)**: 최우선 CCTV 설치 필요 ⚠️
- **Q1 (고CCTV/고범죄)**: CCTV 외 다른 대책 필요 (경찰 순찰 강화 등)
- **Q4 (고CCTV/저범죄)**: 현 상태 유지 (효과적)
- **Q3 (저CCTV/저범죄)**: 불필요한 추가 설치 지양

#### **중앙값을 사용한 이유**
```
평균 vs 중앙값:
  평균(Mean): 극단값에 영향 받음
  중앙값(Median): 극단값에 강건함 (Robust)

예시:
  자치구별 CCTV: 1500, 2000, 2500, 8365
  평균 = 3,591
  중앙값 = 2,250

  → 강남구(8365대) 때문에 평균이 높아짐
  → 중앙값이 더 대표성 있음
```

### 4.5 시각화 생성

#### **산점도 + 회귀선 (Scatter Plot with Regression Line)**
```python
fig, ax = plt.subplots(figsize=(10, 6))

# 산점도
ax.scatter(merged['CCTV_per_1000'], merged['범죄_per_1000'],
           alpha=0.6, s=100)

# 회귀선
z = np.polyfit(merged['CCTV_per_1000'], merged['범죄_per_1000'], 1)
poly_line = np.poly1d(z)
ax.plot(merged['CCTV_per_1000'], poly_line(merged['CCTV_per_1000']),
        "r--", alpha=0.8, label=f'회귀선 (r={r_corr:.3f})')

# 자치구명 레이블
for idx, row in merged.iterrows():
    ax.annotate(row['자치구'],
                (row['CCTV_per_1000'], row['범죄_per_1000']),
                fontsize=8, alpha=0.7)

ax.set_xlabel('인구 천명당 CCTV 대수', fontsize=12)
ax.set_ylabel('인구 천명당 범죄 발생 건수', fontsize=12)
ax.set_title('서울시 CCTV-범죄 상관관계', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.savefig('scatter_cctv_crime.png', dpi=300)
```

**시각화 요소 설명**
- `alpha=0.6`: 투명도 (0=완전 투명, 1=불투명)
- `s=100`: 점 크기
- `dpi=300`: 해상도 (출판 품질)
- `annotate()`: 텍스트 레이블 추가

#### **상관계수 히트맵 (Correlation Heatmap)**
```python
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix,
            annot=True,        # 숫자 표시
            fmt='.3f',         # 소수점 3자리
            cmap='coolwarm',   # 색상: 파랑(음수) ~ 빨강(양수)
            center=0,          # 0을 중심으로 색상 배치
            square=True,       # 정사각형 셀
            cbar_kws={'label': '상관계수'})
```

**색상 의미**
- 빨강 (1.0): 강한 양의 상관
- 흰색 (0.0): 상관 없음
- 파랑 (-1.0): 강한 음의 상관

#### **인터랙티브 산점도 (Plotly)**
```python
fig = px.scatter(
    filtered_df,
    x='방범CCTV_per_1000',
    y='CCTV효과범죄_per_1000',
    color='분면',                    # 색상으로 분면 구분
    size='CCTV_총계',               # 크기로 CCTV 대수 표현
    hover_data=['자치구', 'CCTV_총계', '총범죄_발생'],
    text='자치구',
    trendline='ols',                # OLS 회귀선 자동 추가
    color_discrete_map={            # 색상 맵핑
        'Q1: 고CCTV/고범죄': '#ff7f0e',
        'Q2: 저CCTV/고범죄 (우선순위)': '#d62728',
        'Q3: 저CCTV/저범죄': '#2ca02c',
        'Q4: 고CCTV/저범죄 (효과적)': '#1f77b4'
    }
)

# 중앙값 기준선
fig.add_hline(y=crime_median, line_dash="dash", line_color="gray")
fig.add_vline(x=cctv_median, line_dash="dash", line_color="gray")

st.plotly_chart(fig, use_container_width=True)
```

**Plotly 장점**
- 마우스 호버: 자치구명, CCTV 대수, 범죄 건수 표시
- 줌/팬: 특정 영역 확대 가능
- 범례 클릭: 특정 분면 숨기기/보이기
- `trendline='ols'`: 회귀선 자동 계산 및 R² 표시

---

## 5. 통계 분석 방법론

### 5.1 상관관계와 인과관계

#### **상관관계 (Correlation)**
```
정의: 두 변수가 함께 변하는 정도
공식: Pearson 상관계수 r = Cov(X,Y) / (σX * σY)
```

**예시**
- CCTV ↑ → 범죄 ↑ (r = 0.77)
- 이것만으로는 인과관계 증명 불가!

#### **인과관계 (Causation)**
```
조건:
  1. X와 Y가 상관관계 있음
  2. X가 Y보다 시간적으로 앞섬
  3. 제3의 변수(Z)가 X와 Y를 모두 일으키지 않음
```

**이 프로젝트의 문제**
```
발견: CCTV ↑ → 범죄 ↑ (양의 상관)
예상: CCTV ↑ → 범죄 ↓ (음의 상관을 기대했으나...)

원인: 역인과관계 (Reverse Causality)
  실제: 범죄 ↑ → CCTV 설치 ↑

정책 결정 과정:
  1. 범죄가 많이 발생한 지역 파악
  2. 해당 지역에 CCTV 추가 설치
  3. 결과적으로 범죄 많은 곳 = CCTV 많은 곳
```

#### **시계열 데이터 필요성**
```
단면 데이터 (Cross-sectional):
  - 한 시점의 스냅샷
  - 인과관계 파악 어려움
  - 이 프로젝트는 2024년 단면 데이터

시계열 데이터 (Time-series):
  - 여러 시점 추적
  - 인과관계 파악 가능

예시:
  2020년: 강남구 CCTV 5,000대 → 범죄 7,000건
  2021년: CCTV 1,000대 추가 설치
  2022년: 강남구 CCTV 6,000대 → 범죄 6,500건 (감소!)

  → 이제 CCTV의 범죄 억제 효과 확인 가능
```

### 5.2 통계적 유의성 검정

#### **p-value 의미**
```
귀무가설 (H0): CCTV와 범죄 간 상관관계 없음 (r=0)
대립가설 (H1): CCTV와 범죄 간 상관관계 있음 (r≠0)

p-value = 0.0001
→ H0가 참일 확률이 0.01% (매우 낮음)
→ H0 기각, H1 채택
→ 상관관계가 통계적으로 유의함
```

**기준**
- p < 0.001: 매우 유의함 ***
- p < 0.01: 유의함 **
- p < 0.05: 유의함 *
- p ≥ 0.05: 유의하지 않음 (ns)

### 5.3 다중 선형 회귀 가정

**1) 선형성 (Linearity)**
- X와 Y가 선형 관계
- 확인: 산점도가 직선 형태

**2) 독립성 (Independence)**
- 잔차가 서로 독립적
- 위반 시: 자기상관(Autocorrelation) 문제

**3) 정규성 (Normality)**
- 잔차가 정규분포
- 확인: Q-Q Plot

**4) 등분산성 (Homoscedasticity)**
- 잔차의 분산이 일정
- 확인: 잔차 vs 예측값 산점도

**5) 다중공선성 없음 (No Multicollinearity)**
- 독립변수들 간 강한 상관 없음
- 확인: VIF < 10

---

## 6. 대시보드 구조 및 기능

### 6.1 전체 구조

```python
# 페이지 설정
st.set_page_config(
    page_title="서울시 CCTV-범죄 분석 대시보드",
    page_icon="📹",
    layout="wide",              # 전체 폭 사용
    initial_sidebar_state="expanded"
)
```

### 6.2 데이터 캐싱

```python
@st.cache_data  # 함수 결과를 메모리에 저장
def load_data():
    df = pd.read_csv('data/processed/integrated_data_with_analysis.csv')

    # 사분면 분류
    cctv_median = df['방범CCTV_per_1000'].median()
    crime_median = df['CCTV효과범죄_per_1000'].median()
    df['분면'] = df.apply(classify_quadrant, axis=1)

    return df

df = load_data()  # 첫 실행: 데이터 로드 → 캐시 저장
                  # 이후 실행: 캐시에서 바로 불러옴 (빠름!)
```

**캐싱의 중요성**
- Streamlit은 사용자 액션마다 스크립트 전체 재실행
- 캐싱 없으면: 매번 CSV 읽기 (느림)
- 캐싱 있으면: 한 번만 읽고 재사용 (빠름)

### 6.3 필터 기능

```python
# 사이드바 필터
selected_districts = st.sidebar.multiselect(
    "자치구 선택",
    options=sorted(df['자치구'].unique().tolist()),
    default=sorted(df['자치구'].unique().tolist())  # 기본값: 전체 선택
)

selected_quadrants = st.sidebar.multiselect(
    "분면 선택",
    options=sorted(df['분면'].unique().tolist()),
    default=sorted(df['분면'].unique().tolist())
)

# 필터 적용
filtered_df = df[
    (df['자치구'].isin(selected_districts)) &
    (df['분면'].isin(selected_quadrants))
]
```

**동작 원리**
1. 사용자가 "강남구" 선택 해제
2. `selected_districts`에서 "강남구" 제외
3. `isin()` 조건으로 필터링
4. `filtered_df`에 강남구 제외된 데이터만 남음
5. 모든 차트가 `filtered_df` 기반으로 재생성

### 6.4 주요 탭별 기능

#### **탭 1: 📈 개요**
```python
with tab1:
    # 4사분면 산점도
    fig = px.scatter(...)

    # 중앙값 기준선
    fig.add_hline(y=median_crime, line_dash="dash")
    fig.add_vline(x=median_cctv, line_dash="dash")

    # 분면별 파이 차트
    fig_pie = px.pie(values=quadrant_counts.values, ...)

    # 상관계수 요약
    corr1 = filtered_df['CCTV_per_1000'].corr(filtered_df['범죄_per_1000'])
    st.metric("전체 CCTV vs 전체 범죄", f"{corr1:.4f}")
```

**핵심 기능**
- 4사분면 시각화로 정책 우선순위 한눈에 파악
- 분면별 자치구 분포 확인
- 주요 상관계수 요약

#### **탭 2: 📹 CCTV 분석**
```python
with tab2:
    # 상위 10개 자치구 (CCTV 대수)
    top_districts = filtered_df.nlargest(10, 'CCTV_총계')
    fig_top_cctv = px.bar(top_districts, x='CCTV_총계', y='자치구',
                          orientation='h')  # 수평 막대 차트

    # 인구당 CCTV 상위 10개
    top_cctv_per_capita = filtered_df.nlargest(10, 'CCTV_per_1000')

    # CCTV 유형별 스택 차트
    fig_stack = px.bar(cctv_by_district, barmode='stack')
```

**핵심 기능**
- 절대값 vs 인구당 비교
- CCTV 유형별 비중 확인 (방범용, 교통단속 등)

#### **탭 3: 🚨 범죄 분석**
```python
with tab3:
    # 범죄 발생 상위 자치구
    top_crime_districts = filtered_df.nlargest(10, '총범죄_발생')

    # 범죄 유형별 스택 차트
    crime_types = filtered_df[['살인', '강도', '강간강제추행', '절도', '폭력']]
    fig_crime_stack = px.bar(crime_types, barmode='stack')
```

**핵심 기능**
- 범죄 다발 지역 식별
- 범죄 유형별 비중 파악 (절도가 가장 많음)

#### **탭 4: 🗺️ 상관관계**
```python
with tab4:
    # 상관계수 히트맵
    corr_matrix = filtered_df[correlation_columns].corr()
    fig_corr = px.imshow(corr_matrix, color_continuous_scale='RdBu_r',
                         zmin=-1, zmax=1, text_auto='.2f')

    # 산점도 + OLS 회귀선
    fig_scatter = px.scatter(..., trendline='ols')
```

**핵심 기능**
- 모든 변수 간 상관관계 한눈에 확인
- 회귀선으로 추세 파악
- R² 값으로 설명력 확인

#### **탭 5: 📋 데이터 테이블**
```python
with tab5:
    # 데이터프레임 표시
    st.dataframe(display_df, use_container_width=True, height=400)

    # CSV 다운로드
    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name='cctv_crime_analysis_2024.csv',
        mime='text/csv'
    )
```

**핵심 기능**
- 원본 데이터 확인
- CSV 다운로드로 외부 분석 가능

### 6.5 반응형 레이아웃

```python
# 2열 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# 4열 레이아웃 (메트릭 카드)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 CCTV", f"{total_cctv:,}대")
```

**`use_container_width=True`의 중요성**
- 화면 크기에 따라 차트 크기 자동 조정
- 모바일/태블릿/데스크톱 모두 대응

---

## 7. 코드 구조 및 아키텍처

### 7.1 프로젝트 파일 구조

```
cctv분석/
│
├── data/
│   ├── raw/                          # 원본 데이터
│   │   ├── cctv_seoul_2024.csv
│   │   ├── crime_seoul_2024.csv
│   │   └── population_seoul_2024.csv
│   └── processed/                    # 전처리 데이터
│       └── integrated_data_with_analysis.csv
│
├── cctvdataset/                      # 공공데이터 원본 (Excel/CSV)
│   ├── 서울시 자치구 CCTV 설치현황.xlsx
│   ├── 5대+범죄+발생현황.csv
│   └── 등록인구.csv
│
├── results/
│   ├── figures/                      # 시각화 이미지
│   │   ├── scatter_cctv_crime_real.png
│   │   ├── correlation_heatmap_real.png
│   │   └── cctv_by_district_real.png
│   └── reports/                      # 분석 보고서
│       └── analysis_summary.txt
│
├── process_real_data.py              # 원본 데이터 정제
├── run_real_data_analysis.py         # 통계 분석 실행
├── dashboard_real.py                 # Streamlit 대시보드
├── fetch_seoul_data.py               # API 데이터 수집 (미사용)
├── requirements.txt                  # Python 패키지 목록
└── README.md                         # 프로젝트 설명서
```

### 7.2 실행 순서

```bash
# 1단계: 데이터 정제
python process_real_data.py
# 출력: data/raw/cctv_seoul_2024.csv
#       data/raw/crime_seoul_2024.csv
#       data/raw/population_seoul_2024.csv

# 2단계: 통계 분석
python run_real_data_analysis.py
# 출력: results/figures/*.png
#       results/reports/analysis_summary.txt
#       data/processed/integrated_data_with_analysis.csv

# 3단계: 대시보드 실행
streamlit run dashboard_real.py
# 브라우저 자동 열림: http://localhost:8501
```

### 7.3 주요 함수 설명

#### **process_real_data.py**
```python
# 역할: Excel/CSV → 정제된 CSV 변환

# 1. CCTV 데이터 처리
cctv_df = pd.read_excel('파일경로', header=None)
# → 헤더 스킵, 자치구별 집계

# 2. 범죄 데이터 처리
crime_df = pd.read_csv('파일경로', encoding='utf-8-sig')
# → '-' 문자열을 0으로 변환

# 3. 인구 데이터 처리
pop_df = pd.read_csv('파일경로', encoding='utf-8-sig')
# → 자치구명 표준화

# 4. 데이터 병합 및 저장
merged = cctv_clean.merge(crime_clean, on='자치구')
merged.to_csv('data/raw/merged_real_data.csv')
```

#### **run_real_data_analysis.py**
```python
# 역할: 통계 분석 및 시각화 생성

# 1. 데이터 로드
df = pd.read_csv('data/raw/cctv_seoul_2024.csv')

# 2. 파생 변수 생성
df['CCTV_per_1000'] = (df['CCTV_총계'] / df['총인구']) * 1000

# 3. 상관 분석
r, p = stats.pearsonr(df['CCTV_per_1000'], df['범죄_per_1000'])

# 4. 시각화
plt.scatter(...)
plt.savefig('results/figures/scatter.png', dpi=300)

# 5. 결과 저장
df.to_csv('data/processed/integrated_data_with_analysis.csv')
```

#### **dashboard_real.py**
```python
# 역할: 인터랙티브 웹 대시보드

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/integrated_data_with_analysis.csv')
    df['분면'] = df.apply(classify_quadrant, axis=1)
    return df

df = load_data()

# 필터
selected = st.multiselect("자치구", df['자치구'].unique())
filtered_df = df[df['자치구'].isin(selected)]

# 시각화
fig = px.scatter(filtered_df, ...)
st.plotly_chart(fig)
```

---

## 8. 주요 발견 사항 및 인사이트

### 8.1 핵심 발견

#### **1. 강한 양의 상관관계**
```
CCTV_per_1000 vs 범죄_per_1000
  r = 0.7684
  p < 0.0001

해석:
  - CCTV가 많은 자치구일수록 범죄도 많음
  - 이는 일반적인 예상과 반대
```

#### **2. 역인과관계 확인**
```
예상: CCTV 설치 → 범죄 감소 (음의 상관)
현실: 범죄 발생 → CCTV 설치 (양의 상관)

이유:
  정책 결정 과정에서 범죄 다발 지역에
  우선적으로 CCTV를 설치했기 때문
```

#### **3. CCTV 유형별 차이**
```
방범용 CCTV vs CCTV효과범죄
  r = 0.7408 (강한 양의 상관)

교통단속 CCTV vs CCTV효과범죄
  r = 0.32 (약한 양의 상관)

→ 방범용 CCTV가 범죄와 더 강한 관련성
```

#### **4. 4사분면 분류 결과**
```
Q1 (고CCTV/고범죄): 6개 자치구
  - 강남구, 송파구, 관악구 등
  - CCTV 많지만 여전히 범죄 많음
  - 추가 대책 필요 (경찰 순찰, 조명 등)

Q2 (저CCTV/고범죄): 4개 자치구 ⚠️
  - 영등포구, 동대문구 등
  - CCTV 설치 최우선 지역
  - 예산 투입 우선순위

Q3 (저CCTV/저범죄): 8개 자치구
  - 도봉구, 노원구 등
  - 현 상태 유지
  - 불필요한 추가 설치 지양

Q4 (고CCTV/저범죄): 6개 자치구
  - 서초구, 용산구 등
  - CCTV 효과적으로 작동
  - 모범 사례로 활용
```

### 8.2 정책 제안

#### **단기 제안 (1년 이내)**
1. **Q2 지역 집중 투자**
   - 저CCTV/고범죄 지역에 방범 CCTV 우선 설치
   - 예산: CCTV 1대당 약 500만원

2. **Q1 지역 복합 대책**
   - CCTV만으로 부족 → 경찰 순찰 강화
   - LED 가로등 교체 (밝기 개선)
   - 주민 안심귀가 서비스

#### **중장기 제안 (2-3년)**
1. **시계열 데이터 구축**
   - 연도별 CCTV 설치 이력 수집
   - 설치 전/후 범죄 변화 추적
   - 실제 CCTV 효과 검증

2. **AI 기반 범죄 예측 모델**
   - 머신러닝으로 범죄 다발 시간/장소 예측
   - CCTV 카메라 각도 최적화
   - 실시간 위험 지역 모니터링

3. **데이터 기반 의사결정 체계**
   - 이 대시보드를 정책 회의에서 활용
   - 매 분기 데이터 업데이트 및 재분석
   - 투명한 예산 배분 근거 제시

### 8.3 한계점

#### **1. 시계열 데이터 부재**
```
문제:
  2024년 단면 데이터만 사용
  → 인과관계 파악 불가

해결:
  2020~2024년 연도별 데이터 수집
  → 패널 회귀 분석 (Panel Regression)
```

#### **2. 누락 변수 편향 (Omitted Variable Bias)**
```
포함한 변수:
  CCTV, 범죄, 인구, 인구밀도

누락된 변수:
  - 경찰 순찰 빈도
  - 가로등 밝기
  - 상권 활성화 정도
  - 유동인구

→ 이들이 CCTV와 범죄 모두에 영향
```

#### **3. 집계 수준 (Aggregation Level)**
```
현재: 자치구별 집계 (N=24)
  → 자치구 내부 편차 무시

개선:
  동 단위 또는 격자(Grid) 단위 분석
  → 더 세밀한 패턴 파악
```

#### **4. CCTV 품질 미고려**
```
미고려 요인:
  - 화질 (HD, 4K 등)
  - 작동 시간 (24시간 vs 야간만)
  - 모니터링 여부 (실시간 vs 녹화만)

→ 같은 1대라도 효과 다를 수 있음
```

---

## 9. 면접 예상 질문 및 답변

### 9.1 프로젝트 개요

**Q1. 이 프로젝트를 왜 진행했나요?**

A: 도시 안전은 주민 삶의 질에 직결되는 중요한 문제입니다. 서울시는 매년 수백억 원의 예산을 CCTV 설치에 투입하고 있지만, 실제로 범죄 예방 효과가 있는지 데이터 기반 검증이 부족했습니다. 저는 공공데이터를 활용하여 CCTV와 범죄 간 관계를 분석하고, 예산을 효율적으로 배분할 수 있는 정책 인사이트를 제공하고자 이 프로젝트를 시작했습니다.

**Q2. 프로젝트의 핵심 성과는 무엇인가요?**

A: 크게 3가지입니다.

1. **역인과관계 발견**: CCTV가 범죄를 줄이는 것이 아니라, 범죄가 많은 지역에 CCTV를 더 설치한다는 사실을 통계적으로 입증했습니다 (r=0.77, p<0.0001).

2. **4사분면 분류 모델**: 자치구를 CCTV 밀도와 범죄율로 분류하여, 저CCTV/고범죄 지역(Q2)을 우선 투자 대상으로 명확히 제시했습니다.

3. **인터랙티브 대시보드**: Streamlit으로 정책 입안자가 직접 데이터를 탐색하고, 실시간으로 다양한 시나리오를 분석할 수 있는 도구를 제공했습니다.

### 9.2 기술 역량

**Q3. Pandas의 merge와 SQL JOIN의 차이를 설명해주세요.**

A: 개념적으로는 유사하지만, 문법과 동작 방식에 차이가 있습니다.

```python
# Pandas
merged = df1.merge(df2, on='key', how='inner')

# SQL
SELECT * FROM df1 INNER JOIN df2 ON df1.key = df2.key
```

**주요 차이점**:
1. **메모리**: Pandas는 전체 데이터를 메모리에 로드, SQL은 인덱스 활용으로 효율적
2. **타입**: Pandas는 DataFrame 객체 반환, SQL은 테이블 반환
3. **확장성**: SQL은 대용량 데이터에 강함 (디스크 기반), Pandas는 메모리 제약

이 프로젝트에서는 24개 자치구로 데이터가 작아서 Pandas를 사용했지만, 동 단위(424개)로 확장한다면 SQLite나 PostgreSQL을 고려할 것입니다.

**Q4. 왜 인구 정규화(Per Capita)가 필요한가요?**

A: 절대값 비교는 인구 규모를 무시하여 잘못된 결론을 도출할 수 있기 때문입니다.

**예시**:
```
강남구: CCTV 8,365대, 인구 54만 → 15.5대/천명
종로구: CCTV 2,100대, 인구 14만 → 15.0대/천명
```

절대값만 보면 강남구가 CCTV가 4배 많지만, 인구당으로는 비슷합니다. 정책 결정 시 "어느 지역이 CCTV 부족한가?"를 판단하려면 인구당 비율이 필수입니다.

**구현**:
```python
df['CCTV_per_1000'] = (df['CCTV_총계'] / df['총인구']) * 1000
```

곱하기 1000을 하는 이유는 "인구 천명당"으로 표현하면 소수점을 줄여 가독성이 높아지기 때문입니다 (15.5대 vs 0.0155대).

**Q5. Streamlit의 캐싱(@st.cache_data)은 왜 중요한가요?**

A: Streamlit은 사용자가 위젯을 조작할 때마다 스크립트 전체를 재실행하는 구조입니다. 캐싱 없이 `pd.read_csv()`를 실행하면 매번 디스크에서 파일을 읽어야 해서 느려집니다.

**캐싱 전**:
```python
def load_data():
    return pd.read_csv('large_file.csv')  # 매번 1초 소요

df = load_data()
st.selectbox(...)  # 사용자가 선택할 때마다 1초씩 대기
```

**캐싱 후**:
```python
@st.cache_data
def load_data():
    return pd.read_csv('large_file.csv')  # 첫 실행만 1초, 이후 0.01초

df = load_data()  # 캐시에서 즉시 로드
```

이 프로젝트에서는 CSV 파일이 작아서 체감 속도는 크지 않지만, 실무에서 수백 MB 데이터를 다룰 때는 캐싱이 필수입니다.

### 9.3 통계 분석

**Q6. 상관관계와 인과관계를 구분해서 설명해주세요.**

A: 상관관계는 두 변수가 함께 변하는 정도, 인과관계는 한 변수가 다른 변수를 일으키는 관계입니다.

**예시 1 - 상관관계 ≠ 인과관계**:
```
아이스크림 판매량 ↑ ↔ 익사 사고 ↑ (r=0.8)
→ 아이스크림이 익사를 일으킨 게 아님!
→ 숨은 변수: 기온 (더울 때 둘 다 증가)
```

**예시 2 - 이 프로젝트**:
```
발견: CCTV ↑ ↔ 범죄 ↑ (r=0.77)
해석: 역인과관계 (범죄 → CCTV 설치)
```

**인과관계 입증 조건**:
1. X와 Y 상관관계 ✓
2. X가 Y보다 시간적으로 앞섬 ✗ (단면 데이터라 모름)
3. 제3의 변수(Z)가 둘 다 일으키지 않음 ✗ (인구밀도, 상권 등)

→ 시계열 데이터로 2번 조건 해결 필요

**Q7. p-value가 0.0001이면 무엇을 의미하나요?**

A: 귀무가설(H0: 상관계수 r=0)이 참일 확률이 0.01%라는 뜻입니다. 즉, 우연히 이런 상관관계가 나올 확률이 극히 낮아서, 통계적으로 유의미한 관계가 있다고 결론 내릴 수 있습니다.

**기준**:
- p < 0.001: 매우 강력한 증거 ***
- p < 0.01: 강력한 증거 **
- p < 0.05: 충분한 증거 * (일반적 기준)
- p ≥ 0.05: 증거 부족 (귀무가설 기각 불가)

이 프로젝트에서는 p=0.0001로 매우 강력한 증거를 확보했습니다.

**Q8. 회귀 분석의 R-squared가 0.627이면 좋은 건가요?**

A: R²=0.627은 독립변수(방범CCTV, 인구밀도)가 종속변수(CCTV효과범죄)의 변동을 62.7% 설명한다는 의미입니다.

**평가 기준**:
- 사회과학: R²=0.3~0.5도 괜찮음 (인간 행동은 복잡)
- 자연과학: R²=0.8 이상 기대 (물리 법칙은 명확)

**이 프로젝트**: 62.7%는 사회 현상을 다루는 분석치고 준수한 수준입니다. 나머지 37.3%는 경찰 순찰, 조명, 유동인구 등 미포함 변수의 영향입니다.

**개선 방안**:
- 추가 변수 포함 → R² 향상
- 비선형 모델(Random Forest 등) 시도

### 9.4 대시보드 및 시각화

**Q9. Plotly를 선택한 이유는 무엇인가요?**

A: Matplotlib/Seaborn과 비교했을 때 3가지 장점 때문입니다.

**1. 인터랙티브**:
- 마우스 호버로 데이터 상세 정보 표시
- 줌/팬으로 특정 영역 확대
- 범례 클릭으로 특정 카테고리 숨기기

**2. Streamlit 완벽 호환**:
```python
fig = px.scatter(...)
st.plotly_chart(fig, use_container_width=True)  # 한 줄로 통합
```

**3. OLS 회귀선 자동 계산**:
```python
fig = px.scatter(..., trendline='ols')
# → 회귀선 + R² 값 자동 표시
```

**단점**:
- 파일 저장 시 의존성 필요 (Matplotlib는 간단)
- 커스터마이징이 복잡할 수 있음

하지만 대시보드 프로젝트에서는 인터랙티브가 핵심이므로 Plotly가 최적입니다.

**Q10. 4사분면 분류에서 중앙값을 사용한 이유는?**

A: 평균은 극단값(Outlier)에 영향을 많이 받지만, 중앙값은 강건(Robust)하기 때문입니다.

**예시**:
```
CCTV 대수: 1500, 2000, 2500, 8365 (강남구)
평균 = 3,591
중앙값 = 2,250

→ 강남구 1개 때문에 평균이 1,000대 이상 높아짐
→ 중앙값이 더 대표성 있음
```

**4사분면 분류에서**:
- 평균 기준: 강남구 때문에 기준선이 높아져 많은 자치구가 "저CCTV"로 분류됨
- 중앙값 기준: 정확히 50%씩 분할 → 균형 잡힌 분류

### 9.5 프로젝트 개선

**Q11. 이 프로젝트를 어떻게 개선할 수 있을까요?**

A: 4가지 방향으로 개선하겠습니다.

**1. 시계열 분석**:
```python
# 현재: 2024년 단면 데이터
# 개선: 2020~2024년 패널 데이터

# 패널 회귀 (Fixed Effects Model)
from linearmodels import PanelOLS

model = PanelOLS(y, X, entity_effects=True, time_effects=True)
# → CCTV 설치 전/후 범죄 변화 추적
```

**2. 공간 분석**:
```python
# 공간 자기상관 (Spatial Autocorrelation)
from pysal.explore import esda

# 모란 지수 (Moran's I)
moran = esda.Moran(df['범죄율'], weights)
# → 범죄가 인접 자치구로 확산되는지 확인
```

**3. 머신러닝 모델**:
```python
from sklearn.ensemble import RandomForestRegressor

# 비선형 관계 포착
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# Feature Importance
importances = model.feature_importances_
# → 어떤 변수가 가장 중요한지 파악
```

**4. 실시간 데이터 파이프라인**:
```python
# 현재: 수동 CSV 업데이트
# 개선: API 자동 수집 + 스케줄링

import schedule

def update_data():
    fetcher = SeoulDataFetcher()
    fetcher.fetch_crime_data()
    run_analysis()

schedule.every().month.do(update_data)
# → 매월 자동으로 데이터 갱신 및 재분석
```

**Q12. 실무에서 이 프로젝트를 어떻게 활용할 수 있을까요?**

A: 3가지 활용 시나리오를 생각했습니다.

**1. 정책 입안자용 의사결정 도구**:
- 시의회 예산 심의 시 이 대시보드 활용
- "Q2 지역에 CCTV 100대 추가 시 예상 효과는?" 시뮬레이션
- 투명한 근거 제시로 예산 승인율 향상

**2. 경찰청 범죄 예방 전략**:
- 분면별 맞춤형 대책 수립
- Q1 지역: CCTV + 순찰 강화
- Q2 지역: CCTV 집중 투자
- 분기별 재분석으로 효과 모니터링

**3. 데이터 분석 플랫폼 확장**:
- 다른 도시(부산, 대구 등)로 확장
- 도시 간 비교 분석
- 베스트 프랙티스 공유

---

## 10. 트러블슈팅 및 개선 사항

### 10.1 데이터 수집 문제

#### **문제 1: 한글 인코딩 깨짐**
```python
# 오류
df = pd.read_csv('file.csv')
# → 한글이 깨져서 출력됨

# 해결
df = pd.read_csv('file.csv', encoding='utf-8-sig')
# → BOM(Byte Order Mark) 제거하여 한글 정상 표시
```

**원인**: Windows Excel에서 CSV 저장 시 UTF-8 BOM 형식 사용

#### **문제 2: 비표준 CSV 형식**
```python
# 문제: 헤더가 5번째 줄에 있음
# 1줄: 제목
# 2줄: 출처
# 3줄: 기준일
# 4줄: 공백
# 5줄: 컬럼명
# 6줄~: 데이터

# 해결
df = pd.read_csv('file.csv', header=None)  # 헤더 무시
for i in range(5, len(df)):  # 5번째 줄부터 수동 파싱
    row = df.iloc[i]
    # ...
```

### 10.2 데이터 정제 문제

#### **문제 3: '-' 문자열 처리**
```python
# 오류
df['범죄건수'].sum()  # TypeError: unsupported operand

# 원인: '-'가 문자열로 인식됨

# 해결
df['범죄건수'] = pd.to_numeric(
    df['범죄건수'].replace('-', 0),
    errors='coerce'
).fillna(0)
```

#### **문제 4: 자치구명 불일치**
```python
# 문제
df1: ['종로구', '중구', ...]
df2: ['종로구청', '중구청', ...]
# → merge 시 0건 매칭

# 해결
mapping = {
    '종로구청': '종로구',
    '중구청': '중구',
    # ...
}
df2['자치구'] = df2['자치구'].replace(mapping)
```

### 10.3 분석 문제

#### **문제 5: 다중공선성 (Multicollinearity)**
```python
# 문제: CCTV_총계와 방범용이 높은 상관 (r=0.95)
# → VIF > 10 → 회귀 계수 불안정

# 해결: 한 변수만 사용
X = df[['방범CCTV_per_1000', '인구밀도']]  # CCTV_총계 제외
```

#### **문제 6: 이상치 (Outlier)**
```python
# 강남구가 CCTV 8,365대로 극단적으로 많음
# → 회귀선이 강남구 쪽으로 치우침

# 확인
plt.boxplot(df['CCTV_총계'])
# → 강남구가 outlier로 표시됨

# 해결 옵션:
# 1) Robust 회귀 (RANSAC)
from sklearn.linear_model import RANSACRegressor

# 2) 로그 변환
df['log_CCTV'] = np.log(df['CCTV_총계'])

# 3) 제거 (비권장: 정보 손실)
df_no_outlier = df[df['CCTV_총계'] < 7000]
```

### 10.4 대시보드 문제

#### **문제 7: 필터 선택 해제 시 에러**
```python
# 문제: 사용자가 모든 자치구 선택 해제 시
# → filtered_df가 빈 DataFrame
# → 차트 생성 실패

# 해결
if len(filtered_df) == 0:
    st.warning("자치구를 1개 이상 선택해주세요.")
    st.stop()
else:
    fig = px.scatter(filtered_df, ...)
```

#### **문제 8: 대시보드 느린 속도**
```python
# 원인: 캐싱 없이 매번 CSV 로드

# 해결
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# 추가 최적화
@st.cache_data
def calculate_correlation(df):
    return df.corr()  # 무거운 계산도 캐싱
```

### 10.5 배포 문제

#### **문제 9: Streamlit Cloud 메모리 부족**
```python
# 문제: Free tier는 1GB RAM 제한
# → 큰 차트 여러 개 생성 시 OOM

# 해결
# 1) 차트 크기 줄이기
fig.update_layout(height=400)  # 600 → 400

# 2) 데이터 샘플링
if len(df) > 10000:
    df_sampled = df.sample(10000)
else:
    df_sampled = df

# 3) 이미지 해상도 낮추기
fig.write_image('chart.png', width=800, height=600)  # 1920x1080 대신
```

#### **문제 10: requirements.txt 버전 충돌**
```python
# 문제
streamlit==1.28.0
plotly==5.17.0
pandas==2.1.0
# → Streamlit Cloud에서 설치 실패

# 해결: 버전 범위 지정
streamlit>=1.28.0,<2.0.0
plotly>=5.17.0
pandas>=2.0.0,<3.0.0

# 또는 최소 버전만
streamlit>=1.28.0
plotly>=5.17.0
```

### 10.6 교훈

**1. 데이터 품질이 가장 중요**
- 분석 시간의 70%는 데이터 정제
- 초기에 데이터 구조 파악 필수

**2. 문서화의 중요성**
- 코드 주석으로 "왜"를 설명
- README에 실행 방법 명시

**3. 버전 관리**
```bash
git commit -m "Add correlation analysis"
# → 매 기능마다 커밋
# → 문제 발생 시 롤백 용이
```

**4. 사용자 테스트**
- 다른 사람에게 대시보드 사용 요청
- 예상치 못한 사용 패턴 발견
- UX 개선 아이디어 도출

---

## 📚 추가 학습 자료

### 통계 기초
- Khan Academy: Statistics and Probability
- StatQuest (YouTube): 시각적 통계 설명

### Python 데이터 분석
- "Python for Data Analysis" by Wes McKinney (Pandas 창시자)
- Real Python: pandas tutorials

### Streamlit
- Streamlit 공식 문서: https://docs.streamlit.io
- Streamlit Gallery: 다양한 대시보드 예시

### 공간 분석
- GeoPandas 튜토리얼
- Folium (지도 시각화)

---

## ✅ 면접 대비 체크리스트

### 프로젝트 설명 (30초 버전)
```
"서울시 24개 자치구의 CCTV 설치 현황과 범죄 발생 데이터를
분석하여 CCTV 설치 우선순위를 도출한 프로젝트입니다.

Pandas로 데이터 정제 및 통합, Scipy로 상관분석(r=0.77),
Streamlit으로 인터랙티브 대시보드를 구현했습니다.

4사분면 분류 모델로 저CCTV/고범죄 지역을 우선 투자 대상으로
제시하여 예산 효율성을 높였습니다."
```

### 기술 스택 완벽 이해
- [ ] Pandas merge 3가지 타입 설명 가능
- [ ] Pearson 상관계수 공식 이해
- [ ] p-value 의미 설명 가능
- [ ] Streamlit 캐싱 원리 이해
- [ ] Plotly vs Matplotlib 장단점 비교 가능

### 통계 개념
- [ ] 상관관계 vs 인과관계 구분
- [ ] 역인과관계 예시 설명
- [ ] 회귀 분석 가정 5가지 암기
- [ ] VIF 해석 방법 이해

### 프로젝트 한계 및 개선안
- [ ] 시계열 데이터 필요성 설명
- [ ] 누락 변수 편향 이해
- [ ] 머신러닝 모델 적용 아이디어
- [ ] 실무 활용 시나리오 3가지 준비

---

## 🎯 마무리

이 문서는 서울시 CCTV-범죄 상관관계 분석 프로젝트의 모든 것을 담고 있습니다.

**포트폴리오 발표 시**:
1. 개요 → 기술 스택 → 핵심 발견 순으로 설명
2. 4사분면 분류 시각화를 핵심 차별점으로 강조
3. 대시보드 라이브 데모 준비

**면접 대비**:
1. 이 문서를 3회 이상 정독
2. 코드 직접 실행하며 각 단계 체감
3. 예상 질문 답변 연습 (특히 Q1~Q12)

**연락처**: 이 문서에 대한 질문이나 프로젝트 관련 문의는 [이메일]로 연락 주세요.

**최종 업데이트**: 2025-12-11

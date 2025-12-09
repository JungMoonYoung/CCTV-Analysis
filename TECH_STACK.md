# 프로젝트 기술 스택 상세 설명

## 📚 목차
1. [프로그래밍 언어](#1-프로그래밍-언어)
2. [데이터 처리 라이브러리](#2-데이터-처리-라이브러리)
3. [통계 분석 라이브러리](#3-통계-분석-라이브러리)
4. [데이터 시각화](#4-데이터-시각화)
5. [API 연동](#5-api-연동)
6. [개발 환경 및 도구](#6-개발-환경-및-도구)
7. [분석 방법론](#7-분석-방법론)
8. [프로젝트 아키텍처](#8-프로젝트-아키텍처)

---

## 1. 프로그래밍 언어

### Python 3.8+
**역할**: 프로젝트 전체의 기반 언어

**선택 이유**:
- 데이터 분석 생태계가 가장 풍부함 (pandas, numpy, scipy)
- 통계 분석 및 머신러닝 라이브러리 지원 우수
- 가독성이 높아 유지보수 용이
- 과학 계산 및 연구 분야 표준 언어

**사용 예시**:
```python
# 리스트 컴프리헨션
cctv_types = ['방범용', '교통단속용', '어린이안전용', '기타']

# 함수형 프로그래밍
df['자치구'] = df['자치구'].apply(standardize_district_name)

# 클래스 기반 설계
class SeoulDataFetcher:
    def __init__(self):
        self.crime_key = os.getenv('SEOUL_CRIME_API_KEY')
```

---

## 2. 데이터 처리 라이브러리

### 2.1 Pandas (>=2.0.0)
**역할**: 데이터프레임 기반 데이터 조작 및 분석

**핵심 기능**:
- **DataFrame**: 2차원 테이블 구조로 CSV, Excel 등 다양한 형식 지원
- **데이터 정제**: 결측치 처리, 중복 제거, 타입 변환
- **데이터 변환**: 피벗, 그룹핑, 병합(merge/join)
- **통계 계산**: describe(), corr(), groupby() 등

**프로젝트 사용 사례**:
```python
# CSV 읽기 (한글 인코딩 처리)
df_cctv = pd.read_csv('cctv_seoul_2023.csv', encoding='utf-8-sig')

# 데이터 병합 (SQL의 JOIN과 유사)
merged = df_cctv.merge(df_crime, on='자치구', how='inner')

# 파생 변수 생성
merged['인구당_총CCTV'] = (merged['총_CCTV'] / merged['인구수'] * 1000).round(2)

# 카테고리 변수 생성 (4분위수 기반)
merged['CCTV밀도_등급'] = pd.qcut(merged['인구당_총CCTV'], q=4, labels=['하', '중하', '중상', '상'])

# 기술 통계량 계산
summary = df[numeric_cols].describe()
```

**장점**:
- SQL과 유사한 직관적인 문법
- 대용량 데이터 처리 최적화
- 시계열 데이터 처리 강력함


### 2.2 NumPy (>=1.24.0)
**역할**: 수치 계산 및 배열 연산

**핵심 기능**:
- **다차원 배열(ndarray)**: 빠른 벡터 연산
- **브로드캐스팅**: 다른 크기의 배열 간 연산 자동화
- **난수 생성**: 재현 가능한 샘플 데이터 생성
- **수학 함수**: sin, cos, log, exp 등

**프로젝트 사용 사례**:
```python
# 재현 가능한 난수 생성 (샘플 데이터)
np.random.seed(42)
populations = np.random.randint(500, 3000, 25)

# 배열 연산
populations = np.maximum(populations, min_population)  # 최소값 보장

# 통계 함수
mean = np.mean(data)
std = np.std(data)
```

**Pandas와의 관계**:
- Pandas의 내부 구현은 NumPy 배열 기반
- Pandas는 NumPy를 감싸 더 편리한 인터페이스 제공

---

## 3. 통계 분석 라이브러리

### 3.1 SciPy (>=1.11.0)
**역할**: 과학 계산 및 통계 검정

**핵심 기능**:
- **통계 분포**: 정규분포, t분포, F분포 등
- **가설 검정**: t-test, chi-square test, ANOVA
- **상관 분석**: Pearson, Spearman 상관계수
- **최적화**: 최소값/최대값 찾기

**프로젝트 사용 사례**:
```python
from scipy import stats

# Pearson 상관계수 계산
corr, p_value = stats.pearsonr(df['인구당_방범용'], df['인구당_CCTV효과범죄율'])

# Spearman 상관계수 (순위 기반, 비선형 관계 탐지)
rho, p_value = stats.spearmanr(df['CCTV밀도'], df['범죄율'])

# 정규성 검정 (Shapiro-Wilk test)
stat, p_value = stats.shapiro(residuals)
```

**통계적 의미**:
- **p-value < 0.05**: 통계적으로 유의미함
- **상관계수 r**: -1 ~ 1 범위 (0에 가까우면 무상관)


### 3.2 Statsmodels (>=0.14.0)
**역할**: 회귀분석 및 고급 통계 모델링

**핵심 기능**:
- **선형 회귀(OLS)**: 최소자승법 기반 회귀분석
- **회귀 진단**: VIF, 잔차 분석, Q-Q plot
- **시계열 분석**: ARIMA, 계절성 분해
- **통계 검정**: F-test, Durbin-Watson

**프로젝트 사용 사례**:
```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 다중 선형 회귀
X = merged[['인구당_방범용', '인구밀도']]
y = merged['인구당_CCTV효과범죄율']
X_with_const = sm.add_constant(X)  # 절편 추가
model = sm.OLS(y, X_with_const).fit()

# 회귀 결과 출력
print(model.summary())  # R², Adj R², F-statistic, p-value, 계수 등

# VIF (다중공선성 진단)
vif = pd.DataFrame()
vif['Variable'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
# VIF > 10이면 다중공선성 의심
```

**회귀 결과 해석**:
- **R² (결정계수)**: 모델이 설명하는 분산 비율 (0~1)
- **Adj R²**: 변수 개수를 고려한 수정된 R²
- **F-statistic**: 모델 전체의 유의성
- **계수(coef)**: 독립변수 1단위 증가 시 종속변수 변화량
- **p-value**: 계수의 통계적 유의성 (< 0.05면 유의)

---

## 4. 데이터 시각화

### 4.1 Matplotlib (>=3.7.0)
**역할**: 기본 시각화 라이브러리 (MATLAB 스타일)

**핵심 기능**:
- **다양한 차트**: 선 그래프, 막대 그래프, 산점도, 히스토그램
- **세밀한 커스터마이징**: 색상, 폰트, 축, 레전드 등
- **subplot**: 여러 그래프를 한 화면에 배치
- **저장**: PNG, PDF, SVG 등 다양한 형식

**프로젝트 사용 사례**:
```python
import matplotlib.pyplot as plt

# 기본 설정
matplotlib.use('Agg')  # Non-interactive backend (서버 환경용)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 히스토그램
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['총_CCTV'], bins=15, edgecolor='black', alpha=0.7)
ax.set_title('CCTV 분포', fontsize=14, fontweight='bold')
ax.axvline(mean_val, color='red', linestyle='--', label=f'평균: {mean_val:.1f}')
ax.legend()
plt.savefig('cctv_distribution.png', dpi=300, bbox_inches='tight')

# Subplot (여러 그래프)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
axes[0].bar(categories, means)
axes[1].pie(means, labels=categories, autopct='%1.1f%%')
plt.tight_layout()
```

**장점**:
- Python 시각화의 사실상 표준
- 세밀한 제어 가능
- 다른 라이브러리의 기반 (seaborn, pandas plot 등)


### 4.2 Seaborn (>=0.12.0)
**역할**: 통계적 시각화 (Matplotlib 기반 고수준 인터페이스)

**핵심 기능**:
- **통계 차트**: 박스플롯, 바이올린 플롯, 히트맵
- **회귀 플롯**: regplot, lmplot (회귀선 자동 추가)
- **분포 플롯**: distplot, kdeplot (커널 밀도 추정)
- **색상 팔레트**: 미적으로 우수한 기본 테마

**프로젝트 사용 사례**:
```python
import seaborn as sns

# 상관관계 히트맵
corr_matrix = merged[['인구당_총CCTV', '인구당_방범용', '인구당_CCTV효과범죄율', '인구밀도']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.3f')
plt.title('변수 간 상관관계')

# 회귀 플롯 (산점도 + 회귀선)
sns.regplot(x='인구당_방범용', y='인구당_CCTV효과범죄율', data=merged)

# 박스플롯 (이상치 탐지)
sns.boxplot(data=merged, y='총_범죄')

# 색상 팔레트 설정
sns.set_palette("husl")
```

**Matplotlib과의 차이**:
- Seaborn: 빠르고 예쁜 통계 차트 (고수준)
- Matplotlib: 세밀한 커스터마이징 (저수준)
- 둘을 함께 사용하는 것이 일반적

---

## 5. API 연동

### 5.1 Requests (>=2.31.0)
**역할**: HTTP 요청을 통한 API 호출

**핵심 기능**:
- **GET/POST 요청**: RESTful API 호출
- **세션 관리**: 인증, 쿠키 유지
- **타임아웃 설정**: 무한 대기 방지
- **JSON 파싱**: API 응답 자동 변환

**프로젝트 사용 사례**:
```python
import requests

# 서울 열린데이터광장 API 호출
url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/{service_name}/1/1000"
response = requests.get(url, timeout=30)

# 상태 코드 확인
response.raise_for_status()  # 200이 아니면 예외 발생

# JSON 파싱
data = response.json()
rows = data['결과키']['row']
df = pd.DataFrame(rows)
```

**주요 에러 처리**:
```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("API 응답 시간 초과")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 오류: {e}")
except requests.exceptions.RequestException as e:
    print(f"요청 실패: {e}")
```


### 5.2 Python-dotenv (>=1.0.0)
**역할**: 환경 변수 관리 (.env 파일)

**핵심 기능**:
- **API 키 보호**: Git에 노출되지 않도록 분리
- **.env 파일 자동 로드**: os.getenv()로 접근
- **환경별 설정**: 개발/운영 환경 분리

**프로젝트 사용 사례**:
```python
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수 읽기
api_key = os.getenv('SEOUL_CRIME_API_KEY')
```

**.env 파일 예시**:
```env
SEOUL_CRIME_API_KEY=abc123xyz
SEOUL_POPULATION_API_KEY=def456uvw
```

**보안 중요성**:
- .env 파일은 절대 Git에 커밋하지 않음 (.gitignore에 추가)
- .env.example은 키 없이 템플릿만 제공

---

## 6. 개발 환경 및 도구

### 6.1 Git
**역할**: 버전 관리 시스템

**프로젝트 사용**:
```bash
# .gitignore 설정
.env              # API 키 보호
__pycache__/      # Python 캐시
*.pyc
data/raw/*.csv    # 대용량 원본 데이터
logs/*.log
```


### 6.2 Python 표준 라이브러리

#### os 모듈
- **파일/디렉토리 관리**: `os.makedirs()`, `os.path.join()`
- **환경 변수**: `os.getenv()`

#### platform 모듈
- **OS 감지**: Windows/macOS/Linux별 한글 폰트 설정
```python
system = platform.system()
if system == 'Windows':
    font_name = 'Malgun Gothic'
elif system == 'Darwin':  # macOS
    font_name = 'AppleGothic'
else:  # Linux
    font_name = 'NanumGothic'
```

---

## 7. 분석 방법론

### 7.1 상관 분석
**개념**: 두 변수 간 선형 관계의 강도와 방향 측정

**사용 기법**:
- **Pearson 상관계수**: 선형 관계 (정규분포 가정)
- **Spearman 상관계수**: 순위 기반 (비선형 관계 탐지)

**해석**:
- r = 1: 완전한 양의 상관
- r = 0: 무상관
- r = -1: 완전한 음의 상관
- |r| > 0.7: 강한 상관
- 0.3 < |r| < 0.7: 중간 상관
- |r| < 0.3: 약한 상관


### 7.2 다중 선형 회귀 분석
**개념**: 여러 독립변수로 종속변수 예측

**모형**:
```
y = β₀ + β₁X₁ + β₂X₂ + ε

y: 인구당_CCTV효과범죄율
X₁: 인구당_방범용
X₂: 인구밀도
β: 회귀계수
ε: 오차항
```

**회귀 가정 검토**:
1. **다중공선성 (VIF)**:
   - VIF < 10: 문제 없음
   - VIF > 10: 독립변수 간 상관 높음 (제거 필요)

2. **잔차 정규성 (Shapiro-Wilk test)**:
   - p-value > 0.05: 정규분포 가정 만족

3. **등분산성 (Residual plot)**:
   - 잔차가 무작위로 분포해야 함

4. **독립성 (Durbin-Watson)**:
   - 1.5 ~ 2.5: 독립성 만족


### 7.3 IQR 기반 이상치 탐지
**개념**: 사분위수 범위를 이용한 극단값 탐지

**공식**:
```
IQR = Q3 - Q1
하한 = Q1 - 1.5 × IQR
상한 = Q3 + 1.5 × IQR
```

**구현**:
```python
def detect_outliers_iqr(df, column, threshold=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound
```


### 7.4 4사분면 분류 (Quadrant Analysis)
**개념**: 두 기준(CCTV 밀도, 범죄율)으로 지역 분류

**분류 기준**:
- 중앙값(median) 기준으로 고/저 구분
- 4개 그룹 생성

**정책 우선순위**:
```
Q2 (저CCTV/고범죄) → 최우선 설치
Q1 (고CCTV/고범죄) → 종합 대책 필요
Q4 (고CCTV/저범죄) → 효과적 사례
Q3 (저CCTV/저범죄) → 현상 유지
```

**구현**:
```python
cctv_median = merged['인구당_방범용'].median()
crime_median = merged['인구당_CCTV효과범죄율'].median()

def classify_quadrant(row):
    cctv = row['인구당_방범용']
    crime = row['인구당_CCTV효과범죄율']
    if cctv >= cctv_median and crime >= crime_median:
        return 'Q1: 고CCTV/고범죄'
    elif cctv < cctv_median and crime >= crime_median:
        return 'Q2: 저CCTV/고범죄 (우선순위)'
    # ...
```

---

## 8. 프로젝트 아키텍처

### 8.1 모듈화 구조
```
cctv분석/
├── utils/                    # 공통 유틸리티
│   ├── __init__.py          # 패키지 초기화 (from utils import *)
│   ├── constants.py         # 상수 정의 (자치구 리스트, 범위 설정)
│   └── helpers.py           # 재사용 함수 (한글 폰트, 시각화, 통계)
├── run_all_analysis.py      # 메인 실행 스크립트
├── fetch_seoul_data.py      # API 데이터 수집
└── generate_complete_report.py  # 보고서 생성
```

**모듈화 장점**:
- **재사용성**: 한 번 작성한 함수를 여러 곳에서 사용
- **유지보수**: 기능별 파일 분리로 코드 관리 용이
- **테스트**: 개별 함수 단위 테스트 가능


### 8.2 설계 원칙

#### DRY (Don't Repeat Yourself)
```python
# Bad: 중복 코드
df1['ratio'] = (df1['value'] / df1['total'] * 100).round(2)
df2['ratio'] = (df2['value'] / df2['total'] * 100).round(2)

# Good: 함수로 추상화
def calculate_ratio_columns(df, numerator_cols, denominator_col):
    for col in numerator_cols:
        df[f'{col}_비율'] = (df[col] / df[denominator_col] * 100).round(2)
    return df
```

#### 단일 책임 원칙
- `constants.py`: 상수만 관리
- `helpers.py`: 데이터 처리 함수만 관리
- `fetch_seoul_data.py`: API 호출만 담당


### 8.3 데이터 파이프라인
```
1. 데이터 수집 (fetch_seoul_data.py)
   ↓
2. 데이터 정제 (standardize_district_name, calculate_ratio_columns)
   ↓
3. 데이터 통합 (merge)
   ↓
4. 파생 변수 생성 (인구당_CCTV, 인구당_범죄율)
   ↓
5. 통계 분석 (상관분석, 회귀분석)
   ↓
6. 시각화 (히스토그램, 산점도, 히트맵)
   ↓
7. 지역 분류 (4사분면)
   ↓
8. 보고서 생성 (FINAL_REPORT.md)
```

---

## 9. 성능 최적화

### 9.1 벡터화 연산 (Pandas/NumPy)
```python
# Bad: 반복문 (느림)
for i in range(len(df)):
    df.loc[i, 'ratio'] = df.loc[i, 'value'] / df.loc[i, 'total']

# Good: 벡터화 (빠름)
df['ratio'] = df['value'] / df['total']
```

**성능 차이**: 벡터화가 최대 100배 빠름


### 9.2 메모리 최적화
```python
# 인코딩 명시로 메모리 절약
df = pd.read_csv('data.csv', encoding='utf-8-sig')

# 필요한 컬럼만 읽기
df = pd.read_csv('data.csv', usecols=['자치구', '총_CCTV', '총_범죄'])

# 데이터 타입 최적화
df['인구수'] = df['인구수'].astype('int32')  # int64 대신 int32
```


### 9.3 시각화 백엔드
```python
# Non-interactive backend (서버 환경, 빠름)
matplotlib.use('Agg')

# Interactive backend (로컬 개발)
# %matplotlib inline  (Jupyter)
```

---

## 10. 프로젝트의 기술적 강점

### 10.1 재현 가능성 (Reproducibility)
```python
# 난수 시드 고정
np.random.seed(42)
RANDOM_SEED = 42

# 결과: 누가 실행해도 동일한 결과
```


### 10.2 OS 독립성
```python
# OS별 한글 폰트 자동 설정
system = platform.system()
font_name = {
    'Windows': 'Malgun Gothic',
    'Darwin': 'AppleGothic',
    'Linux': 'NanumGothic'
}[system]
```


### 10.3 보안 및 모범 사례
- API 키를 `.env`로 분리 (환경 변수 관리)
- `.gitignore`로 민감 정보 보호
- `try-except`로 견고한 에러 처리
- 타임아웃 설정으로 무한 대기 방지


### 10.4 확장 가능성
```python
# 새로운 데이터셋 추가 시
def fetch_new_data(self, year=2023):
    # 동일한 구조 유지
    service_name = "새데이터셋"
    data = self.fetch_data(self.new_key, service_name, 1, 1000)
    # ...
```

---

## 11. 학습 곡선 및 난이도

| 기술 | 난이도 | 학습 시간 | 중요도 |
|------|--------|-----------|--------|
| Python 기초 | ⭐⭐ | 1-2주 | ⭐⭐⭐⭐⭐ |
| Pandas | ⭐⭐⭐ | 2-4주 | ⭐⭐⭐⭐⭐ |
| NumPy | ⭐⭐ | 1주 | ⭐⭐⭐⭐ |
| Matplotlib | ⭐⭐⭐ | 2주 | ⭐⭐⭐⭐ |
| Seaborn | ⭐⭐ | 1주 | ⭐⭐⭐ |
| Statsmodels | ⭐⭐⭐⭐ | 3-6주 | ⭐⭐⭐⭐ |
| Requests | ⭐ | 2-3일 | ⭐⭐⭐ |
| Git | ⭐⭐ | 1주 | ⭐⭐⭐⭐⭐ |

---

## 12. 대안 기술 비교

| 목적 | 현재 사용 | 대안 | 선택 이유 |
|------|-----------|------|-----------|
| 데이터 처리 | Pandas | R (dplyr), SQL | Python 생태계 통합성 |
| 통계 분석 | Statsmodels | R (lm), SPSS | 오픈소스, 재현 가능성 |
| 시각화 | Matplotlib/Seaborn | ggplot2, Plotly | 정적 차트, 학술 표준 |
| API 호출 | Requests | urllib3, httpx | 간결한 문법 |
| 환경 변수 | python-dotenv | os.environ | 개발 편의성 |

---

## 13. 참고 자료

### 공식 문서
- Pandas: https://pandas.pydata.org/docs/
- Statsmodels: https://www.statsmodels.org/
- Matplotlib: https://matplotlib.org/
- Seaborn: https://seaborn.pydata.org/

### 추천 학습 자료
- **Python 기초**: "Python for Data Analysis" (Wes McKinney)
- **통계 분석**: "An Introduction to Statistical Learning" (ISLR)
- **데이터 시각화**: "Storytelling with Data" (Cole Nussbaumer Knaflic)

---

**문서 버전**: 1.0
**최종 업데이트**: 2025-12-08

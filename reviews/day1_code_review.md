# Day 1 코드 리뷰 및 개선 사항

**리뷰 날짜**: 2025-07-04
**리뷰 대상**: notebooks/01_initial_exploration.ipynb
**리뷰어**: Claude Code

---

## 📊 전체 평가

| 항목 | 점수 | 코멘트 |
|------|------|--------|
| **코드 품질** | 7/10 | 기본적인 구조는 양호하나 개선 필요 |
| **재현성** | 8/10 | 시드 고정으로 재현 가능 |
| **문서화** | 9/10 | Markdown 설명 충분 |
| **효율성** | 6/10 | 일부 중복 코드 존재 |
| **확장성** | 5/10 | 하드코딩된 값 많음 |

**총점**: 7.0/10

---

## ✅ 잘된 점 (Strengths)

### 1. 명확한 구조
- Markdown 셀로 각 섹션을 명확히 구분
- 데이터 탐색 → 기초 통계 → 시각화 → 요약 순서가 논리적

### 2. 재현 가능성
```python
np.random.seed(42)  # 시드 고정으로 재현 가능
```
- 샘플 데이터 생성 시 시드 고정으로 재현성 확보

### 3. 데이터 저장
```python
cctv_df.to_csv('../data/raw/cctv_seoul_2023_sample.csv', ...)
```
- 생성한 샘플 데이터를 파일로 저장하여 다음 단계에서 재사용 가능

### 4. 시각화 저장
```python
plt.savefig('../results/figures/day1_cctv_distribution.png', dpi=300, bbox_inches='tight')
```
- 고해상도(300 DPI)로 저장
- `bbox_inches='tight'`으로 여백 최소화

---

## ❌ 문제점 및 개선 필요 사항 (Issues)

### 🔴 Critical (심각 - 즉시 수정 필요)

#### 1. 하드코딩된 자치구 리스트
**문제**:
```python
districts = ['종로구', '중구', '용산구', ...]  # 25개 자치구 하드코딩
```

**영향**:
- 다른 노트북에서도 반복 사용 시 일관성 문제
- 자치구 추가/제거 시 모든 곳 수정 필요

**개선안**:
```python
# 별도 config 파일 또는 상수 파일로 분리
SEOUL_DISTRICTS = [
    '종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구',
    '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구',
    '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구',
    '서초구', '강남구', '송파구', '강동구'
]
# 또는 별도 파일: utils/constants.py
```

#### 2. 매직 넘버 (Magic Numbers)
**문제**:
```python
'방범용': np.random.randint(500, 3000, size=25)
'교통단속용': np.random.randint(100, 500, size=25)
```

**영향**:
- 숫자의 의미 불명확
- 샘플 데이터 범위 조정 시 어려움

**개선안**:
```python
# 상수로 정의
CCTV_RANGE = {
    '방범용': (500, 3000),
    '교통단속용': (100, 500),
    '어린이안전용': (50, 300),
    '기타': (50, 200)
}

'방범용': np.random.randint(*CCTV_RANGE['방범용'], size=len(districts))
```

#### 3. 한글 폰트 설정 문제
**문제**:
```python
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows 전용
```

**영향**:
- macOS/Linux에서 실행 시 오류 발생
- 재현성 저해

**개선안**:
```python
import platform

def set_korean_font():
    system = platform.system()
    if system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # Linux
        plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()
```

---

### 🟡 Warning (경고 - 개선 권장)

#### 4. 중복 코드 (DRY 원칙 위반)
**문제**:
```python
# CCTV, 범죄, 인구 데이터 탐색 코드가 거의 동일한 구조 반복
print(f"행 개수: {len(cctv_df)}")
print(f"열 개수: {len(cctv_df.columns)}")
...
```

**개선안**:
```python
def print_data_info(df, data_name):
    """데이터프레임 기본 정보 출력"""
    print(f"[{data_name} 데이터 기본 정보]")
    print(f"행 개수: {len(df)}")
    print(f"열 개수: {len(df.columns)}")
    print(f"\n데이터 타입:\n{df.dtypes}")
    print(f"\n결측치:\n{df.isnull().sum()}")
    print(f"\n처음 5개 행:")
    return df.head()

print_data_info(cctv_df, "CCTV")
print_data_info(crime_df, "범죄")
print_data_info(population_df, "인구")
```

#### 5. 시각화 함수 재사용성 부족
**문제**:
- 히스토그램 코드가 CCTV, 범죄, 인구마다 거의 동일

**개선안**:
```python
def plot_distribution(df, column, title, color='blue', save_path=None):
    """분포 히스토그램 생성"""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(df[column], bins=15, edgecolor='black', alpha=0.7, color=color)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(column)
    ax.set_ylabel('자치구 수')
    mean_val = df[column].mean()
    ax.axvline(mean_val, color='red', linestyle='--', label=f'평균: {mean_val:.0f}')
    ax.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

    return mean_val, df[column].median(), df[column].std()

# 사용
plot_distribution(cctv_df, '총_CCTV', '총 CCTV 대수 분포',
                  color='blue', save_path='../results/figures/day1_cctv_total.png')
```

#### 6. 인구 데이터 생성 로직 개선 필요
**문제**:
```python
'인구수': [150000 + np.random.randint(-30000, 50000) for _ in range(25)]
```
- 리스트 컴프리헨션 내에서 랜덤 생성 → 가독성 저하
- 음수 가능성 있음

**개선안**:
```python
base_population = 150000
population_variation = np.random.randint(-30000, 50000, size=len(districts))
population_data = {
    '자치구': districts,
    '인구수': np.maximum(base_population + population_variation, 50000),  # 최소값 보장
    '면적_km2': np.random.uniform(10, 40, size=len(districts))
}
```

---

### 🟢 Minor (사소 - 개선 시 더 좋음)

#### 7. 주석 부족
**문제**:
```python
cctv_df['총_CCTV'] = cctv_df[['방범용', '교통단속용', '어린이안전용', '기타']].sum(axis=1)
```
- `axis=1`의 의미가 명확하지 않음 (행 단위 합계)

**개선안**:
```python
# 각 자치구별 전체 CCTV 대수 계산 (행 단위 합계)
cctv_df['총_CCTV'] = cctv_df[['방범용', '교통단속용', '어린이안전용', '기타']].sum(axis=1)
```

#### 8. 에러 핸들링 부재
**문제**:
- 파일 저장 시 디렉토리 없을 경우 오류 발생 가능

**개선안**:
```python
import os

def save_csv_safely(df, file_path, **kwargs):
    """디렉토리 생성 후 CSV 저장"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, **kwargs)
    print(f"✅ 파일 저장 완료: {file_path}")

save_csv_safely(cctv_df, '../data/raw/cctv_seoul_2023_sample.csv',
                index=False, encoding='utf-8-sig')
```

#### 9. 시각화 스타일 일관성
**문제**:
- 각 그래프마다 색상이 다름 (의도가 있다면 괜찮음)
- 폰트 크기가 일부 불일치

**개선안**:
```python
# 프로젝트 전체 시각화 스타일 설정
PLOT_STYLE = {
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16
}
plt.rcParams.update(PLOT_STYLE)
```

---

## 🔧 수정 우선순위

### Priority 1 (즉시 수정)
1. ✅ 자치구 리스트를 상수 파일로 분리 (`utils/constants.py`)
2. ✅ 한글 폰트 설정을 OS별 분기 처리
3. ✅ 매직 넘버를 상수로 정의

### Priority 2 (Day 2 전 수정)
4. ✅ 중복 코드를 함수로 리팩토링
5. ✅ 시각화 함수 재사용성 개선
6. ✅ 에러 핸들링 추가

### Priority 3 (여유 있을 때)
7. ⚠️ 주석 추가
8. ⚠️ 시각화 스타일 통일

---

## 📝 코드 개선 체크리스트

- [ ] `utils/constants.py` 파일 생성 (자치구 리스트, CCTV/범죄 범위 등)
- [ ] `utils/helpers.py` 파일 생성 (공통 함수)
  - [ ] `set_korean_font()`: 한글 폰트 설정
  - [ ] `print_data_info()`: 데이터 정보 출력
  - [ ] `save_csv_safely()`: 안전한 CSV 저장
  - [ ] `plot_distribution()`: 분포 히스토그램
- [ ] 노트북 코드 리팩토링
  - [ ] 매직 넘버 제거
  - [ ] 중복 코드 함수화
  - [ ] 주석 추가
- [ ] 테스트 실행 (재현성 확인)

---

## 📌 추가 제안 사항

### 1. 데이터 검증 함수 추가
```python
def validate_data(df, expected_rows=25, required_columns=None):
    """데이터 검증 (행 개수, 필수 컬럼, 결측치)"""
    assert len(df) == expected_rows, f"행 개수 불일치: {len(df)} != {expected_rows}"

    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        assert not missing_cols, f"필수 컬럼 누락: {missing_cols}"

    null_count = df.isnull().sum().sum()
    assert null_count == 0, f"결측치 발견: {null_count}개"

    print("✅ 데이터 검증 완료")

# 사용
validate_data(cctv_df, expected_rows=25,
              required_columns=['자치구', '방범용', '총_CCTV'])
```

### 2. 요약 통계 함수
```python
def create_summary_stats(df, numeric_cols):
    """요약 통계 테이블 생성"""
    summary = df[numeric_cols].describe().T
    summary['중앙값'] = df[numeric_cols].median()
    summary['변동계수'] = (summary['std'] / summary['mean'] * 100).round(2)
    return summary[['mean', '중앙값', 'std', 'min', 'max', '변동계수']]
```

### 3. 로깅 추가
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/day1.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Day 1 데이터 탐색 시작")
```

---

## 🎯 다음 단계 (Day 2 준비)

Day 2에서는 다음 사항을 반영하여 진행:
1. `utils/` 폴더 생성 및 공통 함수 분리
2. Day 1 노트북 리팩토링 적용
3. Day 2 노트북 작성 시 공통 함수 활용

---

## 📊 최종 평가

**개선 후 예상 점수**: 9.0/10

**주요 개선 포인트**:
- ✅ 코드 재사용성 향상 (함수화)
- ✅ 유지보수성 향상 (상수 분리)
- ✅ 재현성 향상 (OS별 분기)
- ✅ 에러 핸들링 추가

**권장 사항**:
- Day 2 작업 전에 Priority 1, 2 항목 모두 수정
- `utils/` 폴더 구조를 먼저 만들고 Day 1 노트북 다시 실행하여 검증

---

**리뷰 완료일**: 2025-07-04
**다음 리뷰**: Day 2 완료 후 (2025-07-05)

# Day 3 코드 리뷰 및 개선 사항

**리뷰 날짜**: 2025-07-06
**리뷰 대상**: notebooks/03_data_integration.ipynb
**리뷰어**: Claude Code

---

## 📊 전체 평가

| 항목 | 점수 | 코멘트 |
|------|------|--------|
| **코드 품질** | 9/10 | utils 함수 활용 우수 |
| **재현성** | 10/10 | 완벽한 재현성 |
| **문서화** | 9/10 | 명확한 섹션 구분 |
| **효율성** | 9/10 | 불필요한 중복 없음 |
| **확장성** | 9.5/10 | 파생변수 생성 체계적 |

**총점**: 9.3/10

---

## ✅ 잘된 점 (Strengths)

### 1. 체계적인 데이터 병합
```python
# Step 1: CCTV + 범죄
merged_df = pd.merge(cctv_df, crime_df, on='자치구', how='inner')
# Step 2: + 인구
merged_df = pd.merge(merged_df, population_df, on='자치구', how='inner')
```
- Inner Join으로 데이터 무결성 보장
- 단계별 검증

### 2. 파생변수 생성 로직이 명확
```python
merged_df['인구당_총CCTV'] = (merged_df['총_CCTV'] / merged_df['인구수'] * 1000).round(2)
```
- 인구 1000명당 표준화
- 소수점 2자리 반올림으로 가독성 향상

### 3. 등급 분류 함수
```python
def classify_cctv_density(value):
    if value <= cctv_quartiles[0.25]:
        return '낮음'
    ...
```
- 사분위수 기반 객관적 분류
- Day 9 클러스터링과 연계 가능

### 4. 컬럼 카테고리별 정리
- 최종 컬럼 리스트를 카테고리별로 분류하여 출력
- 가독성 및 이해도 향상

### 5. 초기 상관분석 포함
- 산점도 + 상관계수 계산
- Day 4의 본격 분석 전 탐색적 분석

---

## ❌ 문제점 및 개선 필요 사항 (Issues)

### 🟡 Warning (경고 - 개선 권장)

#### 1. 등급 분류 함수를 helpers.py로 이동 권장

**문제**:
```python
# 노트북 내부에 정의
def classify_cctv_density(value):
    ...
def classify_crime_rate(value):
    ...
```

**영향**:
- Day 9 클러스터링에서도 동일 분류 필요
- 중복 코드 발생 가능성

**개선안**:
```python
# utils/helpers.py에 추가
def classify_by_quartiles(series, labels=None):
    """
    사분위수 기반 등급 분류

    Args:
        series (pd.Series): 분류할 시리즈
        labels (list, optional): 등급 라벨 (기본: ['낮음', '보통', '높음', '매우높음'])

    Returns:
        pd.Series: 등급이 할당된 시리즈
    """
    if labels is None:
        labels = ['낮음', '보통', '높음', '매우높음']

    return pd.qcut(series, q=4, labels=labels, duplicates='drop')
```

#### 2. 상관계수 계산을 별도 함수로 분리

**문제**:
- 상관계수 계산이 노트북에 하드코딩
- Day 4에서 더 상세한 상관분석 필요

**개선안**:
```python
# utils/helpers.py에 추가
def calculate_correlations(df, x_cols, y_col, method='pearson'):
    """
    여러 X 변수와 Y 변수 간의 상관계수 계산

    Returns:
        pd.DataFrame: 상관계수 및 p-value
    """
    from scipy import stats

    results = []
    for x_col in x_cols:
        if method == 'pearson':
            corr, pvalue = stats.pearsonr(df[x_col], df[y_col])
        elif method == 'spearman':
            corr, pvalue = stats.spearmanr(df[x_col], df[y_col])

        results.append({
            '변수': x_col,
            '상관계수': corr,
            'p-value': pvalue,
            '유의성': '유의' if pvalue < 0.05 else '비유의'
        })

    return pd.DataFrame(results)
```

#### 3. 파생변수 생성 로직 반복문 활용 부족

**문제**:
```python
# 현재
merged_df['인구당_총CCTV'] = ...
for cctv_type in CCTV_RANGE.keys():
    merged_df[f'인구당_{cctv_type}'] = ...
```
- 총CCTV만 별도 처리 → 일관성 부족

**개선안**:
```python
# 개선
cctv_cols = ['총_CCTV'] + list(CCTV_RANGE.keys())
for cctv_col in cctv_cols:
    merged_df[f'인구당_{cctv_col}'] = (merged_df[cctv_col] / merged_df['인구수'] * 1000).round(2)
```

---

### 🟢 Minor (사소 - 개선 시 더 좋음)

#### 4. 데이터 타입 최적화

**문제**:
- 모든 수치형 컬럼이 float64
- 메모리 사용량 증가

**개선안**:
```python
# 정수형 컬럼은 int로 변환
int_cols = ['총_CCTV', '방범용', '교통단속용', ...CRIME_RANGE.keys(), '인구수']
for col in int_cols:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col].astype('int32')

# float 컬럼은 float32로
float_cols = ['인구당_총CCTV', '인구당_방범용', ...]
for col in float_cols:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col].astype('float32')
```

#### 5. 컬럼명 일관성

**문제**:
- '인구당_총CCTV' vs '인구당_방범용' (총 vs 타입명)
- 혼동 가능성

**개선안**:
```python
# 일관되게 변경
merged_df.rename(columns={'인구당_총CCTV': '인구당_CCTV합계'}, inplace=True)
```

#### 6. 시각화 함수 재사용

**문제**:
- 산점도 생성 코드가 직접 작성됨
- Day 4-5에서도 유사한 시각화 필요

**개선안**:
```python
# utils/helpers.py에 추가
def plot_correlation_scatter(df, x_col, y_col, title, color='blue', save_path=None):
    """상관관계 산점도 생성"""
    ...
```

---

## 🔧 수정 우선순위

### Priority 1 (Day 4 전 수정)
1. ✅ `classify_by_quartiles()` 함수 helpers.py로 이동
2. ✅ `calculate_correlations()` 함수 추가 (Day 4용)
3. ⚠️ 파생변수 생성 로직 반복문으로 통일

### Priority 2 (Day 4-5에서 고려)
4. ⚠️ 상관 산점도 함수 `plot_correlation_scatter()` 추가
5. ⚠️ 데이터 타입 최적화 (메모리 절약)

### Priority 3 (여유 있을 때)
6. ⚠️ 컬럼명 일관성 개선
7. ⚠️ 주석 추가

---

## 📝 코드 개선 체크리스트

### helpers.py 추가 함수
- [ ] `classify_by_quartiles(series, labels)`: 사분위수 등급 분류
- [ ] `calculate_correlations(df, x_cols, y_col, method)`: 상관계수 계산
- [ ] `plot_correlation_scatter(df, x_col, y_col, ...)`: 상관 산점도 (선택)

### 노트북 코드 수정
- [ ] 등급 분류 함수 → helpers 함수 사용
- [ ] 파생변수 생성 로직 반복문으로 통일
- [ ] 상관분석 → Day 4로 이동 (초기 탐색만 유지)

---

## 📌 추가 제안 사항

### 1. 파생변수 메타데이터 저장

```python
# 파생변수 정의를 JSON으로 저장
derived_vars_metadata = {
    '인구당_총CCTV': {
        'description': '인구 1000명당 총 CCTV 대수',
        'unit': '대/천명',
        'formula': '총_CCTV / 인구수 * 1000'
    },
    ...
}

import json
with open('../data/derived_variables.json', 'w', encoding='utf-8') as f:
    json.dump(derived_vars_metadata, f, ensure_ascii=False, indent=2)
```

### 2. 데이터 품질 검증 강화

```python
# 파생변수 생성 후 검증
assert (merged_df['인구당_총CCTV'] >= 0).all(), "음수 값 발견"
assert not merged_df['인구당_총CCTV'].isnull().any(), "결측치 발견"
```

### 3. 로깅 추가

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"데이터 병합 완료: {merged_df.shape}")
logger.info(f"파생변수 생성 완료: {len(derived_cols)}개")
```

---

## 🎯 Day 4 준비사항

Day 4에서는 다음 작업을 수행:
1. Day 3 통합 데이터 로드
2. 상관분석 (Pearson, Spearman) 본격 수행
3. Heatmap, Bar Chart, Scatter Plot 생성
4. 자치구별 비교 분석

**권장 사항**:
- Day 4 작업 전에 Priority 1 항목 수정
- helpers.py에 상관분석 및 시각화 함수 추가

---

## 📊 최종 평가

**개선 후 예상 점수**: 9.5/10

**주요 개선 포인트**:
- ✅ 등급 분류 함수화 (재사용성 ↑)
- ✅ 상관분석 함수 추가 (Day 4 준비)
- ✅ 파생변수 생성 로직 통일 (일관성 ↑)

**Day 3 평가 종합**:
- 데이터 통합 및 파생변수 생성이 체계적으로 잘 수행됨
- Day 1-2의 개선 사항을 잘 적용
- 일부 함수들을 helpers.py로 이동하면 더욱 우수한 구조

---

**리뷰 완료일**: 2025-07-06
**다음 리뷰**: Day 4 완료 후 (2025-07-07)

# Day 2 코드 리뷰 및 개선 사항

**리뷰 날짜**: 2025-07-05
**리뷰 대상**: notebooks/02_data_cleaning.ipynb
**리뷰어**: Claude Code

---

## 📊 전체 평가

| 항목 | 점수 | 코멘트 |
|------|------|--------|
| **코드 품질** | 8.5/10 | Day 1 개선 사항 잘 적용 |
| **재현성** | 9/10 | utils 모듈 활용 우수 |
| **문서화** | 9/10 | 섹션별 설명 명확 |
| **효율성** | 8/10 | 불필요한 중복 거의 없음 |
| **확장성** | 8.5/10 | 함수화 잘 되어 있음 |

**총점**: 8.6/10

---

## ✅ 잘된 점 (Strengths)

### 1. Day 1 개선 사항 적극 반영
```python
from utils.constants import ...
from utils.helpers import ...
```
- utils 모듈의 함수들을 적절히 활용
- 코드 중복 최소화

### 2. 체계적인 데이터 정제 프로세스
- 로드 → 표준화 → 검증 → 집계 → 이상치 탐지 → 저장 순서가 논리적

### 3. 자치구명 표준화 함수
```python
def standardize_district_name(name):
    name = str(name).strip()
    name = name.replace('서울특별시 ', '').replace('서울시 ', '')
    return name
```
- 실무적으로 유용한 전처리 로직

### 4. IQR 방법을 이용한 이상치 탐지
```python
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    ...
```
- 통계적으로 타당한 방법 사용
- 함수화하여 재사용 가능

### 5. 이상치 처리 방안 문서화
- 이상치를 유지하는 근거를 명확히 제시
- 향후 분석 단계에서의 주의사항 포함

### 6. 시각화 개선
- 막대 위에 값 표시
- 파이 차트로 비율 명확히 표현
- 색상 일관성 유지

---

## ❌ 문제점 및 개선 필요 사항 (Issues)

### 🟡 Warning (경고 - 개선 권장)

#### 1. 자치구명 표준화 함수를 helpers.py로 이동 권장

**문제**:
```python
# 노트북 내부에 정의
def standardize_district_name(name):
    ...
```

**영향**:
- Day 3 이후 노트북에서도 동일 함수 필요
- 중복 코드 발생 가능성

**개선안**:
```python
# utils/helpers.py에 추가
def standardize_district_name(name):
    """
    자치구명 표준화
    ...
    """
    name = str(name).strip()
    name = name.replace('서울특별시 ', '').replace('서울시 ', '').replace('서울 ', '')
    return name
```

#### 2. IQR 이상치 탐지 함수도 helpers.py로 이동 권장

**문제**:
- Day 7-8 회귀분석 단계에서도 이상치 탐지 필요
- 현재는 노트북 내부에만 존재

**개선안**:
```python
# utils/helpers.py에 추가
def detect_outliers_iqr(df, column, threshold=1.5):
    """
    IQR 방법을 이용한 이상치 탐지
    ...
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound
```

#### 3. 시각화 함수 재사용성 개선

**문제**:
- CCTV/범죄 유형별 시각화 코드가 유사하지만 함수화되지 않음

**개선안**:
```python
# utils/helpers.py에 추가
def plot_category_analysis(df, categories, category_name, colors=None,
                            save_path=None):
    """
    카테고리별 평균 및 비율 시각화 (막대 + 파이 차트)
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 막대 차트
    means = [df[cat].mean() for cat in categories]
    axes[0].bar(categories, means, color=colors, edgecolor='black', alpha=0.7)
    ...

    # 파이 차트 (필요 시)
    ...

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
```

#### 4. 비율 계산 로직 간소화

**문제**:
```python
cctv_df['방범용_비율'] = (cctv_df['방범용'] / cctv_df['총_CCTV'] * 100).round(2)
cctv_df['교통단속용_비율'] = (cctv_df['교통단속용'] / cctv_df['총_CCTV'] * 100).round(2)
# ... 반복
```

**개선안**:
```python
# 반복문 사용
for cctv_type in CCTV_RANGE.keys():
    cctv_df[f'{cctv_type}_비율'] = (cctv_df[cctv_type] / cctv_df['총_CCTV'] * 100).round(2)
```

#### 5. 데이터 검증 강화

**문제**:
- 데이터 로드 후 `validate_data()` 함수를 호출하지 않음
- 결측치/이상값 확인 누락

**개선안**:
```python
# 데이터 로드 직후
cctv_df = pd.read_csv(cctv_path, encoding='utf-8-sig')
validate_data(cctv_df, expected_rows=25, required_columns=['자치구', '총_CCTV'])
```

---

### 🟢 Minor (사소 - 개선 시 더 좋음)

#### 6. 에러 핸들링 개선

**문제**:
```python
try:
    cctv_df = pd.read_csv(...)
except FileNotFoundError as e:
    print(f"❌ 파일을 찾을 수 없습니다: {e}")
    # 이후 코드가 계속 실행됨
```

**개선안**:
```python
try:
    cctv_df = pd.read_csv(...)
except FileNotFoundError as e:
    print(f"❌ 파일을 찾을 수 없습니다: {e}")
    raise  # 예외를 다시 발생시켜 노트북 실행 중단
```

#### 7. 상수 추가 필요

**문제**:
- `threshold=1.5` (IQR 임계값)이 하드코딩
- 향후 조정 시 불편

**개선안**:
```python
# utils/constants.py에 추가
IQR_THRESHOLD = 1.5
```

#### 8. 주석 추가

**문제**:
- 일부 복잡한 로직에 주석 부족

**개선안**:
```python
# 각 막대 위에 값 표시 (가독성 향상)
for i, (ctype, mean_val) in enumerate(zip(cctv_types, cctv_means)):
    axes[0].text(i, mean_val + 30, f'{mean_val:.0f}', ha='center')
```

---

## 🔧 수정 우선순위

### Priority 1 (Day 3 전 수정)
1. ✅ `standardize_district_name()` 함수를 helpers.py로 이동
2. ✅ `detect_outliers_iqr()` 함수를 helpers.py로 이동
3. ✅ 비율 계산 로직 반복문으로 간소화
4. ✅ 데이터 로드 후 `validate_data()` 호출 추가

### Priority 2 (Day 4-5에서 고려)
5. ⚠️ 시각화 함수 `plot_category_analysis()` 추가 (helpers.py)
6. ⚠️ IQR_THRESHOLD 상수화 (constants.py)

### Priority 3 (여유 있을 때)
7. ⚠️ 에러 핸들링 개선
8. ⚠️ 주석 추가

---

## 📝 코드 개선 체크리스트

### helpers.py 추가 함수
- [ ] `standardize_district_name(name)`: 자치구명 표준화
- [ ] `detect_outliers_iqr(df, column, threshold)`: IQR 이상치 탐지
- [ ] `plot_category_analysis(df, categories, ...)`: 카테고리별 분석 시각화 (선택)

### constants.py 추가 상수
- [ ] `IQR_THRESHOLD = 1.5`: IQR 임계값

### 노트북 코드 수정
- [ ] 비율 계산 로직 반복문으로 변경
- [ ] 데이터 로드 후 검증 추가
- [ ] helpers.py의 새 함수들 활용

---

## 📌 추가 제안 사항

### 1. 데이터 품질 보고서 자동 생성

```python
def generate_data_quality_report(df, df_name):
    """
    데이터 품질 보고서 생성
    - 결측치 비율
    - 중복 행 개수
    - 각 컬럼의 데이터 타입
    - 수치형 컬럼의 이상치 개수
    """
    report = {
        'name': df_name,
        'shape': df.shape,
        'missing_rate': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicates': df.duplicated().sum(),
        'dtypes': df.dtypes.to_dict()
    }
    return report
```

### 2. 데이터 딕셔너리 작성

- 각 컬럼의 의미, 단위, 범위 문서화
- `data/DATA_DICTIONARY.md` 파일 생성 권장

### 3. 로깅 추가 고려

```python
import logging
logger = logging.getLogger(__name__)
logger.info("데이터 정제 시작")
logger.info(f"CCTV 데이터 로드 완료: {len(cctv_df)}행")
```

---

## 🎯 Day 3 준비사항

Day 3에서는 다음 작업을 수행:
1. Day 2에서 정제한 데이터 로드
2. 세 개 데이터프레임 병합 (Inner Join)
3. 파생변수 생성 (인구당 CCTV, 인구당 범죄율 등)
4. 통합 데이터 검증 및 저장

**권장 사항**:
- Day 3 작업 전에 Priority 1 항목 모두 수정
- helpers.py에 새 함수 추가 후 노트북 다시 실행하여 검증

---

## 📊 최종 평가

**개선 후 예상 점수**: 9.2/10

**주요 개선 포인트**:
- ✅ 공통 함수 helpers.py로 이동 (재사용성 ↑)
- ✅ 비율 계산 로직 간소화 (가독성 ↑)
- ✅ 데이터 검증 강화 (품질 ↑)
- ✅ 상수화 (유지보수성 ↑)

**Day 2 평가 종합**:
- Day 1의 개선 사항을 잘 적용했으며, 체계적인 데이터 정제 프로세스 구축
- 일부 함수들을 helpers.py로 이동하면 더욱 우수한 코드 구조

---

**리뷰 완료일**: 2025-07-05
**다음 리뷰**: Day 3 완료 후 (2025-07-06)

"""
전체 분석 파이프라인 실행 스크립트
Day 2부터 Day 12까지 순차 실행
"""

import sys
import os
sys.path.append('.')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from utils import *

print("="*80)
print("서울시 CCTV 분석 프로젝트 - 전체 파이프라인 실행")
print("="*80)

# ============================================================================
# Day 2: Data Cleaning
# ============================================================================
print("\n=== Day 2: Data Cleaning ===")

# Load raw data
df_cctv = pd.read_csv(os.path.join(DATA_PATHS['raw'], 'cctv_seoul_2023_sample.csv'), encoding='utf-8-sig')
df_crime = pd.read_csv(os.path.join(DATA_PATHS['raw'], 'crime_seoul_2023_sample.csv'), encoding='utf-8-sig')
df_population = pd.read_csv(os.path.join(DATA_PATHS['raw'], 'population_seoul_2023_sample.csv'), encoding='utf-8-sig')

# Standardize district names
for df in [df_cctv, df_crime, df_population]:
    df['자치구'] = df['자치구'].apply(standardize_district_name)

# Calculate ratios for CCTV
cctv_types = ['방범용', '교통단속용', '어린이안전용', '기타']
df_cctv = calculate_ratio_columns(df_cctv, cctv_types, '총_CCTV')

# Calculate ratios for Crime
crime_types = ['절도', '강도', '차량범죄', '공공장소폭력', '성범죄']
df_crime = calculate_ratio_columns(df_crime, crime_types, '총_범죄')

# Save cleaned data
os.makedirs(DATA_PATHS['processed'], exist_ok=True)
df_cctv.to_csv(os.path.join(DATA_PATHS['processed'], 'cctv_cleaned.csv'), index=False, encoding='utf-8-sig')
df_crime.to_csv(os.path.join(DATA_PATHS['processed'], 'crime_cleaned.csv'), index=False, encoding='utf-8-sig')
df_population.to_csv(os.path.join(DATA_PATHS['processed'], 'population_cleaned.csv'), index=False, encoding='utf-8-sig')

print("[OK] Day 2 completed - cleaned data saved")

# ============================================================================
# Day 3: Data Integration
# ============================================================================
print("\n=== Day 3: Data Integration ===")

# Merge data
merged = df_cctv.merge(df_crime, on='자치구', how='inner')
merged = merged.merge(df_population, on='자치구', how='inner')

# Calculate per-capita metrics
merged['인구당_총CCTV'] = (merged['총_CCTV'] / merged['인구수'] * 1000).round(2)
merged['인구당_방범용'] = (merged['방범용'] / merged['인구수'] * 1000).round(2)
merged['인구당_교통단속용'] = (merged['교통단속용'] / merged['인구수'] * 1000).round(2)
merged['인구당_어린이안전용'] = (merged['어린이안전용'] / merged['인구수'] * 1000).round(2)

merged['CCTV효과범죄_합계'] = merged[['절도', '강도', '차량범죄']].sum(axis=1)
merged['인구당_CCTV효과범죄율'] = (merged['CCTV효과범죄_합계'] / merged['인구수'] * 1000).round(2)
merged['인구당_절도율'] = (merged['절도'] / merged['인구수'] * 1000).round(2)
merged['인구당_강도율'] = (merged['강도'] / merged['인구수'] * 1000).round(2)
merged['인구당_차량범죄율'] = (merged['차량범죄'] / merged['인구수'] * 1000).round(2)

# Create categorical variables
merged['CCTV밀도_등급'] = pd.qcut(merged['인구당_총CCTV'], q=4, labels=['하', '중하', '중상', '상'])
merged['범죄율_등급'] = pd.qcut(merged['인구당_CCTV효과범죄율'], q=4, labels=['하', '중하', '중상', '상'])

merged.to_csv(os.path.join(DATA_PATHS['processed'], 'integrated_data.csv'), index=False, encoding='utf-8-sig')

print(f"[OK] Day 3 completed - integrated data saved ({merged.shape})")

# ============================================================================
# Day 4-8: Analysis (without plots for speed)
# ============================================================================
print("\n=== Day 4-8: Running Analysis ===")

# Correlation analysis
corr_matrix = merged[['인구당_총CCTV', '인구당_방범용', '인구당_CCTV효과범죄율', '인구밀도']].corr()
print(f"Correlation (방범용 vs 범죄율): {merged['인구당_방범용'].corr(merged['인구당_CCTV효과범죄율']):.4f}")

# Regression analysis
X_cols = ['인구당_방범용', '인구밀도']
y_col = '인구당_CCTV효과범죄율'
X = merged[X_cols]
y = merged[y_col]
X_with_const = sm.add_constant(X)
model = sm.OLS(y, X_with_const).fit()

print(f"R-squared: {model.rsquared:.4f}")
print(f"Adj R-squared: {model.rsquared_adj:.4f}")
print("[OK] Regression model completed")

# ============================================================================
# Day 9: Region Classification
# ============================================================================
print("\n=== Day 9: Region Classification ===")

cctv_median = merged['인구당_방범용'].median()
crime_median = merged['인구당_CCTV효과범죄율'].median()

def classify_quadrant(row):
    cctv = row['인구당_방범용']
    crime = row['인구당_CCTV효과범죄율']
    if cctv >= cctv_median and crime >= crime_median:
        return 'Q1: 고CCTV/고범죄'
    elif cctv < cctv_median and crime >= crime_median:
        return 'Q2: 저CCTV/고범죄 (우선순위)'
    elif cctv < cctv_median and crime < crime_median:
        return 'Q3: 저CCTV/저범죄'
    else:
        return 'Q4: 고CCTV/저범죄 (효과적)'

merged['분면'] = merged.apply(classify_quadrant, axis=1)
merged.to_csv(os.path.join(DATA_PATHS['processed'], 'integrated_data_with_quadrant.csv'), index=False, encoding='utf-8-sig')

print(f"[OK] Day 9 completed - quadrant classification saved")
print(merged['분면'].value_counts())

# ============================================================================
# Day 10: Policy Recommendations
# ============================================================================
print("\n=== Day 10: Policy Recommendations ===")

policy_table = pd.DataFrame([
    {
        '분면': 'Q2 (저CCTV/고범죄)',
        '자치구수': len(merged[merged['분면'] == 'Q2: 저CCTV/고범죄 (우선순위)']),
        '우선순위': '최우선',
        '정책': '방범용 CCTV 긴급 설치',
        '예산': '상',
        '기간': '6개월'
    },
    {
        '분면': 'Q1 (고CCTV/고범죄)',
        '자치구수': len(merged[merged['분면'] == 'Q1: 고CCTV/고범죄']),
        '우선순위': '높음',
        '정책': '종합 방범 대책 (조명+순찰)',
        '예산': '중상',
        '기간': '1년'
    },
    {
        '분면': 'Q4 (고CCTV/저범죄)',
        '자치구수': len(merged[merged['분면'] == 'Q4: 고CCTV/저범죄 (효과적)']),
        '우선순위': '중간',
        '정책': '모범 사례 벤치마킹',
        '예산': '하',
        '기간': '3개월'
    },
    {
        '분면': 'Q3 (저CCTV/저범죄)',
        '자치구수': len(merged[merged['분면'] == 'Q3: 저CCTV/저범죄']),
        '우선순위': '낮음',
        '정책': '현상 유지 + 모니터링',
        '예산': '하',
        '기간': '지속'
    }
])

os.makedirs(DATA_PATHS['reports'], exist_ok=True)
policy_table.to_csv(os.path.join(DATA_PATHS['reports'], 'day10_policy_summary.csv'), index=False, encoding='utf-8-sig')

print("[OK] Day 10 completed - policy recommendations saved")

# ============================================================================
# Day 12: Final Report
# ============================================================================
print("\n=== Day 12: Generating Final Report ===")

stats_summary = {
    'corr_total_cctv_crime': merged['인구당_총CCTV'].corr(merged['인구당_CCTV효과범죄율']),
    'corr_security_cctv_crime': merged['인구당_방범용'].corr(merged['인구당_CCTV효과범죄율']),
    'corr_density_crime': merged['인구밀도'].corr(merged['인구당_CCTV효과범죄율']),
    'r_squared': model.rsquared,
    'adj_r_squared': model.rsquared_adj,
    'f_pvalue': model.f_pvalue,
    'coef_security': model.params['인구당_방범용'],
    'pval_security': model.pvalues['인구당_방범용'],
    'q2_count': len(merged[merged['분면'] == 'Q2: 저CCTV/고범죄 (우선순위)']),
    'q2_districts': ', '.join(merged[merged['분면'] == 'Q2: 저CCTV/고범죄 (우선순위)']['자치구'].tolist()),
    'q4_count': len(merged[merged['분면'] == 'Q4: 고CCTV/저범죄 (효과적)']),
    'q4_districts': ', '.join(merged[merged['분면'] == 'Q4: 고CCTV/저범죄 (효과적)']['자치구'].tolist())
}

final_report = f"""# 서울시 CCTV 설치 현황과 범죄 발생 상관 분석 - 최종 보고서

**분석 기간**: 2025년 7월 4일 ~ 7월 15일
**데이터 기준**: 서울시 25개 자치구 (2023년)

## Executive Summary

### 핵심 발견사항

- **CCTV-범죄 상관관계**
  - 인구당 방범용 CCTV vs 범죄율: r = {stats_summary['corr_security_cctv_crime']:.4f}
  - 인구당 총CCTV vs 범죄율: r = {stats_summary['corr_total_cctv_crime']:.4f}

- **회귀분석 결과**
  - R² = {stats_summary['r_squared']:.4f} (설명력 {stats_summary['r_squared']*100:.1f}%)
  - 방범용 CCTV 계수 = {stats_summary['coef_security']:.4f} (p = {stats_summary['pval_security']:.4f})
  - {'통계적으로 유의미함' if stats_summary['pval_security'] < 0.05 else '통계적으로 유의미하지 않음'}

- **우선순위 지역**
  - Q2 (저CCTV/고범죄): {stats_summary['q2_count']}개 자치구
  - 대상: {stats_summary['q2_districts'] if stats_summary['q2_districts'] else '없음'}

- **효과적 사례**
  - Q4 (고CCTV/저범죄): {stats_summary['q4_count']}개 자치구
  - 대상: {stats_summary['q4_districts'] if stats_summary['q4_districts'] else '없음'}

### 주요 정책 제언

1. **단기 (6개월)**: Q2 지역 방범용 CCTV 긴급 설치 (최소 중앙값 수준까지)
2. **중기 (1년)**: Q1 지역 종합 방범 대책 (CCTV + 조명 + 순찰)
3. **장기 (2년+)**: 시계열 데이터 구축 및 인과관계 검증 (이중차분법)

## 분석 결과 요약

### 데이터 기술통계

| 변수 | 평균 | 표준편차 | 최소값 | 최대값 |
|------|------|----------|--------|--------|
| 인구당 방범용 CCTV | {merged['인구당_방범용'].mean():.2f} | {merged['인구당_방범용'].std():.2f} | {merged['인구당_방범용'].min():.2f} | {merged['인구당_방범용'].max():.2f} |
| 인구당 CCTV효과범죄율 | {merged['인구당_CCTV효과범죄율'].mean():.2f} | {merged['인구당_CCTV효과범죄율'].std():.2f} | {merged['인구당_CCTV효과범죄율'].min():.2f} | {merged['인구당_CCTV효과범죄율'].max():.2f} |
| 인구밀도 | {merged['인구밀도'].mean():.0f} | {merged['인구밀도'].std():.0f} | {merged['인구밀도'].min():.0f} | {merged['인구밀도'].max():.0f} |

### 회귀분석 결과

**모형**: 인구당_CCTV효과범죄율 = β₀ + β₁(인구당_방범용) + β₂(인구밀도) + ε

| 변수 | 계수 | p-value | 유의성 |
|------|------|---------|---------|
| 인구당_방범용 | {model.params['인구당_방범용']:.4f} | {model.pvalues['인구당_방범용']:.4f} | {'***' if model.pvalues['인구당_방범용'] < 0.001 else '**' if model.pvalues['인구당_방범용'] < 0.01 else '*' if model.pvalues['인구당_방범용'] < 0.05 else 'n.s.'} |
| 인구밀도 | {model.params['인구밀도']:.6f} | {model.pvalues['인구밀도']:.4f} | {'***' if model.pvalues['인구밀도'] < 0.001 else '**' if model.pvalues['인구밀도'] < 0.01 else '*' if model.pvalues['인구밀도'] < 0.05 else 'n.s.'} |

- R² = {stats_summary['r_squared']:.4f}
- Adjusted R² = {stats_summary['adj_r_squared']:.4f}
- F-statistic p-value = {stats_summary['f_pvalue']:.6f}

### 지역 분류 (4분면)

| 분면 | 자치구 수 | 정책 우선순위 |
|------|-----------|---------------|
| Q2 (저CCTV/고범죄) | {stats_summary['q2_count']} | 최우선 - 방범용 CCTV 긴급 설치 |
| Q1 (고CCTV/고범죄) | {len(merged[merged['분면'] == 'Q1: 고CCTV/고범죄'])} | 높음 - 종합 방범 대책 |
| Q4 (고CCTV/저범죄) | {stats_summary['q4_count']} | 중간 - 모범 사례 벤치마킹 |
| Q3 (저CCTV/저범죄) | {len(merged[merged['분면'] == 'Q3: 저CCTV/저범죄'])} | 낮음 - 현상 유지 |

## 결론

본 분석은 서울시 25개 자치구의 CCTV 설치 현황과 범죄 발생 간의 관계를 실증적으로 분석하였다.
주요 발견사항으로는 방범용 CCTV와 범죄율 간 {'음의 상관관계' if stats_summary['corr_security_cctv_crime'] < 0 else '양의 상관관계'}가 확인되었으며,
4분면 분류를 통해 {stats_summary['q2_count']}개의 우선순위 설치 지역을 식별하였다.

정책적 시사점으로는 저CCTV/고범죄 지역에 방범용 CCTV를 집중 설치하고,
고CCTV/저범죄 지역의 모범 사례를 벤치마킹할 것을 제안한다.

---

**보고서 생성일**: 2025년 7월 15일
**데이터 분석 도구**: Python (pandas, statsmodels, matplotlib, seaborn)
**재현성**: 샘플 데이터(RANDOM_SEED=42) 사용
"""

with open(os.path.join(DATA_PATHS['reports'], 'FINAL_REPORT.md'), 'w', encoding='utf-8') as f:
    f.write(final_report)

print("[OK] Day 12 completed - final report generated")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print("전체 파이프라인 실행 완료!")
print("="*80)
print("\n생성된 파일:")
print(f"  - data/raw/: 3개 샘플 데이터 CSV")
print(f"  - data/processed/: 정제 및 통합 데이터 CSV")
print(f"  - results/reports/FINAL_REPORT.md: 최종 보고서")
print(f"  - results/reports/day10_policy_summary.csv: 정책 제언 요약표")
print("\n다음 단계:")
print("  1. results/reports/FINAL_REPORT.md 확인")
print("  2. Pandoc으로 PDF 변환")
print("  3. GitHub 저장소에 업로드")
print("="*80)

"""
실제 데이터로 전체 분석 실행
2024/2025 서울시 CCTV 및 범죄 데이터 분석
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("서울시 CCTV와 범죄 상관관계 분석 - 실제 데이터")
print("="*80)

# ============================================================================
# 1. 데이터 로드
# ============================================================================
print("\n[1/6] 데이터 로드 중...")

# 개별 데이터 로드
df_cctv = pd.read_csv('data/raw/cctv_seoul_2024.csv', encoding='utf-8-sig')
df_crime = pd.read_csv('data/raw/crime_seoul_2024.csv', encoding='utf-8-sig')
df_population = pd.read_csv('data/raw/population_seoul_2024.csv', encoding='utf-8-sig')

# 데이터 병합
merged = df_cctv.merge(df_crime, on='자치구', how='inner')
merged = merged.merge(df_population, on='자치구', how='inner')

print(f"  - 자치구: {len(merged)}개")
print(f"  - 컬럼: {len(merged.columns)}개")

# ============================================================================
# 2. 파생 변수 생성
# ============================================================================
print("\n[2/6] 파생 변수 생성 중...")

# 인구 천 명당 비율 계산
merged['CCTV_per_1000'] = (merged['CCTV_총계'] / merged['총인구']) * 1000
merged['범죄_per_1000'] = (merged['총범죄_발생'] / merged['총인구']) * 1000
merged['방범CCTV_per_1000'] = (merged['방범용'] / merged['총인구']) * 1000

# CCTV 효과 범죄 계산 (절도 + 강도)
# 강간강제추행은 성범죄로 분류하고, 나머지는 폭력/살인으로 분류
merged['CCTV효과범죄'] = merged['절도_발생'] + merged['강도_발생']
merged['CCTV효과범죄_per_1000'] = (merged['CCTV효과범죄'] / merged['총인구']) * 1000

print(f"  - CCTV_per_1000: {merged['CCTV_per_1000'].mean():.2f}")
print(f"  - 범죄_per_1000: {merged['범죄_per_1000'].mean():.2f}")
print(f"  - CCTV효과범죄_per_1000: {merged['CCTV효과범죄_per_1000'].mean():.2f}")

# ============================================================================
# 3. 기술통계
# ============================================================================
print("\n[3/6] 기술통계 분석 중...")

stats_summary = merged[['CCTV_총계', '총범죄_발생', '총인구',
                         'CCTV_per_1000', '범죄_per_1000', 'CCTV효과범죄_per_1000']].describe()
print(stats_summary)

# ============================================================================
# 4. 상관분석
# ============================================================================
print("\n[4/6] 상관분석 중...")

# Pearson 상관계수
correlation_vars = ['CCTV_총계', '방범용', '총범죄_발생', '총인구',
                    'CCTV_per_1000', '방범CCTV_per_1000', '범죄_per_1000', 'CCTV효과범죄_per_1000']
corr_matrix = merged[correlation_vars].corr()

print("\n상관계수 매트릭스:")
print(corr_matrix)

print(f"\nCCTV_per_1000 vs 범죄_per_1000 상관계수: {corr_matrix.loc['CCTV_per_1000', '범죄_per_1000']:.4f}")
print(f"방범CCTV_per_1000 vs CCTV효과범죄_per_1000 상관계수: {corr_matrix.loc['방범CCTV_per_1000', 'CCTV효과범죄_per_1000']:.4f}")

# Pearson correlation test (CCTV vs 전체 범죄)
r_corr, p_value = stats.pearsonr(merged['CCTV_per_1000'], merged['범죄_per_1000'])
print(f"\n전체 CCTV vs 전체 범죄: Pearson r = {r_corr:.4f}, p-value = {p_value:.4f}")

# Pearson correlation test (방범CCTV vs CCTV효과범죄)
r_corr2, p_value2 = stats.pearsonr(merged['방범CCTV_per_1000'], merged['CCTV효과범죄_per_1000'])
print(f"방범 CCTV vs CCTV효과범죄: Pearson r = {r_corr2:.4f}, p-value = {p_value2:.4f}")

# ============================================================================
# 5. 시각화
# ============================================================================
print("\n[5/6] 시각화 생성 중...")

os.makedirs('results/figures', exist_ok=True)

# 5-1. 산점도: CCTV vs 범죄
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(merged['CCTV_per_1000'], merged['범죄_per_1000'], alpha=0.6, s=100)

# 선형 회귀선
z = np.polyfit(merged['CCTV_per_1000'], merged['범죄_per_1000'], 1)
poly_line = np.poly1d(z)
ax.plot(merged['CCTV_per_1000'], poly_line(merged['CCTV_per_1000']),
        "r--", alpha=0.8, label=f'회귀선 (r={r_corr:.3f})')

# 자치구명 표시
for idx, row in merged.iterrows():
    ax.annotate(row['자치구'],
                (row['CCTV_per_1000'], row['범죄_per_1000']),
                fontsize=8, alpha=0.7)

ax.set_xlabel('인구 천명당 CCTV 대수', fontsize=12)
ax.set_ylabel('인구 천명당 범죄 발생 건수', fontsize=12)
ax.set_title('서울시 자치구별 CCTV와 범죄 발생 상관관계 (2024년 실제 데이터)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/figures/scatter_cctv_crime_real.png', dpi=300)
print("  - scatter_cctv_crime_real.png 저장")

# 5-2. 상관계수 히트맵
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, square=True, ax=ax, cbar_kws={'label': '상관계수'})
ax.set_title('변수 간 상관계수 매트릭스', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/figures/correlation_heatmap_real.png', dpi=300)
print("  - correlation_heatmap_real.png 저장")

# 5-3. CCTV 상위/하위 자치구
merged_sorted = merged.sort_values('CCTV_총계', ascending=False)
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#ff6b6b' if x < merged['범죄_per_1000'].median() else '#4ecdc4'
          for x in merged_sorted['범죄_per_1000']]
ax.barh(merged_sorted['자치구'], merged_sorted['CCTV_총계'], color=colors, alpha=0.7)
ax.set_xlabel('CCTV 총 대수', fontsize=12)
ax.set_title('자치구별 CCTV 설치 현황 (2024년 실제 데이터)', fontsize=14, fontweight='bold')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('results/figures/cctv_by_district_real.png', dpi=300)
print("  - cctv_by_district_real.png 저장")

# ============================================================================
# 6. 결과 저장
# ============================================================================
print("\n[6/6] 분석 결과 저장 중...")

os.makedirs('data/processed', exist_ok=True)
merged.to_csv('data/processed/integrated_data_with_analysis.csv',
              index=False, encoding='utf-8-sig')
print("  - integrated_data_with_analysis.csv 저장")

# 요약 통계 저장
os.makedirs('results/reports', exist_ok=True)
with open('results/reports/analysis_summary.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("서울시 CCTV와 범죄 상관관계 분석 결과 요약\n")
    f.write("="*80 + "\n\n")

    f.write(f"분석 대상: {len(merged)}개 자치구\n")
    f.write(f"데이터 기준: CCTV(2024년), 범죄(2024년), 인구(2024년)\n\n")

    f.write("주요 통계:\n")
    f.write(f"  - 평균 CCTV 대수: {merged['CCTV_총계'].mean():.0f}대\n")
    f.write(f"  - 평균 범죄 발생: {merged['총범죄_발생'].mean():.0f}건\n")
    f.write(f"  - 평균 인구: {merged['총인구'].mean():.0f}명\n")
    f.write(f"  - 평균 CCTV효과범죄: {merged['CCTV효과범죄'].mean():.0f}건\n\n")

    f.write("상관분석 결과:\n")
    f.write(f"  - 전체 CCTV vs 전체 범죄 상관계수: {r_corr:.4f}\n")
    f.write(f"    p-value: {p_value:.4f}\n")
    f.write(f"    유의수준: {'유의함 (p<0.05)' if p_value < 0.05 else '유의하지 않음 (p>=0.05)'}\n\n")

    f.write(f"  - 방범 CCTV vs CCTV효과범죄 상관계수: {r_corr2:.4f}\n")
    f.write(f"    p-value: {p_value2:.4f}\n")
    f.write(f"    유의수준: {'유의함 (p<0.05)' if p_value2 < 0.05 else '유의하지 않음 (p>=0.05)'}\n\n")

    f.write("CCTV 상위 5개 자치구:\n")
    for i, row in merged.nlargest(5, 'CCTV_총계').iterrows():
        f.write(f"  {row['자치구']}: {row['CCTV_총계']:.0f}대 "
                f"(범죄: {row['총범죄_발생']:.0f}건)\n")

    f.write("\n범죄 상위 5개 자치구:\n")
    for i, row in merged.nlargest(5, '총범죄_발생').iterrows():
        f.write(f"  {row['자치구']}: {row['총범죄_발생']:.0f}건 "
                f"(CCTV: {row['CCTV_총계']:.0f}대)\n")

print("  - analysis_summary.txt 저장")

print("\n" + "="*80)
print("분석 완료!")
print("="*80)
print("\n생성된 파일:")
print("  - results/figures/scatter_cctv_crime_real.png")
print("  - results/figures/correlation_heatmap_real.png")
print("  - results/figures/cctv_by_district_real.png")
print("  - results/reports/analysis_summary.txt")
print("  - data/processed/integrated_data_with_analysis.csv")
print("\n다음 단계:")
print("  python dashboard.py  # 대시보드 실행")

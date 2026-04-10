import pandas as pd
import numpy as np
import sys
import io

# UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 데이터 로드 - 컬럼명이 한글인 경우 대비
df = pd.read_csv('data/processed/integrated_data_with_analysis.csv', encoding='utf-8-sig')

# 컬럼명 매핑 (한글 -> 영어)
column_mapping = {
    '자치구': 'District',
    'CCTV_총계': 'CCTV_count',
    '범죄예방_총계': 'Crime_prevention',
    '총범죄_발생': 'Crime_total',
    '총인구': 'Population',
    '방범용': 'Security_CCTV'
}

# 컬럼명 변경
for ko, en in column_mapping.items():
    if ko in df.columns and en not in df.columns:
        df.rename(columns={ko: en}, inplace=True)

print('='*80)
print('📊 CCTV 프로젝트 - 면접 대비 핵심 통계 지표')
print('='*80)

# 1. 기본 통계
print('\n【1】 기본 통계량')
print('-'*80)
print(f'총 데이터: {len(df)}개 구')
print(f'분석 기간: 2024년')
print(f'분석 지역: 서울시 25개 자치구')

# 2. CCTV 통계
print('\n【2】 CCTV 통계')
print('-'*80)
cctv_stats = df['CCTV_count'].describe()
print(f'평균: {cctv_stats["mean"]:.1f}대')
print(f'표준편차: {cctv_stats["std"]:.1f}대')
print(f'최소: {cctv_stats["min"]:.0f}대 ({df.loc[df["CCTV_count"].idxmin(), "District"]})')
print(f'최대: {cctv_stats["max"]:.0f}대 ({df.loc[df["CCTV_count"].idxmax(), "District"]})')
print(f'중앙값: {cctv_stats["50%"]:.1f}대')

# CV (변동계수)
cctv_cv = (cctv_stats['std'] / cctv_stats['mean']) * 100
print(f'\n💡 CV (변동계수): {cctv_cv:.2f}%')
print(f'   해석: 구별 CCTV 분포가 {"매우 불균등" if cctv_cv > 30 else "불균등"}함')

# 3. 범죄 통계
print('\n【3】 범죄 발생 통계')
print('-'*80)
crime_stats = df['Crime_total'].describe()
print(f'평균: {crime_stats["mean"]:.1f}건')
print(f'표준편차: {crime_stats["std"]:.1f}건')
print(f'최소: {crime_stats["min"]:.0f}건 ({df.loc[df["Crime_total"].idxmin(), "District"]})')
print(f'최대: {crime_stats["max"]:.0f}건 ({df.loc[df["Crime_total"].idxmax(), "District"]})')

crime_cv = (crime_stats['std'] / crime_stats['mean']) * 100
print(f'\n💡 CV (변동계수): {crime_cv:.2f}%')

# 4. Z-Score 분석
print('\n【4】 Z-Score 분석 (이상치 탐지)')
print('-'*80)
print('📌 Z-Score 개념:')
print('   • 평균으로부터 표준편차 몇 배 떨어져 있는지 측정')
print('   • |Z| > 2: 상위/하위 5% (주목할 만한 값)')
print('   • |Z| > 3: 상위/하위 0.3% (극단적 이상치)\n')

# CCTV Z-Score 계산
df['CCTV_zscore'] = (df['CCTV_count'] - df['CCTV_count'].mean()) / df['CCTV_count'].std()
outliers_cctv = df[abs(df['CCTV_zscore']) > 2].sort_values('CCTV_zscore', ascending=False)

print('🔍 CCTV 이상치 (|Z-Score| > 2):')
if len(outliers_cctv) == 0:
    print('   없음')
else:
    for idx, row in outliers_cctv.iterrows():
        status = '⬆️ 매우 많음' if row['CCTV_zscore'] > 0 else '⬇️ 매우 적음'
        print(f'   {row["District"]:8s}: {row["CCTV_count"]:6.0f}대 (Z={row["CCTV_zscore"]:+.2f}) {status}')

# 범죄 Z-Score 계산
df['Crime_zscore'] = (df['Crime_total'] - df['Crime_total'].mean()) / df['Crime_total'].std()
outliers_crime = df[abs(df['Crime_zscore']) > 2].sort_values('Crime_zscore', ascending=False)

print('\n🔍 범죄 이상치 (|Z-Score| > 2):')
if len(outliers_crime) == 0:
    print('   없음')
else:
    for idx, row in outliers_crime.iterrows():
        status = '⬆️ 매우 많음' if row['Crime_zscore'] > 0 else '⬇️ 매우 적음'
        print(f'   {row["District"]:8s}: {row["Crime_total"]:6.0f}건 (Z={row["Crime_zscore"]:+.2f}) {status}')

# 5. 상관관계
print('\n【5】 상관관계 분석')
print('-'*80)
corr = df['CCTV_count'].corr(df['Crime_total'])
print(f'CCTV vs 범죄 상관계수: {corr:.4f}')

if abs(corr) < 0.3:
    strength = '약한 상관관계'
elif abs(corr) < 0.7:
    strength = '중간 상관관계'
else:
    strength = '강한 상관관계'

print(f'상관 강도: {strength}')

if corr > 0:
    print('⚠️  양의 상관관계 → CCTV 많은 곳이 범죄도 많음')
    print('   → 원인 가설: 범죄 많은 곳에 CCTV를 더 설치했을 가능성')
else:
    print('✅ 음의 상관관계 → CCTV 많은 곳이 범죄 적음')
    print('   → CCTV의 범죄 예방 효과 가능성')

# 6. 효율성 지표
print('\n【6】 효율성 지표 (인구 대비)')
print('-'*80)
if 'CCTV_per_1000' not in df.columns:
    df['CCTV_per_1000'] = (df['CCTV_count'] / df['Population']) * 1000
if 'Crime_per_1000' not in df.columns:
    df['Crime_per_1000'] = (df['Crime_total'] / df['Population']) * 1000

top5_cctv = df.nlargest(5, 'CCTV_per_1000')[['District', 'CCTV_per_1000', 'Population']]
print('인구 1,000명당 CCTV (상위 5개구):')
for idx, row in top5_cctv.iterrows():
    print(f'   {row["District"]:8s}: {row["CCTV_per_1000"]:5.2f}대/천명 (인구: {row["Population"]:,}명)')

# 7. 핵심 인사이트
print('\n【7】 핵심 인사이트 (면접 답변용)')
print('-'*80)
print(f'✅ CCTV 배치 불균등성: CV = {cctv_cv:.1f}%')
print('✅ Z-Score로 이상치 구 파악 → 정책 개선점 도출')
print(f'✅ 상관분석 결과: {corr:.3f} ({strength})')
print('✅ 인구 대비 정규화로 공정한 효율성 비교')
print('✅ 데이터 기반 의사결정 지원')

# 8. 면접 예상 질문
print('\n' + '='*80)
print('💬 면접 예상 질문 & 모범 답변')
print('='*80)

print('\n[Q1] CV(변동계수)가 무엇인가요?')
print('─────────────────────────────────────────────────')
print('📝 표준편차를 평균으로 나눈 값으로, 서로 다른 단위나 스케일을 가진')
print('   데이터의 변동성을 비교할 때 사용합니다.')
print(f'   예시: 본 프로젝트에서 CCTV의 CV는 {cctv_cv:.1f}%로,')
print('   구별로 CCTV 배치가 상당히 불균등하다는 것을 알 수 있습니다.')

print('\n[Q2] Z-Score는 왜 사용했나요?')
print('─────────────────────────────────────────────────')
print('📝 이상치를 객관적으로 탐지하기 위해 사용했습니다.')
print('   Z-Score는 각 값이 평균에서 표준편차 기준으로 얼마나 떨어져')
print('   있는지 측정합니다. |Z| > 2인 값은 상위/하위 5%에 해당하며,')
print('   정책적 관심이 필요한 구를 식별할 수 있습니다.')

print('\n[Q3] 상관계수는 어떻게 해석하나요?')
print('─────────────────────────────────────────────────')
print('📝 -1부터 1 사이의 값으로, 두 변수 간의 선형 관계를 나타냅니다.')
print('   • 0에 가까우면: 거의 무관')
print('   • ±0.3~0.7: 중간 정도 상관')
print('   • ±0.7~1: 강한 상관')
print('   • 양수: 함께 증가, 음수: 반대로 움직임')
print(f'   본 프로젝트: {corr:.4f} → {strength}')

print('\n[Q4] 왜 인구 대비 비율을 계산했나요?')
print('─────────────────────────────────────────────────')
print('📝 절대적인 수치만으로는 공정한 비교가 어렵기 때문입니다.')
print('   인구가 많은 구는 CCTV 수도 많은 것이 당연하므로,')
print('   인구 1,000명당 CCTV 수로 정규화하여 각 구의 실제')
print('   CCTV 커버리지 효율성을 비교했습니다.')

print('\n[Q5] 이 프로젝트에서 가장 중요한 발견은?')
print('─────────────────────────────────────────────────')
print(f'📝 CCTV와 범죄의 상관계수가 {corr:.3f}로 나타났습니다.')
if corr > 0:
    print('   이는 CCTV가 많은 곳이 범죄도 많다는 의미로,')
    print('   범죄율이 높은 곳에 CCTV를 집중 배치했음을 시사합니다.')
    print('   따라서 CCTV는 예방보다는 사후 대응 목적이 강한 것으로 보입니다.')
else:
    print('   이는 CCTV가 범죄 예방에 효과적임을 시사합니다.')

print('\n' + '='*80)
print('🎯 핵심 요약')
print('='*80)
print(f'• 분석 대상: 서울시 {len(df)}개 자치구')
print(f'• CCTV 평균: {cctv_stats["mean"]:.0f}대 (CV: {cctv_cv:.1f}%)')
print(f'• 범죄 평균: {crime_stats["mean"]:.0f}건 (CV: {crime_cv:.1f}%)')
print(f'• 상관계수: {corr:.4f} ({strength})')
print(f'• 주요 기법: 기술통계, Z-Score, 상관분석, 정규화')
print('='*80)

"""
자치구명 불일치 수정
"""

import pandas as pd

print("자치구명 정리 중...")

# 1. CCTV 데이터 수정
cctv = pd.read_csv('data/raw/cctv_real_2025.csv', encoding='utf-8-sig')

# 불필요한 행 제거
cctv = cctv[~cctv['자치구'].str.contains('※', na=False)]

# "구" 추가
cctv['자치구'] = cctv['자치구'].replace({
    '동대문': '동대문구',
    '서대문': '서대문구',
    '영등포': '영등포구'
})

print(f"CCTV: {len(cctv)}개 자치구")
print(cctv['자치구'].tolist())

# 2. 범죄 데이터는 이미 깨끗함
crime = pd.read_csv('data/raw/crime_real_2024.csv', encoding='utf-8-sig')
print(f"\n범죄: {len(crime)}개 자치구")
print(crime['자치구'].tolist())

# 3. 인구 데이터는 이미 깨끗함
pop = pd.read_csv('data/raw/population_real_2025.csv', encoding='utf-8-sig')
print(f"\n인구: {len(pop)}개 자치구")
print(pop['자치구'].tolist())

# 4. 데이터 통합 (inner join - 모든 데이터가 있는 자치구만)
merged = cctv.merge(crime, on='자치구', how='inner')
merged = merged.merge(pop, on='자치구', how='inner')

print(f"\n==> 최종 통합: {len(merged)}개 자치구")
print(merged['자치구'].tolist())

# 5. 저장
cctv.to_csv('data/raw/cctv_real_2025.csv', index=False, encoding='utf-8-sig')
merged.to_csv('data/raw/merged_real_data.csv', index=False, encoding='utf-8-sig')

print("\n저장 완료!")
print(f"최종 데이터: {len(merged)}개 자치구, {len(merged.columns)}개 컬럼")
print("\n데이터 미리보기:")
print(merged[['자치구', 'CCTV_총계', '총범죄_발생', '총인구']].head(10))

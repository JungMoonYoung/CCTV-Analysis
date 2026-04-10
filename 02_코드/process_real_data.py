"""
cctvdataset 폴더의 실제 데이터를 정리하여 분석 가능한 형태로 변환
"""

import pandas as pd
import numpy as np
import sys
import io

# Windows 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("실제 데이터 처리 및 정리")
print("="*80)

# 1. CCTV 데이터 처리
print("\n[1/3] CCTV 데이터 처리 중...")
try:
    cctv_df = pd.read_excel('cctvdataset/서울시 자치구 (목적별) CCTV 설치현황(\'25.6.30 기준).xlsx',
                            header=None)

    # 헤더 스킵하고 데이터 추출
    cctv_data = []
    for i in range(5, len(cctv_df)):  # 5번째 줄부터 데이터 시작
        row = cctv_df.iloc[i]
        district = row[1]
        if pd.isna(district) or district == '자치구':
            continue

        cctv_data.append({
            '자치구': district,
            'CCTV_총계': row[2],
            '범죄예방_총계': row[3],
            '방범용': row[4],
            '어린이보호구역': row[5],
            '공원놀이터': row[6],
            '쓰레기무단투기': row[7] if str(row[7]) != '-' else 0,
            '시설안전_화재예방': row[8],
            '교통단속': row[9],
            '교통정보수집_분석': row[10],
            '기타': row[11]
        })

    cctv_clean = pd.DataFrame(cctv_data)
    print(f"[OK] CCTV 데이터: {len(cctv_clean)}개 자치구")
    print(f"     컬럼: {list(cctv_clean.columns)}")

except Exception as e:
    print(f"[FAIL] CCTV 데이터 처리 실패: {e}")
    cctv_clean = None

# 2. 5대 범죄 데이터 처리
print("\n[2/3] 5대 범죄 발생현황 데이터 처리 중...")
try:
    crime_df = pd.read_csv('cctvdataset/5대+범죄+발생현황_20251210202928.csv', encoding='utf-8-sig')

    # 헤더 스킵하고 데이터 추출 (5번째 줄부터)
    crime_data = []
    for i in range(5, len(crime_df)):
        row = crime_df.iloc[i]
        district = row[1]
        if pd.isna(district) or district == '소계':
            continue

        crime_data.append({
            '자치구': district,
            '총범죄_발생': row[2],
            '총범죄_검거': row[3],
            '살인_발생': row[4],
            '살인_검거': row[5],
            '강도_발생': row[6],
            '강도_검거': row[7],
            '강간강제추행_발생': row[8],
            '강간강제추행_검거': row[9],
            '절도_발생': row[10],
            '절도_검거': row[11],
            '폭력_발생': row[12],
            '폭력_검거': row[13]
        })

    crime_clean = pd.DataFrame(crime_data)

    # '-' 값을 0으로 변환
    for col in crime_clean.columns:
        if col != '자치구':
            crime_clean[col] = pd.to_numeric(crime_clean[col].replace('-', 0), errors='coerce').fillna(0)

    print(f"[OK] 범죄 데이터: {len(crime_clean)}개 자치구")
    print(f"     컬럼: {list(crime_clean.columns)}")

except Exception as e:
    print(f"[FAIL] 범죄 데이터 처리 실패: {e}")
    crime_clean = None

# 3. 인구 데이터 처리
print("\n[3/3] 등록인구 데이터 처리 중...")
try:
    pop_df = pd.read_csv('cctvdataset/등록인구_20251210203438.csv', encoding='utf-8-sig')

    # 헤더 스킵하고 데이터 추출 (4번째 줄부터)
    pop_data = []
    for i in range(4, len(pop_df)):
        row = pop_df.iloc[i]
        district = row[1]
        if pd.isna(district) or district == '소계':
            continue

        # 자치구명에서 '구' 추출
        if '구' in district:
            district_name = district
        else:
            continue

        pop_data.append({
            '자치구': district_name,
            '세대수': row[2],
            '총인구': row[3],
            '남자': row[4],
            '여자': row[5],
            '한국인_총계': row[6],
            '등록외국인_총계': row[9],
            '세대당인구': row[12],
            '고령자수': row[13]
        })

    pop_clean = pd.DataFrame(pop_data)
    print(f"[OK] 인구 데이터: {len(pop_clean)}개 자치구")
    print(f"     컬럼: {list(pop_clean.columns)}")

except Exception as e:
    print(f"[FAIL] 인구 데이터 처리 실패: {e}")
    pop_clean = None

# 4. 데이터 통합
print("\n" + "="*80)
print("데이터 통합 중...")
print("="*80)

if cctv_clean is not None and crime_clean is not None and pop_clean is not None:
    # 자치구 기준으로 병합
    merged = cctv_clean.copy()
    merged = merged.merge(crime_clean, on='자치구', how='outer')
    merged = merged.merge(pop_clean, on='자치구', how='outer')

    print(f"\n통합 데이터: {len(merged)}개 자치구")
    print(f"컬럼 수: {len(merged.columns)}개")
    print(f"\n자치구 목록:")
    print(merged['자치구'].tolist())

    # 5. 저장
    print("\n" + "="*80)
    print("데이터 저장 중...")
    print("="*80)

    # 개별 저장
    cctv_clean.to_csv('data/raw/cctv_real_2025.csv', index=False, encoding='utf-8-sig')
    crime_clean.to_csv('data/raw/crime_real_2024.csv', index=False, encoding='utf-8-sig')
    pop_clean.to_csv('data/raw/population_real_2025.csv', index=False, encoding='utf-8-sig')

    # 통합 데이터 저장
    merged.to_csv('data/raw/merged_real_data.csv', index=False, encoding='utf-8-sig')

    print("\n[OK] 저장 완료:")
    print("  - data/raw/cctv_real_2025.csv")
    print("  - data/raw/crime_real_2024.csv")
    print("  - data/raw/population_real_2025.csv")
    print("  - data/raw/merged_real_data.csv")

    print("\n" + "="*80)
    print("데이터 요약")
    print("="*80)
    print(f"\nCCTV 데이터:")
    print(cctv_clean.head())
    print(f"\n범죄 데이터:")
    print(crime_clean.head())
    print(f"\n인구 데이터:")
    print(pop_clean.head())

    print("\n" + "="*80)
    print("처리 완료! 이제 분석을 시작할 수 있습니다.")
    print("다음 명령어를 실행하세요:")
    print("  python dashboard.py")
    print("  또는")
    print("  python run_all_analysis.py")
    print("="*80)

else:
    print("\n[FAIL] 일부 데이터 처리 실패")
    if cctv_clean is None:
        print("  - CCTV 데이터 실패")
    if crime_clean is None:
        print("  - 범죄 데이터 실패")
    if pop_clean is None:
        print("  - 인구 데이터 실패")

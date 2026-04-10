"""
API 키로 접근 가능한 모든 서비스를 찾아보는 스크립트
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SEOUL_API_KEY')
BASE_URL = "http://openapi.seoul.go.kr:8088"

# 숫자 패턴으로 시도 (LOCALDATA_XXXXXX)
def test_localdata_range(start, end, category_prefix):
    """LOCALDATA 패턴 범위 테스트"""
    successful = []

    for i in range(start, end + 1):
        service_name = f"LOCALDATA_{category_prefix}{i:04d}"
        url = f"{BASE_URL}/{API_KEY}/json/{service_name}/1/1"

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if 'RESULT' in data:
                code = data['RESULT'].get('CODE')
                if code == 'INFO-000' or service_name in str(data):
                    print(f"[OK] {service_name}")
                    successful.append(service_name)
            elif service_name in data:
                print(f"[OK] {service_name}")
                successful.append(service_name)

        except:
            pass

    return successful

print("="*80)
print("서울 열린데이터광장 API - 사용 가능한 서비스 탐색")
print("="*80)
print(f"\nAPI 키: {API_KEY[:10]}...{API_KEY[-5:]}")

print("\n[1/3] 범죄 관련 서비스 탐색 중 (020001-020999)...")
crime_services = test_localdata_range(1, 999, "0205")

print("\n[2/3] 인구 관련 서비스 탐색 중 (010001-010999)...")
population_services = test_localdata_range(1, 999, "0101")

print("\n[3/3] 기타 서비스 탐색 중 (010001-019999)...")
other_services = test_localdata_range(1, 200, "01")

print("\n" + "="*80)
print("탐색 완료")
print("="*80)

all_services = crime_services + population_services + other_services
if all_services:
    print(f"\n발견된 서비스: {len(all_services)}개")
    for service in all_services:
        print(f"  - {service}")
else:
    print("\n추가 서비스를 찾지 못했습니다.")

print("\n권장 사항:")
print("1. API 신청이 승인되었는지 서울 열린데이터광장에서 확인")
print("2. 신청한 데이터가 'Open API(A)' 타입인지 '통계(S)' 타입인지 확인")
print("3. 통계(S) 타입이면 파일 다운로드 방식으로 데이터 수집 필요")

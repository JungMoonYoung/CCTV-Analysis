"""
서울 열린데이터광장 API 연결 테스트 스크립트
실제 서비스명을 찾고 API가 정상 작동하는지 확인
"""

import os
import sys
import requests
from dotenv import load_dotenv
import json

# Windows 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# .env 파일에서 API 키 로드
load_dotenv()

# API 기본 설정
BASE_URL = "http://openapi.seoul.go.kr:8088"
API_KEY = os.getenv('SEOUL_API_KEY')

# 테스트할 서비스명 리스트 (일반적인 패턴들)
TEST_SERVICE_NAMES = [
    # 범죄 관련 - 다양한 패턴 시도
    "LOCALDATA_020501",
    "LOCALDATA_020502",
    "tbCrimeStatus",
    "CrimeStatistics",
    "FiveMajorCrimes",
    "FiveCrimeStatus",
    "SeoulCrimeStatus",
    "CrimeOccurrence",
    "CrimeByLocation",

    # 인구 관련
    "LOCALDATA_010101",
    "LOCALDATA_010102",
    "PopulationStatus",
    "ResidentRegistration",
    "PopulationMigration",
    "PopulationByAge",

    # 통계 서비스 (일부 API는 통계 서비스로 제공)
    "StatCrimeOccurrence",
    "Stat5MajorCrimes",
]

def test_api_call(service_name, start_idx=1, end_idx=5):
    """
    API 호출 테스트

    Args:
        service_name: 테스트할 서비스명
        start_idx: 시작 인덱스
        end_idx: 종료 인덱스

    Returns:
        (success: bool, response_data: dict)
    """
    url = f"{BASE_URL}/{API_KEY}/json/{service_name}/{start_idx}/{end_idx}"

    print(f"\n테스트 중: {service_name}")
    print(f"URL: {url}")

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # 응답 확인
        if response.status_code == 200:
            # 에러 코드 확인
            if 'RESULT' in data:
                result = data['RESULT']
                code = result.get('CODE')
                message = result.get('MESSAGE', '')

                if code == 'INFO-000':
                    print(f"[OK] 성공! - {message}")
                    print(f"  응답 데이터 키: {list(data.keys())}")
                    return True, data
                else:
                    print(f"[FAIL] 실패 - 코드: {code}, 메시지: {message}")
                    return False, data
            else:
                print(f"[OK] 성공! (응답 구조 다름)")
                print(f"  응답 데이터 키: {list(data.keys())}")
                return True, data
        else:
            print(f"[FAIL] HTTP 에러: {response.status_code}")
            return False, data

    except requests.exceptions.RequestException as e:
        print(f"[FAIL] 요청 실패: {e}")
        return False, None
    except json.JSONDecodeError as e:
        print(f"[FAIL] JSON 파싱 실패: {e}")
        print(f"  응답 내용: {response.text[:200]}")
        return False, None
    except Exception as e:
        print(f"[FAIL] 예상치 못한 오류: {e}")
        return False, None


def main():
    print("="*80)
    print("서울 열린데이터광장 API 연결 테스트")
    print("="*80)

    if not API_KEY:
        print("\n오류: API 키가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        return

    print(f"\nAPI 키: {API_KEY[:10]}...{API_KEY[-5:]}")
    print(f"테스트할 서비스명 개수: {len(TEST_SERVICE_NAMES)}")

    successful_services = []

    # 각 서비스명 테스트
    for service_name in TEST_SERVICE_NAMES:
        success, data = test_api_call(service_name)
        if success:
            successful_services.append((service_name, data))

    # 결과 요약
    print("\n" + "="*80)
    print("테스트 결과 요약")
    print("="*80)

    if successful_services:
        print(f"\n[OK] 성공한 서비스: {len(successful_services)}개")
        for service_name, data in successful_services:
            print(f"\n  [{service_name}]")
            print(f"  - 데이터 키: {list(data.keys())}")

            # 데이터 샘플 출력
            for key in data.keys():
                if key != 'RESULT':
                    if isinstance(data[key], dict) and 'row' in data[key]:
                        rows = data[key]['row']
                        print(f"  - {key}: {len(rows)}개 레코드")
                        if rows:
                            print(f"  - 첫 번째 레코드 필드: {list(rows[0].keys())}")
    else:
        print("\n[FAIL] 성공한 서비스가 없습니다.")
        print("\n다음 단계:")
        print("1. 서울 열린데이터광장(data.seoul.go.kr)에 로그인")
        print("2. 마이페이지 > API 활용신청 현황 확인")
        print("3. 각 API의 정확한 '서비스명' 확인")
        print("4. fetch_seoul_data.py의 service_name을 실제 값으로 수정")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()

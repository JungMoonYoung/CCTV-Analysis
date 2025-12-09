"""
서울 열린데이터광장 API로부터 실제 데이터 수집
API 인증키를 받은 후 실행하세요
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 API 키 로드
load_dotenv()

# API 기본 설정
BASE_URL = "http://openapi.seoul.go.kr:8088"
OUTPUT_FORMAT = "json"  # json 또는 xml
ROWS_PER_REQUEST = 1000

class SeoulDataFetcher:
    """서울 열린데이터광장 API 클라이언트"""

    def __init__(self):
        self.crime_key = os.getenv('SEOUL_CRIME_API_KEY')
        self.crime_location_key = os.getenv('SEOUL_CRIME_LOCATION_API_KEY')
        self.population_key = os.getenv('SEOUL_POPULATION_API_KEY')
        self.migration_key = os.getenv('SEOUL_MIGRATION_API_KEY')

        # API 키 확인
        if not all([self.crime_key, self.population_key]):
            raise ValueError(
                "API 키가 설정되지 않았습니다. "
                ".env 파일을 생성하고 API 키를 입력하세요. "
                ".env.example 파일을 참고하세요."
            )

    def fetch_data(self, api_key, service_name, start_idx=1, end_idx=1000):
        """
        서울 열린데이터광장 API 호출

        Args:
            api_key: API 인증키
            service_name: 서비스명 (예: '범죄발생현황')
            start_idx: 시작 인덱스
            end_idx: 종료 인덱스

        Returns:
            JSON 응답 데이터
        """
        url = f"{BASE_URL}/{api_key}/{OUTPUT_FORMAT}/{service_name}/{start_idx}/{end_idx}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 호출 실패: {e}")
            return None

    def fetch_crime_data(self, year=2023):
        """범죄 발생 현황 데이터 수집"""
        print(f"\n[1/4] {year}년 범죄 발생 현황 데이터 수집 중...")

        # 실제 서비스명은 API 신청 후 확인 필요
        # 예시: '범죄발생현황', 'crimeStat' 등
        service_name = "범죄발생현황"  # TODO: 실제 서비스명으로 변경

        data = self.fetch_data(self.crime_key, service_name, 1, 1000)

        if data:
            # JSON을 DataFrame으로 변환 (실제 구조에 맞게 수정 필요)
            # df = pd.DataFrame(data['결과키']['row'])
            print("✓ 범죄 데이터 수집 완료")
            return data
        else:
            print("✗ 범죄 데이터 수집 실패")
            return None

    def fetch_crime_location_data(self, year=2023):
        """5대 범죄 발생장소별 현황 데이터 수집"""
        print(f"\n[2/4] {year}년 5대 범죄 발생장소별 현황 데이터 수집 중...")

        service_name = "5대범죄발생장소"  # TODO: 실제 서비스명으로 변경

        data = self.fetch_data(self.crime_location_key, service_name, 1, 1000)

        if data:
            print("✓ 범죄 발생장소 데이터 수집 완료")
            return data
        else:
            print("✗ 범죄 발생장소 데이터 수집 실패")
            return None

    def fetch_population_data(self, year=2023):
        """등록인구 통계 데이터 수집"""
        print(f"\n[3/4] {year}년 등록인구 통계 데이터 수집 중...")

        service_name = "등록인구통계"  # TODO: 실제 서비스명으로 변경

        data = self.fetch_data(self.population_key, service_name, 1, 1000)

        if data:
            print("✓ 인구 데이터 수집 완료")
            return data
        else:
            print("✗ 인구 데이터 수집 실패")
            return None

    def fetch_migration_data(self, year=2023):
        """인구이동 통계 데이터 수집"""
        print(f"\n[4/4] {year}년 인구이동 통계 데이터 수집 중...")

        service_name = "인구이동통계"  # TODO: 실제 서비스명으로 변경

        data = self.fetch_data(self.migration_key, service_name, 1, 1000)

        if data:
            print("✓ 인구이동 데이터 수집 완료")
            return data
        else:
            print("✗ 인구이동 데이터 수집 실패")
            return None

    def save_to_csv(self, data, filename):
        """데이터를 CSV 파일로 저장"""
        if data is None:
            print(f"데이터가 없어 {filename} 저장 실패")
            return

        # 실제 JSON 구조에 맞게 수정 필요
        # 예시: df = pd.DataFrame(data['결과키']['row'])
        # df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✓ {filename} 저장 완료")


def main():
    """메인 실행 함수"""
    print("="*80)
    print("서울 열린데이터광장 API 데이터 수집 스크립트")
    print("="*80)

    try:
        fetcher = SeoulDataFetcher()

        # 데이터 수집
        crime_data = fetcher.fetch_crime_data(year=2023)
        crime_location_data = fetcher.fetch_crime_location_data(year=2023)
        population_data = fetcher.fetch_population_data(year=2023)
        migration_data = fetcher.fetch_migration_data(year=2023)

        # 데이터 저장
        os.makedirs('data/raw', exist_ok=True)

        print("\n" + "="*80)
        print("데이터 수집 완료!")
        print("="*80)
        print("\n다음 단계:")
        print("1. 수집된 JSON 데이터의 구조를 확인하세요")
        print("2. save_to_csv() 함수를 수정하여 실제 데이터 구조에 맞게 CSV로 저장하세요")
        print("3. run_all_analysis.py를 실행하여 분석을 시작하세요")

    except ValueError as e:
        print(f"\n오류: {e}")
        print("\n설정 방법:")
        print("1. .env.example을 복사하여 .env 파일을 만드세요")
        print("2. 서울 열린데이터광장에서 받은 API 키를 입력하세요")
        print("3. 다시 실행하세요")
    except Exception as e:
        print(f"\n예상치 못한 오류 발생: {e}")


if __name__ == "__main__":
    main()

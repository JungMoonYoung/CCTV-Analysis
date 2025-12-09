"""
프로젝트 전역 상수 정의

이 파일은 프로젝트 전반에서 사용되는 상수들을 정의합니다.
- 서울시 자치구 리스트
- 샘플 데이터 생성 범위
- 시각화 설정
"""

# 서울시 25개 자치구 (가나다 순)
SEOUL_DISTRICTS = [
    '강남구', '강동구', '강북구', '강서구', '관악구',
    '광진구', '구로구', '금천구', '노원구', '도봉구',
    '동대문구', '동작구', '마포구', '서대문구', '서초구',
    '성동구', '성북구', '송파구', '양천구', '영등포구',
    '용산구', '은평구', '종로구', '중구', '중랑구'
]

# CCTV 유형별 샘플 데이터 생성 범위 (최소, 최대)
CCTV_RANGE = {
    '방범용': (500, 3000),
    '교통단속용': (100, 500),
    '어린이안전용': (50, 300),
    '기타': (50, 200)
}

# 범죄 유형별 샘플 데이터 생성 범위
CRIME_RANGE = {
    '절도': (100, 800),
    '강도': (5, 50),
    '차량범죄': (50, 300),
    '공공장소폭력': (80, 400),
    '성범죄': (30, 150)
}

# CCTV 효과 범죄 유형 (분석 대상)
CCTV_EFFECT_CRIMES = ['절도', '강도', '차량범죄']

# 인구 샘플 데이터 생성 범위
POPULATION_CONFIG = {
    'base_population': 150000,
    'population_range': (-30000, 50000),
    'min_population': 50000,  # 최소 인구 보장
    'area_range': (10, 40)  # km²
}

# 시각화 색상 팔레트
COLOR_PALETTE = {
    'cctv': '#1f77b4',  # 파란색
    'crime': '#ff7f0e',  # 주황색
    'population': '#2ca02c',  # 녹색
    'danger': '#d62728',  # 빨간색
    'safe': '#9467bd'  # 보라색
}

# 시각화 스타일 설정
PLOT_STYLE = {
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
}

# 랜덤 시드 (재현성 확보)
RANDOM_SEED = 42

# 이상치 탐지 설정
IQR_THRESHOLD = 1.5  # IQR 배수 (1.5 표준)

# 데이터 파일 경로
DATA_PATHS = {
    'raw': '../data/raw',
    'processed': '../data/processed',
    'geo': '../data/geo',
    'figures': '../results/figures',
    'reports': '../results/reports',
    'logs': '../logs'
}

# 분석 연도
ANALYSIS_YEAR = 2023

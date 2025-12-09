"""
프로젝트 공통 헬퍼 함수

이 파일은 프로젝트 전반에서 재사용되는 유틸리티 함수들을 정의합니다.
"""

import os
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .constants import PLOT_STYLE, COLOR_PALETTE, SEOUL_DISTRICTS, CCTV_RANGE, CRIME_RANGE, POPULATION_CONFIG, RANDOM_SEED


def set_korean_font():
    """
    OS별 한글 폰트 설정

    Windows: Malgun Gothic
    macOS: AppleGothic
    Linux: NanumGothic

    Returns:
        str: 설정된 폰트 이름
    """
    system = platform.system()

    if system == 'Windows':
        font_name = 'Malgun Gothic'
    elif system == 'Darwin':  # macOS
        font_name = 'AppleGothic'
    else:  # Linux
        font_name = 'NanumGothic'

    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False

    print(f"[OK] 한글 폰트 설정 완료: {font_name} ({system})")
    return font_name


def set_plot_style(style_dict=None):
    """
    matplotlib 시각화 스타일 설정

    Args:
        style_dict (dict, optional): 커스텀 스타일 딕셔너리
    """
    if style_dict is None:
        style_dict = PLOT_STYLE

    plt.rcParams.update(style_dict)
    print("[OK] 시각화 스타일 설정 완료")


def print_data_info(df, data_name):
    """
    데이터프레임 기본 정보 출력

    Args:
        df (pd.DataFrame): 분석할 데이터프레임
        data_name (str): 데이터 이름 (출력용)

    Returns:
        pd.DataFrame: df.head() 결과
    """
    print(f"\n{'='*60}")
    print(f"[{data_name} 데이터 기본 정보]")
    print(f"{'='*60}")
    print(f"행 개수: {len(df):,}")
    print(f"열 개수: {len(df.columns)}")
    print(f"\n데이터 타입:")
    print(df.dtypes)
    print(f"\n결측치:")
    null_counts = df.isnull().sum()
    if null_counts.sum() == 0:
        print("   결측치 없음 [OK]")
    else:
        print(null_counts[null_counts > 0])
    print(f"\n처음 5개 행:")
    print(df.head())
    print(f"{'='*60}\n")

    return df.head()


def save_csv_safely(df, file_path, **kwargs):
    """
    디렉토리 생성 후 CSV 파일 안전하게 저장

    Args:
        df (pd.DataFrame): 저장할 데이터프레임
        file_path (str): 저장 경로
        **kwargs: pd.DataFrame.to_csv()에 전달할 추가 인자
    """
    # 디렉토리 생성 (없으면)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # CSV 저장
    df.to_csv(file_path, **kwargs)
    print(f"[OK] 파일 저장 완료: {file_path}")


def validate_data(df, expected_rows=25, required_columns=None):
    """
    데이터 검증 (행 개수, 필수 컬럼, 결측치)

    Args:
        df (pd.DataFrame): 검증할 데이터프레임
        expected_rows (int): 예상 행 개수 (기본: 25개 자치구)
        required_columns (list, optional): 필수 컬럼 리스트

    Raises:
        AssertionError: 검증 실패 시

    Returns:
        bool: 검증 성공 여부
    """
    # 행 개수 확인
    assert len(df) == expected_rows, \
        f"[ERROR] 행 개수 불일치: {len(df)} != {expected_rows}"

    # 필수 컬럼 확인
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        assert not missing_cols, \
            f"[ERROR] 필수 컬럼 누락: {missing_cols}"

    # 결측치 확인
    null_count = df.isnull().sum().sum()
    assert null_count == 0, \
        f"[ERROR] 결측치 발견: {null_count}개"

    print("[OK] 데이터 검증 완료")
    return True


def plot_distribution(df, column, title, color='blue', xlabel=None,
                       save_path=None, show_stats=True):
    """
    분포 히스토그램 생성

    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 분석할 컬럼명
        title (str): 그래프 제목
        color (str): 막대 색상 (기본: 'blue')
        xlabel (str, optional): X축 라벨 (기본: column 이름)
        save_path (str, optional): 저장 경로
        show_stats (bool): 통계값 표시 여부 (기본: True)

    Returns:
        tuple: (평균, 중앙값, 표준편차)
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    # 히스토그램
    ax.hist(df[column], bins=15, edgecolor='black', alpha=0.7, color=color)

    # 제목 및 라벨
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel if xlabel else column, fontsize=12)
    ax.set_ylabel('자치구 수', fontsize=12)

    # 평균선 및 통계값
    mean_val = df[column].mean()
    median_val = df[column].median()
    std_val = df[column].std()

    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2,
               label=f'평균: {mean_val:.1f}')

    if show_stats:
        ax.axvline(median_val, color='green', linestyle=':', linewidth=2,
                   label=f'중앙값: {median_val:.1f}')

    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # 저장
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] 그래프 저장: {save_path}")

    plt.show()

    # 통계값 출력
    if show_stats:
        print(f"\n {column} 통계:")
        print(f"   평균: {mean_val:.2f}")
        print(f"   중앙값: {median_val:.2f}")
        print(f"   표준편차: {std_val:.2f}")
        print(f"   최소값: {df[column].min():.2f}")
        print(f"   최대값: {df[column].max():.2f}\n")

    return mean_val, median_val, std_val


def create_summary_stats(df, numeric_cols):
    """
    요약 통계 테이블 생성

    Args:
        df (pd.DataFrame): 데이터프레임
        numeric_cols (list): 숫자형 컬럼 리스트

    Returns:
        pd.DataFrame: 요약 통계 테이블
    """
    summary = df[numeric_cols].describe().T
    summary['중앙값'] = df[numeric_cols].median()
    summary['변동계수(%)'] = (summary['std'] / summary['mean'] * 100).round(2)

    # 컬럼 순서 재정렬
    summary = summary[['count', 'mean', '중앙값', 'std', '변동계수(%)',
                        'min', '25%', '50%', '75%', 'max']]

    # 반올림
    summary = summary.round(2)

    return summary


def plot_multiple_distributions(data_dict, figsize=(18, 5), save_path=None):
    """
    여러 데이터의 분포를 한 번에 시각화

    Args:
        data_dict (dict): {제목: (df, column, color)} 형태의 딕셔너리
        figsize (tuple): Figure 크기
        save_path (str, optional): 저장 경로

    Example:
        data_dict = {
            'CCTV 분포': (cctv_df, '총_CCTV', 'blue'),
            '범죄 분포': (crime_df, '총_범죄', 'red')
        }
    """
    n_plots = len(data_dict)
    fig, axes = plt.subplots(1, n_plots, figsize=figsize)

    if n_plots == 1:
        axes = [axes]

    for ax, (title, (df, column, color)) in zip(axes, data_dict.items()):
        ax.hist(df[column], bins=15, edgecolor='black', alpha=0.7, color=color)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel('자치구 수', fontsize=12)

        mean_val = df[column].mean()
        ax.axvline(mean_val, color='darkred', linestyle='--', linewidth=2,
                   label=f'평균: {mean_val:.0f}')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] 그래프 저장: {save_path}")

    plt.show()


def check_district_consistency(*dataframes, district_col='자치구'):
    """
    여러 데이터프레임의 자치구명 일치 여부 확인

    Args:
        *dataframes: 확인할 데이터프레임들
        district_col (str): 자치구 컬럼명 (기본: '자치구')

    Returns:
        dict: 일치 여부 및 불일치 항목
    """
    district_sets = [set(df[district_col]) for df in dataframes]

    # 모든 데이터프레임의 자치구 일치 여부
    all_equal = all(ds == district_sets[0] for ds in district_sets)

    result = {
        'consistent': all_equal,
        'district_sets': district_sets,
        'common_districts': set.intersection(*district_sets),
        'all_districts': set.union(*district_sets)
    }

    if all_equal:
        print(f"[OK] 모든 데이터프레임의 자치구명 일치 ({len(district_sets[0])}개)")
    else:
        print(f"[WARNING] 자치구명 불일치 발견")
        for i, ds in enumerate(district_sets):
            print(f"   데이터프레임 {i+1}: {sorted(ds)}")

    return result


def format_number(num, unit=''):
    """
    숫자를 읽기 쉬운 형식으로 포맷

    Args:
        num (float): 숫자
        unit (str): 단위 (예: '명', '건', '대')

    Returns:
        str: 포맷된 문자열
    """
    return f"{num:,.0f}{unit}"


def standardize_district_name(name):
    """
    자치구명 표준화

    앞뒤 공백 제거, 특수문자 제거, 접두사 제거 등

    Args:
        name (str): 원본 자치구명

    Returns:
        str: 표준화된 자치구명

    Examples:
        >>> standardize_district_name("서울특별시 강남구")
        '강남구'
        >>> standardize_district_name(" 종로구 ")
        '종로구'
    """
    name = str(name).strip()
    name = name.replace('서울특별시 ', '').replace('서울시 ', '').replace('서울 ', '')
    return name


def detect_outliers_iqr(df, column, threshold=1.5):
    """
    IQR (Interquartile Range) 방법을 이용한 이상치 탐지

    Q1 - threshold*IQR 미만 또는 Q3 + threshold*IQR 초과 값을 이상치로 판정

    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 분석할 컬럼명
        threshold (float): IQR 배수 (기본: 1.5)

    Returns:
        tuple: (이상치 데이터프레임, 하한값, 상한값)

    Examples:
        >>> outliers, lower, upper = detect_outliers_iqr(df, '인구수')
        >>> print(f"정상 범위: {lower:.0f} ~ {upper:.0f}")
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    return outliers, lower_bound, upper_bound


def calculate_ratio_columns(df, numerator_cols, denominator_col, suffix='_비율'):
    """
    비율 컬럼 일괄 계산

    Args:
        df (pd.DataFrame): 데이터프레임
        numerator_cols (list): 분자 컬럼 리스트
        denominator_col (str): 분모 컬럼
        suffix (str): 비율 컬럼 접미사 (기본: '_비율')

    Returns:
        pd.DataFrame: 비율 컬럼이 추가된 데이터프레임

    Examples:
        >>> df = calculate_ratio_columns(
        ...     df,
        ...     ['방범용', '교통단속용'],
        ...     '총_CCTV'
        ... )
    """
    for col in numerator_cols:
        ratio_col_name = f'{col}{suffix}'
        df[ratio_col_name] = (df[col] / df[denominator_col] * 100).round(2)

    return df


def plot_category_analysis(df, categories, category_name, colors=None,
                             save_path=None, figsize=(16, 6)):
    """
    카테고리별 평균 및 비율 시각화 (막대 차트 + 파이 차트)

    Args:
        df (pd.DataFrame): 데이터프레임
        categories (list): 분석할 카테고리 컬럼 리스트
        category_name (str): 카테고리 이름 (그래프 제목용)
        colors (list, optional): 색상 리스트
        save_path (str, optional): 저장 경로
        figsize (tuple): Figure 크기

    Returns:
        None
    """
    if colors is None:
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # 좌측: 카테고리별 평균 막대 차트
    means = [df[cat].mean() for cat in categories]

    axes[0].bar(categories, means, color=colors[:len(categories)],
                edgecolor='black', alpha=0.7)
    axes[0].set_title(f'{category_name} 유형별 평균', fontsize=14, fontweight='bold')
    axes[0].set_xlabel(f'{category_name} 유형', fontsize=12)
    axes[0].set_ylabel('평균 값', fontsize=12)
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].tick_params(axis='x', rotation=15)

    # 각 막대 위에 값 표시
    for i, (cat, mean_val) in enumerate(zip(categories, means)):
        axes[0].text(i, mean_val + max(means) * 0.02, f'{mean_val:.0f}',
                     ha='center', fontsize=10, fontweight='bold')

    # 우측: 비율 파이 차트
    axes[1].pie(means, labels=categories, autopct='%1.1f%%',
                colors=colors[:len(categories)], startangle=90,
                textprops={'fontsize': 11})
    axes[1].set_title(f'{category_name} 유형별 비율', fontsize=14, fontweight='bold')

    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] 그래프 저장: {save_path}")

    plt.show()


def generate_sample_cctv_data():
    """샘플 CCTV 데이터 생성"""
    np.random.seed(RANDOM_SEED)
    data = {
        '자치구': SEOUL_DISTRICTS,
        '방범용': np.random.randint(CCTV_RANGE['방범용'][0], CCTV_RANGE['방범용'][1], 25),
        '교통단속용': np.random.randint(CCTV_RANGE['교통단속용'][0], CCTV_RANGE['교통단속용'][1], 25),
        '어린이안전용': np.random.randint(CCTV_RANGE['어린이안전용'][0], CCTV_RANGE['어린이안전용'][1], 25),
        '기타': np.random.randint(CCTV_RANGE['기타'][0], CCTV_RANGE['기타'][1], 25)
    }
    df = pd.DataFrame(data)
    df['총_CCTV'] = df[['방범용', '교통단속용', '어린이안전용', '기타']].sum(axis=1)
    return df


def generate_sample_crime_data():
    """샘플 범죄 데이터 생성"""
    np.random.seed(RANDOM_SEED)
    data = {
        '자치구': SEOUL_DISTRICTS,
        '절도': np.random.randint(CRIME_RANGE['절도'][0], CRIME_RANGE['절도'][1], 25),
        '강도': np.random.randint(CRIME_RANGE['강도'][0], CRIME_RANGE['강도'][1], 25),
        '차량범죄': np.random.randint(CRIME_RANGE['차량범죄'][0], CRIME_RANGE['차량범죄'][1], 25),
        '공공장소폭력': np.random.randint(CRIME_RANGE['공공장소폭력'][0], CRIME_RANGE['공공장소폭력'][1], 25),
        '성범죄': np.random.randint(CRIME_RANGE['성범죄'][0], CRIME_RANGE['성범죄'][1], 25)
    }
    df = pd.DataFrame(data)
    df['총_범죄'] = df[['절도', '강도', '차량범죄', '공공장소폭력', '성범죄']].sum(axis=1)
    return df


def generate_sample_population_data():
    """샘플 인구 데이터 생성"""
    np.random.seed(RANDOM_SEED)
    base = POPULATION_CONFIG['base_population']
    pop_range = POPULATION_CONFIG['population_range']
    min_pop = POPULATION_CONFIG['min_population']
    area_range = POPULATION_CONFIG['area_range']

    populations = base + np.random.randint(pop_range[0], pop_range[1], 25)
    populations = np.maximum(populations, min_pop)

    data = {
        '자치구': SEOUL_DISTRICTS,
        '인구수': populations,
        '면적_km2': np.random.uniform(area_range[0], area_range[1], 25).round(2)
    }
    df = pd.DataFrame(data)
    df['인구밀도'] = (df['인구수'] / df['면적_km2']).round(0).astype(int)
    return df

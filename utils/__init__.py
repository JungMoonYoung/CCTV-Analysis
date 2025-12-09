"""
Utils 패키지

프로젝트 전반에서 사용되는 공통 유틸리티
"""

from .constants import *
from .helpers import *

__all__ = [
    # constants
    'SEOUL_DISTRICTS',
    'CCTV_RANGE',
    'CRIME_RANGE',
    'CCTV_EFFECT_CRIMES',
    'POPULATION_CONFIG',
    'COLOR_PALETTE',
    'PLOT_STYLE',
    'RANDOM_SEED',
    'DATA_PATHS',
    'ANALYSIS_YEAR',
    'IQR_THRESHOLD',

    # helpers
    'set_korean_font',
    'set_plot_style',
    'print_data_info',
    'save_csv_safely',
    'validate_data',
    'plot_distribution',
    'create_summary_stats',
    'plot_multiple_distributions',
    'check_district_consistency',
    'format_number',
    'standardize_district_name',
    'detect_outliers_iqr',
    'calculate_ratio_columns',
    'plot_category_analysis',
    'generate_sample_cctv_data',
    'generate_sample_crime_data',
    'generate_sample_population_data'
]

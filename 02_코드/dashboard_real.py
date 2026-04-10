"""
서울시 CCTV와 범죄 발생 상관 분석 대시보드 (실제 데이터)
Streamlit을 사용한 인터랙티브 데이터 시각화
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="서울시 CCTV-범죄 분석 대시보드",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일 설정
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed/integrated_data_with_analysis.csv', encoding='utf-8-sig')

        # 사분면 분류 추가
        cctv_median = df['방범CCTV_per_1000'].median()
        crime_median = df['CCTV효과범죄_per_1000'].median()

        def classify_quadrant(row):
            cctv = row['방범CCTV_per_1000']
            crime = row['CCTV효과범죄_per_1000']
            if cctv >= cctv_median and crime >= crime_median:
                return 'Q1: 고CCTV/고범죄'
            elif cctv < cctv_median and crime >= crime_median:
                return 'Q2: 저CCTV/고범죄 (우선순위)'
            elif cctv < cctv_median and crime < crime_median:
                return 'Q3: 저CCTV/저범죄'
            else:
                return 'Q4: 고CCTV/저범죄 (효과적)'

        df['분면'] = df.apply(classify_quadrant, axis=1)
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 메인 헤더
st.markdown('<div class="main-header">📹 서울시 CCTV와 범죄 발생 상관 분석</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: gray;">2024년 실제 데이터 기반</p>', unsafe_allow_html=True)
st.markdown("---")

# 데이터 로드
df = load_data()

if df is None:
    st.error("데이터를 불러올 수 없습니다. 파일 경로를 확인해주세요.")
    st.stop()

# 사이드바 - 필터 옵션
st.sidebar.header("🔍 필터 옵션")

# 자치구 선택
selected_districts = st.sidebar.multiselect(
    "자치구 선택",
    options=sorted(df['자치구'].unique().tolist()),
    default=sorted(df['자치구'].unique().tolist())
)

# 분면 선택
quadrant_options = sorted(df['분면'].unique().tolist())
selected_quadrants = st.sidebar.multiselect(
    "분면 선택",
    options=quadrant_options,
    default=quadrant_options
)

# 데이터 필터링
filtered_df = df[
    (df['자치구'].isin(selected_districts)) &
    (df['분면'].isin(selected_quadrants))
]

# 주요 지표 표시
st.markdown('<div class="sub-header">📊 주요 지표</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cctv = filtered_df['CCTV_총계'].sum()
    st.metric("총 CCTV 대수", f"{int(total_cctv):,}대")

with col2:
    total_crime = filtered_df['총범죄_발생'].sum()
    st.metric("총 범죄 건수", f"{int(total_crime):,}건")

with col3:
    avg_cctv_per_capita = filtered_df['CCTV_per_1000'].mean()
    st.metric("평균 인구당 CCTV", f"{avg_cctv_per_capita:.2f}대/천명")

with col4:
    avg_crime_rate = filtered_df['범죄_per_1000'].mean()
    st.metric("평균 범죄율", f"{avg_crime_rate:.2f}건/천명")

st.markdown("---")

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 개요", "📹 CCTV 분석", "🚨 범죄 분석", "🗺️ 상관관계", "📋 데이터 테이블"])

# 탭 1: 개요
with tab1:
    st.markdown('<div class="sub-header">4사분면 분류 분석</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # 4사분면 산점도
        fig = px.scatter(
            filtered_df,
            x='방범CCTV_per_1000',
            y='CCTV효과범죄_per_1000',
            color='분면',
            size='CCTV_총계',
            hover_data=['자치구', 'CCTV_총계', '총범죄_발생'],
            text='자치구',
            title='방범 CCTV 밀도 vs CCTV효과범죄율 (4사분면 분석)',
            labels={
                '방범CCTV_per_1000': '인구 천명당 방범 CCTV (대)',
                'CCTV효과범죄_per_1000': '인구 천명당 CCTV효과범죄 (건)'
            },
            color_discrete_map={
                'Q1: 고CCTV/고범죄': '#ff7f0e',
                'Q2: 저CCTV/고범죄 (우선순위)': '#d62728',
                'Q3: 저CCTV/저범죄': '#2ca02c',
                'Q4: 고CCTV/저범죄 (효과적)': '#1f77b4'
            }
        )

        # 중앙값 기준선 추가
        median_cctv = filtered_df['방범CCTV_per_1000'].median()
        median_crime = filtered_df['CCTV효과범죄_per_1000'].median()

        fig.add_hline(y=median_crime, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=median_cctv, line_dash="dash", line_color="gray", opacity=0.5)

        fig.update_traces(textposition='top center', textfont_size=8)
        fig.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 분면별 통계
        st.markdown("#### 분면별 자치구 수")
        quadrant_counts = filtered_df['분면'].value_counts()

        fig_pie = px.pie(
            values=quadrant_counts.values,
            names=quadrant_counts.index,
            title='분면별 분포',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("#### 분면별 평균 지표")
        quadrant_stats = filtered_df.groupby('분면').agg({
            '방범CCTV_per_1000': 'mean',
            'CCTV효과범죄_per_1000': 'mean',
            'CCTV_총계': 'sum'
        }).round(2)
        quadrant_stats.columns = ['평균 방범CCTV', '평균 CCTV효과범죄율', '총 CCTV']
        st.dataframe(quadrant_stats, use_container_width=True)

    # 상관관계 요약
    st.markdown("#### 주요 상관관계 분석")
    col1, col2, col3 = st.columns(3)

    with col1:
        corr1 = filtered_df['CCTV_per_1000'].corr(filtered_df['범죄_per_1000'])
        st.metric("전체 CCTV vs 전체 범죄", f"{corr1:.4f}")

    with col2:
        corr2 = filtered_df['방범CCTV_per_1000'].corr(filtered_df['CCTV효과범죄_per_1000'])
        st.metric("방범 CCTV vs CCTV효과범죄", f"{corr2:.4f}")

    with col3:
        corr3 = filtered_df['CCTV_총계'].corr(filtered_df['총범죄_발생'])
        st.metric("CCTV 대수 vs 범죄 건수", f"{corr3:.4f}")

# 탭 2: CCTV 분석
with tab2:
    st.markdown('<div class="sub-header">CCTV 설치 현황 분석</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 자치구별 총 CCTV 순위
        top_districts = filtered_df.nlargest(10, 'CCTV_총계')[['자치구', 'CCTV_총계']].sort_values('CCTV_총계', ascending=True)

        fig_top_cctv = px.bar(
            top_districts,
            x='CCTV_총계',
            y='자치구',
            orientation='h',
            title='CCTV 설치 대수 상위 10개 자치구',
            labels={'CCTV_총계': 'CCTV 대수', '자치구': ''},
            text='CCTV_총계',
            color='CCTV_총계',
            color_continuous_scale='Blues'
        )
        fig_top_cctv.update_traces(texttemplate='%{text:,.0f}대', textposition='outside')
        fig_top_cctv.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_cctv, use_container_width=True)

    with col2:
        # 인구당 CCTV 순위
        top_cctv_per_capita = filtered_df.nlargest(10, 'CCTV_per_1000')[['자치구', 'CCTV_per_1000']].sort_values('CCTV_per_1000', ascending=True)

        fig_per_capita = px.bar(
            top_cctv_per_capita,
            x='CCTV_per_1000',
            y='자치구',
            orientation='h',
            title='인구 천명당 CCTV 상위 10개 자치구',
            labels={'CCTV_per_1000': '인구 천명당 CCTV', '자치구': ''},
            text='CCTV_per_1000',
            color='CCTV_per_1000',
            color_continuous_scale='Greens'
        )
        fig_per_capita.update_traces(texttemplate='%{text:.2f}대', textposition='outside')
        fig_per_capita.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_per_capita, use_container_width=True)

    # CCTV 유형별 분포
    st.markdown("#### CCTV 유형별 설치 현황")

    cctv_by_district = filtered_df[['자치구', '방범용', '어린이보호구역', '교통단속', '공원놀이터']].set_index('자치구')
    cctv_by_district = cctv_by_district.nlargest(10, '방범용')

    fig_stack = px.bar(
        cctv_by_district,
        title='자치구별 CCTV 유형별 설치 현황 (상위 10개 자치구)',
        labels={'value': 'CCTV 대수', 'variable': 'CCTV 유형'},
        barmode='stack',
        height=400
    )
    st.plotly_chart(fig_stack, use_container_width=True)

# 탭 3: 범죄 분석
with tab3:
    st.markdown('<div class="sub-header">범죄 발생 현황 분석</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 자치구별 총 범죄 순위
        top_crime_districts = filtered_df.nlargest(10, '총범죄_발생')[['자치구', '총범죄_발생']].sort_values('총범죄_발생', ascending=True)

        fig_top_crime = px.bar(
            top_crime_districts,
            x='총범죄_발생',
            y='자치구',
            orientation='h',
            title='범죄 발생 건수 상위 10개 자치구',
            labels={'총범죄_발생': '범죄 건수', '자치구': ''},
            text='총범죄_발생',
            color='총범죄_발생',
            color_continuous_scale='Reds'
        )
        fig_top_crime.update_traces(texttemplate='%{text:,}건', textposition='outside')
        fig_top_crime.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_crime, use_container_width=True)

    with col2:
        # 인구당 범죄율
        crime_rate = filtered_df.nlargest(10, '범죄_per_1000')[['자치구', '범죄_per_1000']].sort_values('범죄_per_1000', ascending=True)

        fig_rate = px.bar(
            crime_rate,
            x='범죄_per_1000',
            y='자치구',
            orientation='h',
            title='인구당 범죄율 상위 10개 자치구',
            labels={'범죄_per_1000': '범죄율 (건/천명)', '자치구': ''},
            text='범죄_per_1000',
            color='범죄_per_1000',
            color_continuous_scale='Oranges'
        )
        fig_rate.update_traces(texttemplate='%{text:.2f}건', textposition='outside')
        fig_rate.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_rate, use_container_width=True)

    # 범죄 유형별 분석
    st.markdown("#### 범죄 유형별 발생 현황")

    crime_types = filtered_df[['자치구', '살인_발생', '강도_발생', '강간강제추행_발생', '절도_발생', '폭력_발생']].set_index('자치구')
    crime_types = crime_types.nlargest(10, '절도_발생')

    fig_crime_stack = px.bar(
        crime_types,
        title='자치구별 범죄 유형별 발생 현황 (상위 10개 자치구)',
        labels={'value': '발생 건수', 'variable': '범죄 유형'},
        barmode='stack',
        height=400
    )
    st.plotly_chart(fig_crime_stack, use_container_width=True)

# 탭 4: 상관관계 분석
with tab4:
    st.markdown('<div class="sub-header">CCTV와 범죄 간 상관관계</div>', unsafe_allow_html=True)

    # 상관관계 매트릭스
    correlation_columns = [
        'CCTV_per_1000', '방범CCTV_per_1000',
        '범죄_per_1000', 'CCTV효과범죄_per_1000',
        '총인구', '고령자수'
    ]

    corr_matrix = filtered_df[correlation_columns].corr()

    fig_corr = px.imshow(
        corr_matrix,
        labels=dict(color="상관계수"),
        x=['전체 CCTV', '방범 CCTV', '전체 범죄율', 'CCTV효과범죄율', '총인구', '고령자수'],
        y=['전체 CCTV', '방범 CCTV', '전체 범죄율', 'CCTV효과범죄율', '총인구', '고령자수'],
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title='상관관계 히트맵',
        zmin=-1,
        zmax=1,
        text_auto='.2f'
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

    # 개별 산점도
    st.markdown("#### CCTV vs 범죄 산점도")

    col1, col2 = st.columns(2)

    with col1:
        # 전체 CCTV vs 전체 범죄
        fig_scatter1 = px.scatter(
            filtered_df,
            x='CCTV_per_1000',
            y='범죄_per_1000',
            color='분면',
            size='총인구',
            hover_data=['자치구'],
            text='자치구',
            title='전체 CCTV vs 전체 범죄율',
            labels={
                'CCTV_per_1000': '인구 천명당 CCTV (대)',
                '범죄_per_1000': '인구 천명당 범죄 (건)'
            },
            trendline="ols"
        )
        fig_scatter1.update_traces(textposition='top center', textfont_size=8)
        fig_scatter1.update_layout(height=400)
        st.plotly_chart(fig_scatter1, use_container_width=True)

    with col2:
        # 방범 CCTV vs CCTV효과범죄
        fig_scatter2 = px.scatter(
            filtered_df,
            x='방범CCTV_per_1000',
            y='CCTV효과범죄_per_1000',
            color='분면',
            size='총인구',
            hover_data=['자치구'],
            text='자치구',
            title='방범 CCTV vs CCTV효과범죄율',
            labels={
                '방범CCTV_per_1000': '인구 천명당 방범 CCTV (대)',
                'CCTV효과범죄_per_1000': '인구 천명당 CCTV효과범죄 (건)'
            },
            trendline="ols"
        )
        fig_scatter2.update_traces(textposition='top center', textfont_size=8)
        fig_scatter2.update_layout(height=400)
        st.plotly_chart(fig_scatter2, use_container_width=True)

# 탭 5: 데이터 테이블
with tab5:
    st.markdown('<div class="sub-header">데이터 테이블</div>', unsafe_allow_html=True)

    # 주요 컬럼만 표시
    display_columns = [
        '자치구', 'CCTV_총계', '방범용', '총범죄_발생', 'CCTV효과범죄',
        '총인구', 'CCTV_per_1000', '범죄_per_1000',
        '방범CCTV_per_1000', 'CCTV효과범죄_per_1000', '분면'
    ]

    # 컬럼명 변경
    display_df = filtered_df[display_columns].copy()
    display_df.columns = [
        '자치구', 'CCTV 총계', '방범용 CCTV', '총 범죄', 'CCTV효과범죄',
        '총 인구', 'CCTV/천명', '범죄율/천명',
        '방범CCTV/천명', 'CCTV효과범죄율/천명', '분면'
    ]

    # 데이터 표시
    st.dataframe(
        display_df.sort_values('자치구'),
        use_container_width=True,
        height=400
    )

    # CSV 다운로드 버튼
    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name='cctv_crime_analysis_2024.csv',
        mime='text/csv'
    )

# 사이드바 - 정보
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 프로젝트 정보")
st.sidebar.info("""
**서울시 CCTV-범죄 상관 분석**

이 대시보드는 2024년 실제 데이터를 바탕으로
서울시 자치구별 CCTV 설치 현황과
범죄 발생 간의 관계를 분석합니다.

**주요 발견:**
- CCTV와 범죄 간 강한 양의 상관관계 (r=0.77)
- 범죄가 많은 지역에 CCTV를 더 많이 설치

**주요 기능:**
- 4사분면 분류 분석
- CCTV 유형별 분석
- 범죄 유형별 분석
- 상관관계 분석
- 인터랙티브 시각화

**데이터 출처:**
- 서울 열린데이터광장 (2024년)
- 공공데이터포털
""")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>서울시 CCTV와 범죄 발생 상관 분석 대시보드 | 2024년 실제 데이터 기준</p>
    <p>Made with Streamlit 📊</p>
</div>
""", unsafe_allow_html=True)

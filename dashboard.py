"""
서울시 CCTV와 범죄 발생 상관 분석 대시보드
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
        df = pd.read_csv('data/processed/integrated_data_with_quadrant.csv', encoding='utf-8-sig')
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# 메인 헤더
st.markdown('<div class="main-header">📹 서울시 CCTV와 범죄 발생 상관 분석 대시보드</div>', unsafe_allow_html=True)
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
    options=df['자치구'].unique().tolist(),
    default=df['자치구'].unique().tolist()
)

# 분면 선택
quadrant_options = df['분면'].unique().tolist()
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
    total_cctv = filtered_df['총_CCTV'].sum()
    st.metric("총 CCTV 대수", f"{total_cctv:,}대")

with col2:
    total_crime = filtered_df['총_범죄'].sum()
    st.metric("총 범죄 건수", f"{total_crime:,}건")

with col3:
    avg_cctv_per_capita = filtered_df['인구당_총CCTV'].mean()
    st.metric("평균 인구당 CCTV", f"{avg_cctv_per_capita:.2f}대")

with col4:
    avg_crime_rate = filtered_df['인구당_CCTV효과범죄율'].mean()
    st.metric("평균 범죄율", f"{avg_crime_rate:.2f}%")

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
            x='인구당_총CCTV',
            y='인구당_CCTV효과범죄율',
            color='분면',
            size='총_CCTV',
            hover_data=['자치구', '총_CCTV', '총_범죄'],
            text='자치구',
            title='CCTV 밀도 vs 범죄율 (4사분면 분석)',
            color_discrete_map={
                'Q1: 고CCTV/고범죄': '#ff7f0e',
                'Q2: 저CCTV/고범죄 (우선순위)': '#d62728',
                'Q3: 저CCTV/저범죄': '#2ca02c',
                'Q4: 고CCTV/저범죄 (효과적)': '#1f77b4'
            }
        )

        # 중앙값 기준선 추가
        median_cctv = filtered_df['인구당_총CCTV'].median()
        median_crime = filtered_df['인구당_CCTV효과범죄율'].median()

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
            '인구당_총CCTV': 'mean',
            '인구당_CCTV효과범죄율': 'mean',
            '총_CCTV': 'sum'
        }).round(2)
        st.dataframe(quadrant_stats, use_container_width=True)

# 탭 2: CCTV 분석
with tab2:
    st.markdown('<div class="sub-header">CCTV 유형별 분석</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # CCTV 유형별 비율
        cctv_types = ['방범용', '교통단속용', '어린이안전용', '기타']
        total_by_type = filtered_df[cctv_types].sum()

        fig_cctv_type = px.bar(
            x=cctv_types,
            y=total_by_type.values,
            title='CCTV 유형별 설치 현황',
            labels={'x': 'CCTV 유형', 'y': '설치 대수'},
            color=cctv_types,
            text=total_by_type.values
        )
        fig_cctv_type.update_traces(texttemplate='%{text:,}대', textposition='outside')
        fig_cctv_type.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_cctv_type, use_container_width=True)

    with col2:
        # 자치구별 총 CCTV 순위
        top_districts = filtered_df.nlargest(10, '총_CCTV')[['자치구', '총_CCTV']].sort_values('총_CCTV', ascending=True)

        fig_top_cctv = px.bar(
            top_districts,
            x='총_CCTV',
            y='자치구',
            orientation='h',
            title='CCTV 설치 대수 상위 10개 자치구',
            labels={'총_CCTV': 'CCTV 대수', '자치구': ''},
            text='총_CCTV',
            color='총_CCTV',
            color_continuous_scale='Blues'
        )
        fig_top_cctv.update_traces(texttemplate='%{text:,}대', textposition='outside')
        fig_top_cctv.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_cctv, use_container_width=True)

    # CCTV 밀도 히트맵
    st.markdown("#### 자치구별 CCTV 유형별 비율 히트맵")

    heatmap_data = filtered_df[['자치구', '방범용_비율', '교통단속용_비율', '어린이안전용_비율', '기타_비율']].set_index('자치구')

    fig_heatmap = px.imshow(
        heatmap_data.T,
        labels=dict(x="자치구", y="CCTV 유형", color="비율 (%)"),
        x=heatmap_data.index,
        y=['방범용', '교통단속용', '어린이안전용', '기타'],
        aspect="auto",
        color_continuous_scale='YlOrRd',
        title='자치구별 CCTV 유형 비율'
    )
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# 탭 3: 범죄 분석
with tab3:
    st.markdown('<div class="sub-header">범죄 유형별 분석</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 범죄 유형별 발생 건수
        crime_types = ['절도', '강도', '차량범죄', '공공장소폭력', '성범죄']
        total_by_crime = filtered_df[crime_types].sum()

        fig_crime_type = px.pie(
            values=total_by_crime.values,
            names=crime_types,
            title='범죄 유형별 발생 비율',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_crime_type.update_traces(textposition='inside', textinfo='percent+label')
        fig_crime_type.update_layout(height=400)
        st.plotly_chart(fig_crime_type, use_container_width=True)

    with col2:
        # 자치구별 총 범죄 순위
        top_crime_districts = filtered_df.nlargest(10, '총_범죄')[['자치구', '총_범죄']].sort_values('총_범죄', ascending=True)

        fig_top_crime = px.bar(
            top_crime_districts,
            x='총_범죄',
            y='자치구',
            orientation='h',
            title='범죄 발생 건수 상위 10개 자치구',
            labels={'총_범죄': '범죄 건수', '자치구': ''},
            text='총_범죄',
            color='총_범죄',
            color_continuous_scale='Reds'
        )
        fig_top_crime.update_traces(texttemplate='%{text:,}건', textposition='outside')
        fig_top_crime.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_top_crime, use_container_width=True)

    # CCTV 효과 범죄 분석
    st.markdown("#### CCTV 효과 범죄 (절도, 강도, 차량범죄) 분석")

    col1, col2 = st.columns(2)

    with col1:
        # CCTV 효과 범죄 합계
        cctv_effect_crimes = filtered_df.nlargest(10, 'CCTV효과범죄_합계')[['자치구', 'CCTV효과범죄_합계']].sort_values('CCTV효과범죄_합계', ascending=True)

        fig_effect = px.bar(
            cctv_effect_crimes,
            x='CCTV효과범죄_합계',
            y='자치구',
            orientation='h',
            title='CCTV 효과 범죄 상위 10개 자치구',
            labels={'CCTV효과범죄_합계': '범죄 건수', '자치구': ''},
            text='CCTV효과범죄_합계',
            color='CCTV효과범죄_합계',
            color_continuous_scale='Oranges'
        )
        fig_effect.update_traces(texttemplate='%{text:,}건', textposition='outside')
        fig_effect.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_effect, use_container_width=True)

    with col2:
        # 인구당 범죄율
        crime_rate = filtered_df.nlargest(10, '인구당_CCTV효과범죄율')[['자치구', '인구당_CCTV효과범죄율']].sort_values('인구당_CCTV효과범죄율', ascending=True)

        fig_rate = px.bar(
            crime_rate,
            x='인구당_CCTV효과범죄율',
            y='자치구',
            orientation='h',
            title='인구당 CCTV효과범죄율 상위 10개 자치구',
            labels={'인구당_CCTV효과범죄율': '범죄율 (%)', '자치구': ''},
            text='인구당_CCTV효과범죄율',
            color='인구당_CCTV효과범죄율',
            color_continuous_scale='Reds'
        )
        fig_rate.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_rate.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_rate, use_container_width=True)

# 탭 4: 상관관계 분석
with tab4:
    st.markdown('<div class="sub-header">CCTV와 범죄 간 상관관계</div>', unsafe_allow_html=True)

    # 상관관계 매트릭스
    correlation_columns = [
        '인구당_총CCTV', '인구당_방범용', '인구당_교통단속용', '인구당_어린이안전용',
        '인구당_CCTV효과범죄율', '인구당_절도율', '인구당_강도율', '인구당_차량범죄율'
    ]

    corr_matrix = filtered_df[correlation_columns].corr()

    fig_corr = px.imshow(
        corr_matrix,
        labels=dict(color="상관계수"),
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        title='상관관계 히트맵',
        zmin=-1,
        zmax=1
    )
    fig_corr.update_layout(height=600)
    st.plotly_chart(fig_corr, use_container_width=True)

    # 개별 상관관계 분석
    st.markdown("#### 개별 변수 간 상관관계")

    col1, col2 = st.columns(2)

    with col1:
        x_var = st.selectbox(
            "X축 변수 선택",
            options=correlation_columns,
            index=0
        )

    with col2:
        y_var = st.selectbox(
            "Y축 변수 선택",
            options=correlation_columns,
            index=4
        )

    # 산점도
    fig_scatter = px.scatter(
        filtered_df,
        x=x_var,
        y=y_var,
        color='분면',
        size='인구수',
        hover_data=['자치구'],
        text='자치구',
        title=f'{x_var} vs {y_var}',
        trendline="ols"
    )
    fig_scatter.update_traces(textposition='top center', textfont_size=8)
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 상관계수 표시
    correlation = filtered_df[x_var].corr(filtered_df[y_var])
    st.info(f"상관계수: {correlation:.4f}")

# 탭 5: 데이터 테이블
with tab5:
    st.markdown('<div class="sub-header">데이터 테이블</div>', unsafe_allow_html=True)

    # 표시할 컬럼 선택
    all_columns = filtered_df.columns.tolist()
    selected_columns = st.multiselect(
        "표시할 컬럼 선택",
        options=all_columns,
        default=['자치구', '총_CCTV', '총_범죄', '인구수', '인구당_총CCTV', '인구당_CCTV효과범죄율', '분면']
    )

    if selected_columns:
        # 데이터 표시
        st.dataframe(
            filtered_df[selected_columns].sort_values('자치구'),
            use_container_width=True,
            height=400
        )

        # CSV 다운로드 버튼
        csv = filtered_df[selected_columns].to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name='cctv_crime_analysis.csv',
            mime='text/csv'
        )
    else:
        st.warning("표시할 컬럼을 선택해주세요.")

# 사이드바 - 정보
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 프로젝트 정보")
st.sidebar.info("""
**서울시 CCTV-범죄 상관 분석**

이 대시보드는 서울시 자치구별 CCTV 설치 현황과
범죄 발생 간의 관계를 분석합니다.

**주요 기능:**
- 4사분면 분류 분석
- CCTV 유형별 분석
- 범죄 유형별 분석
- 상관관계 분석
- 인터랙티브 시각화

**데이터 출처:**
- 서울 열린데이터광장
- 공공데이터포털
- 통계청 KOSIS
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ 사용 방법")
st.sidebar.markdown("""
1. 좌측 필터에서 자치구와 분면을 선택하세요
2. 각 탭을 클릭하여 다양한 분석 결과를 확인하세요
3. 그래프 위에 마우스를 올려 상세 정보를 확인하세요
4. 데이터 테이블 탭에서 원본 데이터를 확인하고 다운로드할 수 있습니다
""")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>서울시 CCTV와 범죄 발생 상관 분석 대시보드 | 2023년 데이터 기준</p>
    <p>Made with Streamlit 📊</p>
</div>
""", unsafe_allow_html=True)

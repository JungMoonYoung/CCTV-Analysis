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
tab_summary, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📌 SUMMARY", "📈 개요", "📹 CCTV 분석", "🚨 범죄 분석", "🗺️ 상관관계", "📋 데이터 테이블"]
)

# ============================================================
# 📌 SUMMARY 탭 — 인사이트 브리핑 (진입 첫 화면)
# ============================================================
with tab_summary:
    # ---------- 컴팩트 히어로 ----------
    st.markdown("""
    <div style="padding:20px 26px;border-radius:14px;
                background:linear-gradient(135deg,#1e3a8a 0%,#7f1d1d 100%);
                border:1px solid rgba(255,255,255,0.08);margin-bottom:18px;">
        <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
            <div style="font-size:24px;font-weight:800;color:#fff;">
                🚨 서울시 안전 인프라 최적화
            </div>
            <div style="font-size:14px;color:#fca5a5;letter-spacing:0.5px;">
                공공데이터로 정책 제안 수준의 인사이트를 도출할 수 있습니다
            </div>
        </div>
        <div style="font-size:14px;color:#e5e7eb;margin-top:8px;line-height:1.6;">
            24개 자치구 × 36개 변수 분석으로 <b style="color:#fff;">CCTV-범죄의 역인과 관계</b>를 데이터로 규명하고,
            <b style="color:#fca5a5;">사분면별 차별화 전략</b>으로 정책 우선순위를 제안합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- 4×4 매트릭스 ----------
    C_FIND = "#3b82f6"   # Blue - 문제 발견
    C_METHOD = "#ef4444" # Red - 분석 방법
    C_POLICY = "#10b981" # Green - 정책 제안

    td_base = (
        "padding:18px 20px;vertical-align:top;"
        "border:1px solid rgba(255,255,255,0.08);"
        "background:rgba(255,255,255,0.03);"
    )
    td_label = (
        "padding:18px 20px;vertical-align:top;"
        "border:1px solid rgba(255,255,255,0.08);"
        "background:rgba(252,165,165,0.08);"
        "width:14%;"
    )

    def _header_cell(icon, title, color, question):
        return (
            f'<td style="{td_base}border-top:3px solid {color};width:28.6%;">'
            f'<div style="font-size:32px;line-height:1;">{icon}</div>'
            f'<div style="font-size:22px;font-weight:800;color:{color};margin:10px 0 6px 0;letter-spacing:-0.5px;">{title}</div>'
            f'<div style="color:#e5e7eb;font-size:13.5px;font-style:italic;line-height:1.5;">{question}</div>'
            f'</td>'
        )

    def _label_cell(icon, text):
        return (
            f'<td style="{td_label}">'
            f'<div style="font-size:22px;">{icon}</div>'
            f'<div style="color:#fff;font-size:16px;font-weight:800;margin-top:6px;line-height:1.3;">{text}</div>'
            f'</td>'
        )

    def _content_cell(html_content, color=None, bold=False):
        weight = "600" if bold else "400"
        col = color if color else "#e5e7eb"
        return (
            f'<td style="{td_base}">'
            f'<div style="color:{col};font-size:14px;line-height:1.8;font-weight:{weight};">{html_content}</div>'
            f'</td>'
        )

    table_html = (
        '<table style="width:100%;border-collapse:separate;border-spacing:0;border-radius:14px;overflow:hidden;">'
        # 헤더
        '<tr>'
        f'{_label_cell("🗂️", "구분")}'
        f'{_header_cell("🔍", "문제 발견", C_FIND, "CCTV가 많을수록 범죄가 많다? r=0.768의 함정")}'
        f'{_header_cell("📊", "분석 방법", C_METHOD, "24개 자치구를 어떻게 차별화 분류할 것인가")}'
        f'{_header_cell("💡", "정책 제안", C_POLICY, "어디에 먼저, 얼마나 — 판단할 수 있는 근거")}'
        '</tr>'
        # 행 1: 문제 정의
        '<tr>'
        f'{_label_cell("🎯", "문제 정의")}'
        f'{_content_cell("단순 상관계수만 보면<br>인과 방향을 오해하기 쉽다")}'
        f'{_content_cell("자치구 간 편차가 커서<br>평균만 보면 특성이 묻힌다")}'
        f'{_content_cell("\"어디에 먼저, 얼마나\"를<br>정량적 근거로 답해야 한다")}'
        '</tr>'
        # 행 2: 접근 방법
        '<tr>'
        f'{_label_cell("🔬", "접근 방법")}'
        f'{_content_cell("• 상관·회귀 분석<br>• <b>상위 5구 교차 검증</b><br>• 시차 분석")}'
        f'{_content_cell("• 인구당 CCTV × 범죄율<br>• <b>4사분면 자동 분류</b><br>• Z-score 위험도 점수화")}'
        f'{_content_cell("• 사분면별 전략 매핑<br>• 격차 −20.9% 산출<br>• 예산 우선순위 도출")}'
        '</tr>'
        # 행 3: 왜 이 방법인가
        '<tr>'
        f'{_label_cell("📌", "왜 이 방법인가")}'
        f'{_content_cell("r=0.768만 보면<br><b>\"CCTV가 범죄 유발\"</b> 오해")}'
        f'{_content_cell("CV=0.419 변동성 →<br><b>일괄 정책은 비효율</b>")}'
        f'{_content_cell("단순 순위가 아닌<br><b>구조적 분류</b>가 필요")}'
        '</tr>'
        # 행 4: 정책 활용
        '<tr>'
        f'{_label_cell("💼", "정책 활용")}'
        f'{_content_cell("→ <b>역인과 규명</b><br>범죄 → CCTV (예방 X)", color=C_FIND, bold=True)}'
        f'{_content_cell("→ Q2 확충 / Q1 운영 고도화 /<br>Q4 벤치마킹 전략 분리", color=C_METHOD, bold=True)}'
        f'{_content_cell("→ 구로·노원·은평 등<br><b>최우선 설치 6개 구</b> 도출", color=C_POLICY, bold=True)}'
        '</tr>'
        '</table>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("")

    # ---------- 핵심 발견 3가지 ----------
    st.markdown('<h3 style="margin-top:18px;">🏆 핵심 발견 3가지</h3>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.error(
            "**1️⃣ 역인과관계 확인**\n\n"
            "CCTV 설치 상위 5개 자치구 = 범죄 발생 상위 5개 자치구.\n\n"
            "→ CCTV는 \"예방용\"이 아니라 **사건 이후에 따라가는 형태**로 배치. "
            "**\"범죄 증가 → CCTV 설치\"** 의 역인과."
        )
    with f2:
        st.warning(
            "**2️⃣ 최우선 설치 지역 도출**\n\n"
            "Q2 (저CCTV/고범죄) **4개 구**, 평균 6.60대(인구 1,000명당).\n\n"
            "→ 중앙값 8.34대 대비 **−20.9% 격차**. 이 격차만 메워도 밀도 기준 취약 지역 해소 가능."
        )
    with f3:
        st.info(
            "**3️⃣ 자치구 간 변동성 (CV=0.419)**\n\n"
            "변동성이 높아 하나의 정책을 일괄 적용하는 것은 비효율적.\n\n"
            "→ **사분면별 차별화 전략**이 필수."
        )

    st.success(
        "💡 **핵심 메시지**: \"숫자가 보여주는 것과 숫자가 의미하는 것은 다르다.\" "
        "분석가의 역할은 숫자를 내는 것이 아니라 **올바르게 해석하는 것**."
    )

    st.markdown("---")

    # ---------- 상세 탭 (접이식) ----------
    itab1, itab2, itab3 = st.tabs([
        "🧭 방법론 선택의 근거",
        "🛠️ 문제 해결 경험",
        "💼 정책 활용 시나리오",
    ])

    with itab1:
        st.caption("\"통계를 돌린 것\"과 \"통계를 고른 것\"은 다릅니다. 이 프로젝트에서 각 방법을 선택한 이유입니다.")
        method_df = pd.DataFrame({
            "분석 단계": ["인과 해석", "자치구 분류", "위험도 측정", "정책 제안"],
            "흔한 접근": [
                "상관계수만 보고 결론",
                "평균·순위 나열",
                "절대값 비교",
                "일괄 권고",
            ],
            "이 프로젝트 선택": [
                "상위 5구 교차 검증 + 시차 분석",
                "인구당 CCTV × 범죄율 4사분면 자동 분류",
                "Z-score 표준화 점수화",
                "사분면별 차별화 전략",
            ],
            "선택 이유": [
                "r=0.768 → \"CCTV가 범죄 유발\" 오해 방지",
                "CV=0.419 변동성 → 평균 무의미",
                "자치구 규모(인구) 차이 보정",
                "Q2는 확충, Q1은 운영 고도화 등 맞춤 처방",
            ],
        })
        st.dataframe(method_df, use_container_width=True, hide_index=True)

    with itab2:
        st.caption("분석 과정에서 마주친 두 가지 핵심 문제와 해결 과정입니다.")

        st.markdown("#### 1️⃣ 역인과관계 해석의 오류 방지")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.error(
                "**🚨 문제**\n\n"
                "CCTV-범죄 상관계수 **r=0.768** → "
                "단순 해석 시 **\"CCTV가 범죄를 유발한다\"** 는 잘못된 결론에 빠질 위험"
            )
        with c2:
            st.info(
                "**🔧 해결**\n\n"
                "상위 5구 교차 검증 + 4사분면 분류로 "
                "**\"범죄가 먼저, CCTV가 뒤따라\"** 구조 검증"
            )
        with c3:
            st.success(
                "**🎓 결과**\n\n"
                "**\"CCTV 증가 → 범죄 증가\"** 가 아닌 "
                "**\"범죄 증가 → CCTV 설치\"** 역인과 방향을 데이터로 규명"
            )

        st.markdown("")
        st.markdown("#### 2️⃣ 자치구 편차를 무시한 일괄 분석의 한계")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.error(
                "**🚨 문제**\n\n"
                "24개 자치구를 하나의 평균으로 분석하면 지역별 특성이 묻힘 "
                "(**CV=0.419**, 변동성 높음)"
            )
        with c2:
            st.info(
                "**🔧 해결**\n\n"
                "인구당 CCTV × 범죄율 기준 **4사분면 자동 분류 모델** + "
                "**Z-score 위험도 점수화**"
            )
        with c3:
            st.success(
                "**🎓 결과**\n\n"
                "동일 정책이 아닌 "
                "**사분면별 차별화 전략**(Q2 확충 / Q1 운영 고도화)의 근거 마련"
            )

    with itab3:
        st.caption("이 분석 결과를 실제 서울시 정책에 적용할 수 있는 3가지 시나리오입니다.")

        # 1. 최우선 과제
        st.markdown("#### 🚨 1. 최우선 과제: Q2(저CCTV/고범죄) CCTV 확충")
        st.markdown(
            f'<div style="padding:18px;border-radius:12px;'
            f'background:rgba(239,68,68,0.06);'
            f'border:1px solid rgba(239,68,68,0.25);">'
            f'<div style="color:#e5e7eb;font-size:14px;line-height:1.75;">'
            f'<b style="color:#fff;">구로구 · 노원구 · 은평구 · 종로구 · 성동구 · 용산구</b><br>'
            f'CCTV 밀도가 낮으면서 범죄율이 높은 가장 취약한 지역. '
            f'Q2와 중앙값 격차(<b style="color:{C_METHOD};">−20.9%</b>) 해소만으로 밀도 기준 취약 지역 해소 가능.<br>'
            f'<b style="color:{C_POLICY};">목표</b>: 2028년까지 구로구·노원구를 중앙값(8.34대) 수준으로 보급.'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("")

        # 2. 사분면별 차별화 전략
        st.markdown("#### 🎯 2. 사분면별 차별화 전략")
        st.caption("CV=0.419 → 전 자치구 일괄 정책은 비효율적. 사분면별 맞춤 전략이 필요합니다.")
        quadrant_df = pd.DataFrame({
            "사분면": ["Q1 (고/고)", "Q2 (저/고)", "Q3 (저/저)", "Q4 (고/저)"],
            "자치구": [
                "송파·강동·영등포·중구·관악",
                "구로·노원·은평·종로·성동·용산",
                "중랑·강서·양천·금천·강북",
                "강남·서초·광진·도봉",
            ],
            "전략": [
                "AI 영상분석·경찰 순찰 연계 등 운영 고도화",
                "신규 설치 최우선",
                "현 수준 유지, 분기별 모니터링",
                "벤치마크 대상 → 강남 방식을 구로·노원에 적용",
            ],
        })
        st.dataframe(quadrant_df, use_container_width=True, hide_index=True)

        st.markdown("")

        # 3. 예산 배분 우선순위
        st.markdown("#### 💰 3. 예산 배분 우선순위")
        budget_df = pd.DataFrame({
            "순위": ["1순위", "2순위", "3순위"],
            "대상 자치구": [
                "구로·노원·은평·종로",
                "송파·강동·영등포",
                "중랑·강서·금천",
            ],
            "정책": [
                "CCTV 신규 설치",
                "운영 고도화",
                "모니터링 유지",
            ],
        })
        st.dataframe(budget_df, use_container_width=True, hide_index=True)

        st.success(
            "💡 \"어디에 먼저, 얼마나\"를 판단할 수 있는 **데이터 기반 정책 근거**."
        )

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

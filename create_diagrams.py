"""
프로젝트 아키텍처 다이어그램 생성 스크립트
diagrams 라이브러리를 사용하여 프로페셔널한 아키텍처 다이어그램 생성

설치 방법:
pip install diagrams
brew install graphviz  # macOS
apt-get install graphviz  # Ubuntu/Debian
choco install graphviz  # Windows
"""

try:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.custom import Custom
    from diagrams.programming.language import Python
    from diagrams.programming.framework import Flask
    from diagrams.onprem.analytics import Jupyter
    from diagrams.onprem.vcs import Github
    from diagrams.saas.analytics import Snowflake
    from diagrams.generic.storage import Storage
    from diagrams.generic.database import SQL

    print("diagrams 라이브러리를 사용할 수 있습니다!")
    print("다이어그램을 생성하려면 이 스크립트를 실행하세요.")
    print("\n아래 코드의 주석을 해제하고 실행하세요:\n")

    # 시스템 아키텍처 다이어그램
    with Diagram("CCTV 분석 시스템 아키텍처", filename="docs/system_architecture", show=False, direction="TB"):
        with Cluster("데이터 소스"):
            api_sources = [
                Storage("서울 열린데이터\nCCTV 데이터"),
                Storage("공공데이터포털\n범죄 통계"),
                Storage("통계청 KOSIS\n인구 통계")
            ]

        with Cluster("데이터 수집"):
            collector = Python("fetch_seoul_data.py")
            raw_storage = Storage("data/raw/")

        with Cluster("데이터 처리"):
            cleaner = Jupyter("데이터 정제")
            integrator = Jupyter("데이터 통합")
            processed_storage = Storage("data/processed/")

        with Cluster("분석"):
            eda = Jupyter("탐색적 분석")
            regression = Jupyter("회귀 분석")
            classification = Jupyter("지역 분류")

        with Cluster("시각화"):
            dashboard = Python("Streamlit\n대시보드")
            reports = Storage("분석 리포트")

        with Cluster("배포"):
            github = Github("GitHub")
            cloud = Custom("Streamlit Cloud", "./assets/streamlit_icon.png")

        # 데이터 플로우
        api_sources >> collector >> raw_storage
        raw_storage >> cleaner >> integrator >> processed_storage
        processed_storage >> [eda, regression, classification]
        [eda, regression, classification] >> reports
        processed_storage >> dashboard
        [dashboard, reports] >> github >> cloud

    print("✅ 시스템 아키텍처 다이어그램 생성 완료!")
    print("   파일: docs/system_architecture.png\n")

    # 데이터 파이프라인 다이어그램
    with Diagram("데이터 파이프라인", filename="docs/data_pipeline", show=False, direction="LR"):
        with Cluster("Extract"):
            api_call = Python("API 호출")
            json_response = Storage("JSON")

        with Cluster("Transform"):
            to_csv = Python("CSV 변환")
            clean = Python("정제")
            integrate = Python("통합")
            derive = Python("파생변수")

        with Cluster("Load"):
            processed = SQL("Processed\nData")

        with Cluster("Analyze"):
            analyze = [
                Jupyter("통계 분석"),
                Jupyter("회귀 모델"),
                Jupyter("시각화")
            ]

        with Cluster("Output"):
            output = [
                Storage("리포트"),
                Python("대시보드")
            ]

        api_call >> json_response >> to_csv >> clean >> integrate >> derive >> processed >> analyze >> output

    print("✅ 데이터 파이프라인 다이어그램 생성 완료!")
    print("   파일: docs/data_pipeline.png\n")

except ImportError:
    print("⚠️  diagrams 라이브러리가 설치되지 않았습니다.")
    print("\n다음 명령어로 설치할 수 있습니다:")
    print("1. pip install diagrams")
    print("2. Graphviz 설치:")
    print("   - macOS: brew install graphviz")
    print("   - Ubuntu/Debian: sudo apt-get install graphviz")
    print("   - Windows: choco install graphviz")
    print("\n또는 DIAGRAMS.md 파일의 Mermaid 다이어그램을 사용하세요!")
    print("Mermaid 다이어그램은 GitHub에서 자동으로 렌더링됩니다.")

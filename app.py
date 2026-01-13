"""설문 문항별 원그래프 - Streamlit 앱"""
import streamlit as st

from survey_viewer.config.settings import configure_matplotlib, configure_streamlit
from survey_viewer.data.loader import ExcelDataLoader
from survey_viewer.data.preprocessor import TestResponseFilter
from survey_viewer.data.question_parser import QuestionParser
from survey_viewer.visualization.factory import create_default_factory
from survey_viewer.ui.sidebar import SidebarUI
from survey_viewer.ui.main_content import MainContentUI
from survey_viewer.ui.participant_view import ParticipantView


def main():
    # 설정 초기화
    configure_matplotlib()
    configure_streamlit()

    # 파일 업로드
    file = st.file_uploader("xlsx 업로드", type=["xlsx"])
    if not file:
        st.stop()

    # 데이터 로딩
    loader = ExcelDataLoader(file)
    sheet = st.selectbox("시트 선택", loader.get_sheet_names())
    df = loader.load_sheet(sheet)

    # 전처리
    preprocessor = TestResponseFilter()
    df = preprocessor.process(df)
    st.caption(f"분석에 포함된 응답 수: {len(df)} (테스트 응답 제외 적용)")

    # 문항 파싱
    parser = QuestionParser()
    questions = parser.parse(df)

    # 차트 팩토리
    chart_factory = create_default_factory()

    # 사이드바 렌더링
    sidebar = SidebarUI(questions)
    options = sidebar.render()

    # 탭 UI
    tab1, tab2 = st.tabs(["문항별 분석", "참여자별 응답"])

    with tab1:
        main_content = MainContentUI(df, questions, chart_factory, options)
        main_content.render()

    with tab2:
        participant_view = ParticipantView(df, questions)
        participant_view.render()


if __name__ == "__main__":
    main()

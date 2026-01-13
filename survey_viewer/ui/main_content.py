"""본문 UI - 문항별 시각화"""
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from ..data.question_parser import Question
from ..analysis.detectors import QuestionType, detect_question_type
from ..analysis.aggregators import get_aggregator
from ..visualization.base import ChartOptions
from ..visualization.factory import ChartFactory
from .sidebar import DisplayOptions


class MainContentUI:
    """본문 UI 컴포넌트"""

    def __init__(
        self,
        df: pd.DataFrame,
        questions: List[Question],
        chart_factory: ChartFactory,
        options: DisplayOptions
    ):
        self.df = df
        self.questions = questions
        self.chart_factory = chart_factory
        self.options = options

    def render(self) -> None:
        """모든 문항 렌더링"""
        for question in self.questions:
            self._render_question(question)

    def _render_question(self, question: Question) -> None:
        """개별 문항 렌더링"""
        series = self.df[question.column_name]
        question_type = detect_question_type(question.column_name, series)

        # 앵커 및 제목
        st.markdown(
            f'<div id="{question.anchor_id}"></div>',
            unsafe_allow_html=True
        )
        st.subheader(question.display_title)

        if question_type == QuestionType.TEXT:
            self._render_text_question(series)
        else:
            self._render_chart_question(series, question_type)

        st.divider()

    def _render_text_question(self, series: pd.Series) -> None:
        """서술형 문항 렌더링"""
        s = series.dropna().astype(str).str.strip()
        s = s[(s != "") & (s != ".")]

        st.caption(f"서술형 응답 수: {len(s)}")
        st.dataframe(s.to_frame(name="응답"), width='stretch')

    def _render_chart_question(
        self,
        series: pd.Series,
        question_type: QuestionType
    ) -> None:
        """차트 문항 렌더링 (객관식)"""
        # 집계
        is_multi = question_type == QuestionType.MULTI_SELECT
        aggregator = get_aggregator(is_multi)
        value_counts = aggregator.aggregate(series, self.options.include_blank)

        if value_counts.empty:
            st.info("집계할 응답이 없습니다.")
            return

        # 차트 렌더링
        chart_options = ChartOptions(
            top_n=self.options.top_n,
            include_blank=self.options.include_blank
        )
        renderer = self.chart_factory.get("pie")
        fig, display_data = renderer.render(value_counts, chart_options)

        # 2컬럼 레이아웃
        c1, c2 = st.columns([1, 1])

        with c1:
            if fig is not None:
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)

        with c2:
            stat_df = pd.DataFrame({
                "응답": value_counts.index,
                "빈도": value_counts.values,
                "비율(%)": (value_counts.values / value_counts.values.sum() * 100).round(2),
            })
            st.dataframe(stat_df, width='stretch')

"""사이드바 UI"""
from dataclasses import dataclass
from typing import List

import streamlit as st

from ..data.question_parser import Question


@dataclass
class DisplayOptions:
    """표시 옵션"""
    include_blank: bool = False
    top_n: int = 8


class SidebarUI:
    """사이드바 UI 컴포넌트"""

    def __init__(self, questions: List[Question]):
        self.questions = questions

    def render(self) -> DisplayOptions:
        """사이드바 렌더링 및 옵션 반환"""
        with st.sidebar:
            self._render_navigation()
            st.divider()
            return self._render_options()

    def _render_navigation(self) -> None:
        """문항 바로가기 네비게이션"""
        st.header("문항 바로가기")
        st.caption("아래 문항을 클릭하면 해당 섹션으로 이동합니다.")

        toc_lines = []
        for q in self.questions:
            toc_lines.append(
                f'- <a href="#{q.anchor_id}">{q.display_title}</a>'
            )

        st.markdown("\n".join(toc_lines), unsafe_allow_html=True)

    def _render_options(self) -> DisplayOptions:
        """표시 옵션 UI"""
        st.header("표시 옵션")

        include_blank = st.checkbox("무응답(Blank) 포함", value=False)
        top_n = st.slider("Pie Top N (나머지 Other)", 3, 15, 8)

        return DisplayOptions(
            include_blank=include_blank,
            top_n=top_n
        )

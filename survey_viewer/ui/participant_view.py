"""참여자별 응답 보기 UI"""
from typing import List

import pandas as pd
import streamlit as st

from ..data.question_parser import Question


class ParticipantView:
    """참여자별 응답 보기 컴포넌트"""

    def __init__(self, df: pd.DataFrame, questions: List[Question]):
        self.df = df
        self.questions = questions

    def render(self) -> None:
        """참여자별 응답 렌더링"""
        # 참여자 컬럼 확인
        if "참여자" not in self.df.columns:
            st.warning("'참여자' 컬럼이 없습니다.")
            return

        # 참여자 목록
        participants = self.df["참여자"].dropna().unique().tolist()
        if not participants:
            st.info("참여자 데이터가 없습니다.")
            return

        # 참여자 선택
        selected = st.selectbox(
            "참여자 선택",
            options=participants,
            index=0
        )

        # 선택된 참여자의 응답 필터링
        row = self.df[self.df["참여자"] == selected]

        if row.empty:
            st.warning("선택된 참여자의 응답이 없습니다.")
            return

        st.caption(f"'{selected}'님의 응답")

        # 문항-응답 테이블 생성
        response_data = []
        for q in self.questions:
            value = row[q.column_name].values[0]
            # NaN 처리
            if pd.isna(value):
                value = "(무응답)"
            response_data.append({
                "문항": q.display_title,
                "응답": str(value)
            })

        # 테이블 표시
        response_df = pd.DataFrame(response_data)
        st.dataframe(
            response_df,
            use_container_width=True,
            hide_index=True
        )

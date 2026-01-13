"""문항 파싱 - Q번호 부여 및 Question 데이터 구조"""
import re
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd

from ..config.constants import META_COLS


@dataclass
class Question:
    """설문 문항 데이터"""
    id: int
    column_name: str       # 원본 컬럼명
    display_title: str     # 표시용 제목 (Q1. ...)

    @property
    def anchor_id(self) -> str:
        """HTML 앵커 ID"""
        return f"q{self.id}"


class QuestionParser:
    """문항 컬럼 추출 및 파싱"""

    def __init__(self, meta_cols: set = None):
        self.meta_cols = meta_cols or META_COLS

    def parse(self, df: pd.DataFrame) -> List[Question]:
        """DataFrame에서 문항 목록 추출"""
        question_cols = [c for c in df.columns if c not in self.meta_cols]

        questions = []
        for i, col in enumerate(question_cols, start=1):
            display_title = f"Q{i}. {self._strip_existing_q_prefix(col)}"
            questions.append(Question(
                id=i,
                column_name=col,
                display_title=display_title
            ))

        return questions

    def _strip_existing_q_prefix(self, title: str) -> str:
        """기존 Q번호 접두사 제거"""
        return re.sub(r"^\s*Q\d+\.\s*", "", title).strip()

    def get_column_map(self, questions: List[Question]) -> Dict[str, str]:
        """display_title -> column_name 매핑"""
        return {q.display_title: q.column_name for q in questions}

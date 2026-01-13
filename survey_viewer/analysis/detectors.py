"""문항 유형 감지 - 서술형/객관식 판별"""
from enum import Enum
from typing import List

import pandas as pd


class QuestionType(Enum):
    """문항 유형"""
    SINGLE_SELECT = "single"    # 단일 선택
    MULTI_SELECT = "multi"      # 복수 선택
    TEXT = "text"               # 서술형


# 서술형 힌트 키워드
TEXT_HINTS = ["적어", "순서대로", "떠올려", "사례", "문의/불만", "기준", "어떻게"]


def is_text_question(title: str, series: pd.Series) -> bool:
    """서술형 문항 여부 판별"""
    # 연락처 문항
    if "연락처" in title:
        return True

    # 서술형 힌트 키워드 포함
    if any(hint in title for hint in TEXT_HINTS):
        return True

    # 평균 글자수가 길면 서술형으로 가정
    s = series.dropna().astype(str).str.strip()
    if len(s) == 0:
        return False

    return s.str.len().mean() > 80


def is_multi_select(title: str, series: pd.Series) -> bool:
    """복수 선택 문항 여부 판별"""
    # 문항 제목에 "최대" 포함
    if "최대" in title:
        return True

    # 응답에 파이프(|) 포함
    s_str = series.dropna().astype(str)
    return s_str.str.contains(r"\|").any()


def detect_question_type(title: str, series: pd.Series) -> QuestionType:
    """문항 유형 감지"""
    if is_text_question(title, series):
        return QuestionType.TEXT

    if is_multi_select(title, series):
        return QuestionType.MULTI_SELECT

    return QuestionType.SINGLE_SELECT

"""집계 로직 - 단일/복수 선택 응답 집계"""
import re
from abc import ABC, abstractmethod

import pandas as pd


PIPE_SPLIT = r"\s*\|\s*"


class Aggregator(ABC):
    """집계기 추상 클래스"""

    @abstractmethod
    def aggregate(self, series: pd.Series, include_blank: bool = False) -> pd.Series:
        """응답 집계 수행"""
        pass


class SingleSelectAggregator(Aggregator):
    """단일 선택 응답 집계"""

    def aggregate(self, series: pd.Series, include_blank: bool = False) -> pd.Series:
        s = series.copy()

        if include_blank:
            s = s.fillna("Blank").astype(str).str.strip().replace("", "Blank")
            return s.value_counts()

        s = s.dropna().astype(str).str.strip()
        s = s[s != ""]
        return s.value_counts()


class MultiSelectAggregator(Aggregator):
    """복수 선택 응답 집계 (| 구분자)"""

    def aggregate(self, series: pd.Series, include_blank: bool = False) -> pd.Series:
        tokens = []

        for v in series.tolist():
            parts = self._split_pipe(v)
            if not parts and include_blank:
                tokens.append("Blank")
            else:
                tokens.extend(parts)

        if not tokens:
            return pd.Series(dtype=int)

        return pd.Series(tokens).value_counts()

    def _split_pipe(self, value) -> list:
        """파이프(|) 구분자로 분리"""
        if value is None:
            return []

        s = str(value).strip()
        if s == "" or s.lower() == "nan" or s == ".":
            return []

        return [x.strip() for x in re.split(PIPE_SPLIT, s) if x and x.strip()]


def get_aggregator(is_multi_select: bool) -> Aggregator:
    """문항 유형에 맞는 집계기 반환"""
    if is_multi_select:
        return MultiSelectAggregator()
    return SingleSelectAggregator()

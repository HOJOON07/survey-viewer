"""데이터 전처리 - 테스트 응답 제외 등"""
from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from ..config.constants import CONTACT_COL, EXCLUDE_CONTACT_KEYWORDS


class DataPreprocessor(ABC):
    """데이터 전처리기 추상 클래스"""

    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """DataFrame 전처리 수행"""
        pass


class TestResponseFilter(DataPreprocessor):
    """테스트 응답 필터링"""

    def __init__(
        self,
        contact_col: str = CONTACT_COL,
        exclude_keywords: List[str] = None
    ):
        self.contact_col = contact_col
        self.exclude_keywords = exclude_keywords or EXCLUDE_CONTACT_KEYWORDS

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.contact_col not in df.columns:
            return df

        pattern = "|".join(self.exclude_keywords)
        mask = df[self.contact_col].astype(str).str.contains(pattern, na=False)
        return df[~mask].reset_index(drop=True)


class PreprocessorPipeline(DataPreprocessor):
    """여러 전처리기를 체인으로 연결"""

    def __init__(self, preprocessors: List[DataPreprocessor]):
        self.preprocessors = preprocessors

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df
        for preprocessor in self.preprocessors:
            result = preprocessor.process(result)
        return result

"""데이터 로딩 - Excel 파일 처리"""
from abc import ABC, abstractmethod
from typing import List, BinaryIO

import pandas as pd


class DataLoader(ABC):
    """데이터 로더 추상 클래스"""

    @abstractmethod
    def get_sheet_names(self) -> List[str]:
        """시트 이름 목록 반환"""
        pass

    @abstractmethod
    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        """지정된 시트를 DataFrame으로 로드"""
        pass


class ExcelDataLoader(DataLoader):
    """Excel 파일 로더"""

    def __init__(self, file: BinaryIO):
        self._excel_file = pd.ExcelFile(file)

    def get_sheet_names(self) -> List[str]:
        return self._excel_file.sheet_names

    def load_sheet(self, sheet_name: str) -> pd.DataFrame:
        return pd.read_excel(
            self._excel_file,
            sheet_name=sheet_name
        ).reset_index(drop=True)

"""차트 렌더러 추상 클래스 및 옵션"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class ChartOptions:
    """차트 렌더링 옵션"""
    top_n: int = 8
    include_blank: bool = False
    figsize: Tuple[int, int] = (6, 6)


class ChartRenderer(ABC):
    """차트 렌더러 추상 클래스"""

    @abstractmethod
    def render(
        self,
        data: pd.Series,
        options: ChartOptions
    ) -> Tuple[Optional[plt.Figure], pd.Series]:
        """
        차트 렌더링

        Args:
            data: 집계된 데이터 (value_counts 결과)
            options: 차트 옵션

        Returns:
            (Figure 또는 None, 표시용 데이터)
        """
        pass

    @abstractmethod
    def get_chart_type(self) -> str:
        """차트 유형 반환"""
        pass

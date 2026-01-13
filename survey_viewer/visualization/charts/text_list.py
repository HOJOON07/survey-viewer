"""서술형 응답 리스트 렌더러"""
from typing import Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt

from ..base import ChartRenderer, ChartOptions


class TextListRenderer(ChartRenderer):
    """서술형 응답 리스트 렌더러 (차트 없음)"""

    def render(
        self,
        data: pd.Series,
        options: ChartOptions
    ) -> Tuple[Optional[plt.Figure], pd.Series]:
        # 서술형은 차트가 없으므로 None 반환
        # data는 원본 시리즈 그대로 반환
        return None, data

    def get_chart_type(self) -> str:
        return "text"

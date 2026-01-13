"""원그래프 렌더러"""
from typing import Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt

from ..base import ChartRenderer, ChartOptions


class PieChartRenderer(ChartRenderer):
    """원그래프 렌더러"""

    def render(
        self,
        data: pd.Series,
        options: ChartOptions
    ) -> Tuple[Optional[plt.Figure], pd.Series]:
        if data.empty:
            return None, data

        # Top N + Other 처리
        display_data = data.copy()
        if len(display_data) > options.top_n:
            top = display_data.head(options.top_n)
            other = display_data.iloc[options.top_n:].sum()
            display_data = pd.concat([top, pd.Series({"Other": other})])

        # 차트 생성
        fig, ax = plt.subplots(figsize=options.figsize)
        ax.pie(
            display_data.values,
            labels=display_data.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")

        return fig, display_data

    def get_chart_type(self) -> str:
        return "pie"

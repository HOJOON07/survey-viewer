"""차트 팩토리 - 차트 렌더러 생성 및 관리"""
from typing import Dict

from .base import ChartRenderer
from .charts.pie_chart import PieChartRenderer
from .charts.text_list import TextListRenderer
from ..analysis.detectors import QuestionType


class ChartFactory:
    """차트 렌더러 팩토리"""

    def __init__(self):
        self._renderers: Dict[str, ChartRenderer] = {}

    def register(self, chart_type: str, renderer: ChartRenderer) -> None:
        """렌더러 등록"""
        self._renderers[chart_type] = renderer

    def get(self, chart_type: str) -> ChartRenderer:
        """렌더러 반환"""
        if chart_type not in self._renderers:
            raise ValueError(f"Unknown chart type: {chart_type}")
        return self._renderers[chart_type]

    def get_for_question_type(self, question_type: QuestionType) -> ChartRenderer:
        """문항 유형에 맞는 렌더러 반환"""
        if question_type == QuestionType.TEXT:
            return self.get("text")
        return self.get("pie")


def create_default_factory() -> ChartFactory:
    """기본 차트 팩토리 생성"""
    factory = ChartFactory()
    factory.register("pie", PieChartRenderer())
    factory.register("text", TextListRenderer())
    return factory

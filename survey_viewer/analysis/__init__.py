"""분석 모듈 - 집계 및 문항 유형 감지"""
from .aggregators import Aggregator, SingleSelectAggregator, MultiSelectAggregator
from .detectors import QuestionType, detect_question_type

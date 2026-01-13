"""앱 설정 - 폰트, 페이지 설정"""
import platform
import warnings
import matplotlib.pyplot as plt
import streamlit as st


def configure_matplotlib() -> None:
    """matplotlib 한글 폰트 및 경고 설정"""
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

    system = platform.system()
    if system == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:
        plt.rcParams['font.family'] = 'NanumGothic'

    plt.rcParams['axes.unicode_minus'] = False


def configure_streamlit() -> None:
    """Streamlit 페이지 설정"""
    st.set_page_config(page_title="설문 문항별 원그래프", layout="wide")
    st.title("설문 문항별 원그래프")

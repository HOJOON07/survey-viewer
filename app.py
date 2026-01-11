import re
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="설문 문항별 원그래프", layout="wide")
st.title("설문 문항별 원그래프")

# ---- 필수 설치:
# pip install streamlit pandas openpyxl matplotlib

file = st.file_uploader("xlsx 업로드", type=["xlsx"])
if not file:
    st.stop()

# 시트 선택
xls = pd.ExcelFile(file)
sheet = st.selectbox("시트 선택", xls.sheet_names)
df = pd.read_excel(xls, sheet_name=sheet).reset_index(drop=True)

# =========================
# 1) 테스트 응답 제외 (연락처 컬럼 기준)
# =========================
CONTACT_COL = "연락처(이메일/전화번호), 가능한 시간대"
EXCLUDE_CONTACT_KEYWORDS = ["성종연", "김상진"]  # "김상진 테스트"도 포함됨

if CONTACT_COL in df.columns:
    mask = df[CONTACT_COL].astype(str).str.contains("|".join(EXCLUDE_CONTACT_KEYWORDS), na=False)
    df = df[~mask].reset_index(drop=True)

st.caption(f"분석에 포함된 응답 수: {len(df)} (테스트 응답 제외 적용)")

# =========================
# 2) 문항 컬럼 추출 + Q번호 붙이기
# =========================
META_COLS = {
    "응답일시",
    "참여자",
    "본 설문은 오프라인 모임/이벤트 운영 프로세스 개선을 위한 리서치이며, 응답은 익명 통계로만 사용됩니다.(*)",
}
question_cols = [c for c in df.columns if c not in META_COLS]

def strip_existing_q_prefix(title: str) -> str:
    # 이미 "Q1. ..." 형태면 앞의 Q번호는 제거하고 다시 붙여줌
    return re.sub(r"^\s*Q\d+\.\s*", "", title).strip()

display_items = []
col_map = {}  # display -> original col
for i, col in enumerate(question_cols, start=1):
    disp = f"Q{i}. {strip_existing_q_prefix(col)}"
    display_items.append(disp)
    col_map[disp] = col

# =========================
# 3) 도우미: 복수선택(|) 집계 + pie
# =========================
PIPE_SPLIT = r"\s*\|\s*"

def split_pipe(v):
    if v is None:
        return []
    s = str(v).strip()
    if s == "" or s.lower() == "nan" or s == ".":
        return []
    return [x.strip() for x in re.split(PIPE_SPLIT, s) if x and x.strip()]

def value_counts_single(series: pd.Series, include_blank: bool):
    s = series.copy()
    if include_blank:
        s = s.fillna("Blank").astype(str).str.strip().replace("", "Blank")
        return s.value_counts()
    s = s.dropna().astype(str).str.strip()
    s = s[s != ""]
    return s.value_counts()

def value_counts_multi(series: pd.Series, include_blank: bool):
    tokens = []
    for v in series.tolist():
        parts = split_pipe(v)
        if not parts and include_blank:
            tokens.append("Blank")
        else:
            tokens.extend(parts)
    if not tokens:
        return pd.Series(dtype=int)
    return pd.Series(tokens).value_counts()

def plot_pie(vc: pd.Series, top_n: int = 8):
    if vc.empty:
        return None, vc
    vc2 = vc.copy()
    if len(vc2) > top_n:
        top = vc2.head(top_n)
        other = vc2.iloc[top_n:].sum()
        vc2 = pd.concat([top, pd.Series({"Other": other})])
    fig, ax = plt.subplots()
    ax.pie(vc2.values, labels=vc2.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    return fig, vc2

def is_text_question(col_title: str, series: pd.Series) -> bool:
    # 연락처/서술형 문항은 pie 대신 리스트로
    if "연락처" in col_title:
        return True
    # 서술형 힌트(문항 문장에 “적어주세요/떠올려” 등)
    hints = ["적어", "순서대로", "떠올려", "사례", "문의/불만", "기준", "어떻게"]
    if any(h in col_title for h in hints):
        return True
    # 평균 글자수가 길면 서술형으로 가정
    s = series.dropna().astype(str).str.strip()
    if len(s) == 0:
        return False
    return (s.str.len().mean() > 80)

# =========================
# 4) 사이드바: 문항 목록(클릭 이동) + 옵션
#    "문항을 누르면 원그래프 표시"를 TOC 링크로 해결
#    기본은 아래 본문에서 전부 원그래프가 이미 렌더됨
# =========================
with st.sidebar:
    st.header("문항 바로가기")
    st.caption("아래 문항을 클릭하면 해당 섹션으로 이동합니다.")
    toc_lines = []
    for idx, disp in enumerate(display_items, start=1):
        toc_lines.append(f'- <a href="#q{idx}">{disp}</a>')
    st.markdown("\n".join(toc_lines), unsafe_allow_html=True)

    st.divider()
    st.header("표시 옵션")
    include_blank = st.checkbox("무응답(Blank) 포함", value=False)
    top_n = st.slider("Pie Top N (나머지 Other)", 3, 15, 8)

# =========================
# 5) 본문: 기본 상태에서 모든 문항 원그래프(또는 서술 리스트) 표시
# =========================
for idx, disp in enumerate(display_items, start=1):
    col = col_map[disp]
    series = df[col]

    # 앵커(TOC 클릭 이동)
    st.markdown(f'<div id="q{idx}"></div>', unsafe_allow_html=True)
    st.subheader(disp)

    if is_text_question(col, series):
        # 서술형: pie 대신 응답 리스트
        s = series.dropna().astype(str).str.strip()
        s = s[(s != "") & (s != ".")]
        st.caption(f"서술형 응답 수: {len(s)}")
        st.dataframe(s.to_frame(name="응답"), use_container_width=True)
        st.divider()
        continue

    # 객관식(단일/복수) 자동 판별: 값에 '|'가 있으면 복수로 처리
    s_str = series.dropna().astype(str)
    is_multi = s_str.str.contains(r"\|").any() or ("최대" in col)

    vc = value_counts_multi(series, include_blank) if is_multi else value_counts_single(series, include_blank)
    if vc.empty:
        st.info("집계할 응답이 없습니다.")
        st.divider()
        continue

    fig, vc_pie = plot_pie(vc, top_n=top_n)

    c1, c2 = st.columns([1, 1])
    with c1:
        if fig is not None:
            st.pyplot(fig, clear_figure=True)
    with c2:
        stat_df = pd.DataFrame({
            "응답": vc.index,
            "빈도": vc.values,
            "비율(%)": (vc.values / vc.values.sum() * 100).round(2),
        })
        st.dataframe(stat_df, use_container_width=True)

    st.divider()

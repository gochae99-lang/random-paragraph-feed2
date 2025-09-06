import streamlit as st
import pdfplumber
import random

st.set_page_config(page_title="랜덤 텍스트 피드", layout="centered")
st.title("📖 PDF 랜덤 쓱뽕 피드")
st.markdown("PDF에서 추출한 텍스트를 랜덤으로 보여줍니다. 최신 10개까지만 표시됩니다.")

# 세션 상태 초기화
if 'texts' not in st.session_state:
    st.session_state.texts = []  # (pdf_title, chunk)
if 'feed' not in st.session_state:
    st.session_state.feed = []

# PDF 업로드
uploaded_files = st.file_uploader("📄 PDF 파일 업로드 (여러 개 가능)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_title = uploaded_file.name
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    chunks = [(pdf_title, text[i:i+280].strip()) for i in range(0, len(text), 280) if text[i:i+280].strip()]
                    st.session_state.texts.extend(chunks)
    st.success(f"{len(st.session_state.texts)} 텍스트 추출 완료!")

    # 버튼 영역
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 랜덤 텍스트 추가"):
            if st.session_state.texts:
                pdf_title, new_text = random.choice(st.session_state.texts)
                st.session_state.feed.insert(0, (pdf_title, new_text))
                st.session_state.feed = st.session_state.feed[:10]  # 최신 10개 유지

    with col2:
        if st.button("🔁 연속 랜덤 5개 추가"):
            if st.session_state.texts:
                for _ in range(min(5, len(st.session_state.texts))):
                    st.session_state.feed.insert(0, random.choice(st.session_state.texts))
                st.session_state.feed = st.session_state.feed[:10]

    # 피드 출력 (카드 스타일)
    if st.session_state.feed:
        st.markdown("### 📰 최신 랜덤 텍스트 (최대 10개)")
        for pdf_title, txt in st.session_state.feed:
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ccc; 
                    border-radius: 10px; 
                    padding: 12px; 
                    margin-bottom: 10px; 
                    background-color: #f9f9f9;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                ">
                    <strong style="color:#333;">{pdf_title}</strong>
                    <p style="margin-top:5px; font-size:14px; line-height:1.5;">{txt}</p>
                </div>
                """, unsafe_allow_html=True
            )
else:
    st.info("PDF 파일을 업로드하세요.")

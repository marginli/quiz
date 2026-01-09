import streamlit as st
import pandas as pd # 引入 pandas 用來讀取 CSV
import time
import random

# --- 1. 讀取 CSV 題庫 ---
# 使用 @st.cache_data 讓讀取速度變快，不用每次按按鈕都重讀檔案
@st.cache_data
def load_data():
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv("vocabulary.csv")
        # 轉換成我們要的格式: [{"word": "Apple", "answer": "蘋果"}, ...]
        return df.to_dict('records')
    except FileNotFoundError:
        st.error("找不到 vocabulary.csv 檔案！請確認有上傳此檔案到 GitHub。")
        return []

# 載入資料
quiz_source = load_data()

# --- 2. 初始化 Session State ---

# 確保題庫載入成功才執行
if quiz_source:
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = quiz_source.copy()
        random.shuffle(st.session_state.quiz_data)

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'wrong_attempts' not in st.session_state:
        st.session_state.wrong_attempts = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

# --- 3. 核心邏輯 (與之前相同) ---

def check_answer():
    q_index = st.session_state.current_question
    question_data = st.session_state.quiz_data[q_index]
    
    correct_english = str(question_data['word']).strip() # 確保轉為字串並去空白
    chinese_question = str(question_data['answer']).strip()
    
    user_answer = st.session_state.user_input.strip()

    if user_answer.lower() == correct_english.lower():
        st.toast(f"✅ 答對了！ {chinese_question} = {correct_english}", icon="🎉")
        st.session_state.score += 10
        st.session_state.wrong_attempts = 0
        st.session_state.current_question += 1
        st.session_state.user_input = "" 
        
    else:
        st.session_state.wrong_attempts += 1
        attempts_left = 3 - st.session_state.wrong_attempts
        
        if attempts_left > 0:
            st.error(f"❌ 答錯囉！請再試一次 (剩餘機會：{attempts_left}次)")
        else:
            st.warning(f"⚠️ 機會用完囉！正確的英文是：{correct_english}")
            st.session_state.wrong_attempts = 0
            st.session_state.current_question += 1
            st.session_state.user_input = ""
            time.sleep(2)
            st.rerun()

    if st.session_state.current_question >= len(st.session_state.quiz_data):
        st.session_state.game_over = True

def restart_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.wrong_attempts = 0
    st.session_state.game_over = False
    st.session_state.user_input = ""
    # 重新讀取並洗牌
    st.session_state.quiz_data = quiz_source.copy()
    random.shuffle(st.session_state.quiz_data)

# --- 4. 建立 UI 畫面 ---

st.title("🦁 國小英文單字大挑戰 (1200單字版)")

# 檢查是否有資料
if not quiz_source:
    st.warning("⚠️ 尚未建立題庫，請檢查 vocabulary.csv")
    st.stop() # 停止執行下方程式碼

if not st.session_state.game_over:
    total_q = len(st.session_state.quiz_data)
    current_q = st.session_state.current_question
    
    progress = current_q / total_q
    st.progress(progress, text=f"進度：第 {current_q + 1} 題 / 共 {total_q} 題")
    
    st.caption(f"目前得分：{st.session_state.score}")
    st.divider()

    # 顯示題目
    question_text = st.session_state.quiz_data[current_q]['answer']
    st.markdown(f"### 請拼出這個單字：")
    st.markdown(f"# 🇹🇼 {question_text}")

    st.text_input(
        "您的答案 (不分大小寫)：", 
        key="user_input", 
        on_change=check_answer
    )
    
    st.button("送出答案", on_click=check_answer)

    if st.session_state.wrong_attempts > 0:
        st.info(f"加油！這題已經試了 {st.session_state.wrong_attempts} 次...")

else:
    st.balloons()
    st.success("🎉 測驗結束！")
    st.markdown(f"## 您的最終成績是： {st.session_state.score} 分")
    st.button("🔄 重新洗牌再玩一次", on_click=restart_game)

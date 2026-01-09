import streamlit as st
import time

# --- 1. 設定題庫 ---
# 結構維持一樣： word 是英文(現在是正確答案)，answer 是中文(現在是題目)
quiz_data = [
    {"word": "Apple", "answer": "蘋果"},
    {"word": "Teacher", "answer": "老師"},
    {"word": "Student", "answer": "學生"},
    {"word": "Book", "answer": "書"},
    {"word": "Happy", "answer": "快樂"},
    {"word": "School", "answer": "學校"},
    {"word": "Cat", "answer": "貓"},
    {"word": "Dog", "answer": "狗"},
    {"word": "Friend", "answer": "朋友"},
    {"word": "Time", "answer": "時間"},
]

# --- 2. 初始化 Session State ---
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

# --- 3. 核心邏輯 ---

def check_answer():
    """檢查答案"""
    q_index = st.session_state.current_question
    question_data = quiz_data[q_index]
    
    # 【關鍵修改 1】現在正確答案是英文 (word 欄位)
    correct_english = question_data['word']
    # 題目是中文 (answer 欄位)
    chinese_question = question_data['answer']
    
    # 取得使用者輸入
    user_answer = st.session_state.user_input.strip()

    # 【關鍵修改 2】比對時忽略大小寫 (.lower())
    # 這樣輸入 apple, Apple, APPLE 都會算對
    if user_answer.lower() == correct_english.lower():
        st.toast(f"✅ 答對了！ {chinese_question} = {correct_english}", icon="🎉")
        st.session_state.score += 10
        st.session_state.wrong_attempts = 0
        st.session_state.current_question += 1
        st.session_state.user_input = "" # 清空輸入框
        
    else:
        # 答錯了
        st.session_state.wrong_attempts += 1
        attempts_left = 3 - st.session_state.wrong_attempts
        
        if attempts_left > 0:
            st.error(f"❌ 答錯囉！請再試一次 (剩餘機會：{attempts_left}次)")
        else:
            # 錯三次，顯示正確答案並強制下一題
            st.warning(f"⚠️ 機會用完囉！正確的英文是：{correct_english}")
            st.session_state.wrong_attempts = 0
            st.session_state.current_question += 1
            st.session_state.user_input = ""
            time.sleep(2)
            st.rerun()

    # 檢查是否結束
    if st.session_state.current_question >= len(quiz_data):
        st.session_state.game_over = True

def restart_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.wrong_attempts = 0
    st.session_state.game_over = False
    st.session_state.user_input = ""

# --- 4. 建立 UI 畫面 ---

st.title("🔤 英文單字拼寫大挑戰")

if not st.session_state.game_over:
    # 顯示進度
    progress = st.session_state.current_question / len(quiz_data)
    st.progress(progress, text=f"進度：第 {st.session_state.current_question + 1} 題 / 共 {len(quiz_data)} 題")
    st.markdown(f"### 目前分數：{st.session_state.score} 分")
    st.divider()

    # 【關鍵修改 3】顯示中文題目
    question_text = quiz_data[st.session_state.current_question]['answer']
    st.markdown(f"# 🇹🇼 {question_text}")
    st.caption("請在下方輸入對應的英文單字")

    # 輸入框
    st.text_input(
        "您的答案 (不分大小寫)：", 
        key="user_input", 
        on_change=check_answer
    )
    
    st.button("送出答案", on_click=check_answer)

    if st.session_state.wrong_attempts > 0:
        st.info(f"加油！這題已經試了 {st.session_state.wrong_attempts

import streamlit as st
import re
from crawler import QuizCrawler

st.title("Wayground cheat")
quiz_title = ""
quiz_total_questions = 0
quiz_questions = []
with st.form("input_form"):
    url = st.text_input(
        "Enter Wayground URL:", placeholder="https://wayground.com/join/quiz/..."
    )
    submit_button = st.form_submit_button("Submit")
    if submit_button:
        match = re.search(r"https://wayground.com/.*/quiz/([^/]+)", url)
        quiz_id = match.group(1) if match else None
        quiz_id = quiz_id.split("?")[0] if quiz_id else None
        if quiz_id:
            print(quiz_id)
            quiz_title = ""
            quiz_total_questions = 0
            quiz_questions = []
            crawler = QuizCrawler(quiz_id)
            try:
                with st.spinner("Fetching quiz data..."):
                    crawler.parse_questions()
                    st.success(f"Quiz {quiz_id} fetched successfully!")
                    quiz_title = crawler.title
                    quiz_total_questions = crawler.total_questions
                    quiz_questions = crawler.questions
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Invalid Wayground URL. Please enter a valid URL.")
container = st.container(border=True)
if quiz_questions:
    container.subheader(f"Quiz Title: {quiz_title}")
    container.write(f"Total Questions: {quiz_total_questions}")
    for idx, qa in enumerate(quiz_questions):
        container.markdown(f"Q{idx + 1}: **{qa['question'].strip()}**")
        container.markdown(f"- Answer: **{qa['answer'].strip()}**")

st.write("---")
st.markdown("Developed by [Huan](https://github.com/hvd1026)")

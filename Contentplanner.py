import streamlit as st
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os
from openai import OpenAI

# ---- Load environment variables ----
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("🧠 Universal Content Planner Generator")
st.markdown("Generate a 5-day content plan with 2 posts per day for any topic you want!")

# ---- User Input ----
topic = st.text_input("Enter the topic/category you want content for:", "AI")
num_days = st.number_input("Number of days:", min_value=1, max_value=100, value=5)
posts_per_day = st.number_input("Posts per day:", min_value=1, max_value=10, value=2)

# ---- Function to generate content dynamically (using OpenAI) ----
def generate_content(topic):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",   # or gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are a social media content planner AI."},
            {"role": "user", "content": f"Generate one content idea for {topic} with a content type, hook/caption, and engagement prompt."}
        ],
        max_tokens=120
    )
    return response.choices[0].message.content

# ---- Generate Planner ----
if st.button("Generate Content Planner"):
    planner = []
    days_list = [f"Day {i+1}" for i in range(num_days)]
    for day in days_list:
        for post_num in range(1, posts_per_day+1):
            idea = generate_content(topic)
            planner.append({
                "Day": day,
                "Post #": post_num,
                "Generated Idea": idea
            })

    df = pd.DataFrame(planner)
    st.dataframe(df)

    # CSV Download
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name=f"{topic}_Content_Planner.csv",
        mime="text/csv"
    )

    # Excel Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Planner")
    data = output.getvalue()
    st.download_button(
        label="📥 Download Excel",
        data=data,
        file_name=f"{topic}_Content_Planner.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

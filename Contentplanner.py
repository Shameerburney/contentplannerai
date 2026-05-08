import streamlit as st
import pandas as pd
from io import BytesIO
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("🧠 Universal Content Planner Generator")
st.markdown("Generate a content plan with multiple posts per day for any topic.")

# ---- User Input ----
topic = st.text_input("Enter the topic/category:", "AI")
num_days = st.number_input("Number of days:", min_value=1, max_value=100, value=5)
posts_per_day = st.number_input("Posts per day:", min_value=1, max_value=10, value=2)

# ---- Gemini Function ----
def generate_content(topic):
    try:
        prompt = f"""
You are a social media content planner AI.

Generate ONE content idea for: {topic}

Include:
- Content type
- Hook or caption
- Engagement idea

Keep it short and practical.
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Error: {e}"

# ---- Generate Planner ----
if st.button("Generate Content Planner"):
    planner = []

    for day in range(1, num_days + 1):
        for post_num in range(1, posts_per_day + 1):
            idea = generate_content(topic)

            planner.append({
                "Day": f"Day {day}",
                "Post #": post_num,
                "Generated Idea": idea
            })

    df = pd.DataFrame(planner)
    st.dataframe(df)

    # ---- CSV Download ----
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name=f"{topic}_Content_Planner.csv",
        mime="text/csv"
    )

    # ---- Excel Download ----
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Planner")

    st.download_button(
        label="📥 Download Excel",
        data=output.getvalue(),
        file_name=f"{topic}_Content_Planner.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

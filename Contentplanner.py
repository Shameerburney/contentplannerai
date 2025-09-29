import streamlit as st
import pandas as pd
from io import BytesIO
from huggingface_hub import InferenceClient

# ---- Load API key from Streamlit Secrets ----
client = InferenceClient(api_key=st.secrets["HF_API_KEY"])

st.title("🧠 Universal Content Planner Generator (Hugging Face)")
st.markdown("Generate a 5-day content plan with 2 posts per day for any topic you want!")

# ---- User Input ----
topic = st.text_input("Enter the topic/category you want content for:", "AI")
num_days = st.number_input("Number of days:", min_value=1, max_value=100, value=5)
posts_per_day = st.number_input("Posts per day:", min_value=1, max_value=10, value=2)

# ---- Function to generate content dynamically ----
def generate_content(topic):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-2-13b-chat-hf",   # 👈 Change model if needed
            messages=[
                {"role": "system", "content": "You are a social media content planner AI."},
                {"role": "user", "content": f"Generate one content idea for {topic} with a content type, hook/caption, and engagement prompt."}
            ],
            max_tokens=120
        )
        return response.choices[0].message["content"].strip()
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

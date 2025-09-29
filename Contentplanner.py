import streamlit as st
import random
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os
from openai import OpenAI

# ---- Load environment variables ----
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.title("🧠 Universal Content Planner Generator")
st.markdown("Generate a 5-day content plan with 2 posts per day for any topic you want!")

# ---- OpenAI Client ----
client = None
if api_key:
    client = OpenAI(api_key=api_key)

# ---- User Input ----
topic = st.text_input("Enter the topic/category you want content for:", "AI")
num_days = st.number_input("Number of days:", min_value=1, max_value=100, value=5)
posts_per_day = st.number_input("Posts per day:", min_value=1, max_value=10, value=2)

# ---- Function to generate content ----
def generate_content(topic):
    if client:  # If API key exists, use AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a social media content planner AI."},
                {"role": "user", "content": f"Generate one content idea for {topic} with a content type, hook/caption, and engagement prompt."}
            ],
            max_tokens=100
        )
        text = response.choices[0].message.content
        return {"Content Type": "AI Generated", "Hook / Caption": text, "Engagement Prompt": "Ask your audience about it!"}
    else:  # Fallback to random picks if no API
        content_types = [
            f"{topic} Tutorial", f"{topic} Tips", f"{topic} Story", f"{topic} Fun Fact",
            f"{topic} Trend", f"{topic} Challenge", f"{topic} News", f"{topic} Hack"
        ]
        hooks = [
            f"Learn something new about {topic} today! 🤯",
            f"{topic} hack you didn't know! ⚡",
            f"Can you try this {topic} challenge? 😎",
            f"Top {topic} trend happening right now! 🔥",
            f"{topic} fun fact that will surprise you! 🤯",
            f"Boost your {topic} skills with this tip! ✨",
            f"Story about {topic} you must read! 📖",
            f"Interesting {topic} news you missed! 📰"
        ]
        engagement_prompts = [
            f"What do you think about {topic}? Comment below!",
            f"Would you try this {topic}? YES/NO",
            f"Share your {topic} experience in the comments!",
            f"Tag someone who needs to see this {topic} tip!",
            f"Do you agree with this {topic} trend?",
            f"What’s your favorite {topic} hack?"
        ]
        return {
            "Content Type": random.choice(content_types),
            "Hook / Caption": random.choice(hooks),
            "Engagement Prompt": random.choice(engagement_prompts)
        }

# ---- Generate Planner ----
if st.button("Generate Content Planner"):
    planner = []
    days_list = [f"Day {i+1}" for i in range(num_days)]
    for day in days_list:
        for post_num in range(1, posts_per_day+1):
            post = generate_content(topic)
            planner.append({
                "Day": day,
                "Post #": post_num,
                "Content Type": post["Content Type"],
                "Hook / Caption": post["Hook / Caption"],
                "Engagement Prompt": post["Engagement Prompt"]
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

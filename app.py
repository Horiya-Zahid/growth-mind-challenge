import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import datetime

# Dark Mode & Light Mode Toggle
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"], index=0)
if theme == "Dark":
    st.markdown("""
        <style>
            body { background-color: #121212; color: #ffffff; }
            .st-bb { color: white !important; }
            .st-bj { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# Motivational Quotes List
QUOTES = [
    "Keep going! Every step counts. 🚀",
    "Mistakes are proof that you are trying. 💡",
    "Growth begins where comfort ends! 🔥",
    "Believe in yourself and your potential. 🌟",
    "Every expert was once a beginner. ✨"
]

# Load or Create Learning Progress Data
def load_data():
    try:
        df = pd.read_csv("learning_progress.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Goal", "Progress", "Notes"])
    return df

# Save Data
def save_data(df):
    df.to_csv("learning_progress.csv", index=False)

# Streamlit UI
st.title("📚 AI-Powered Learning Tracker")

# Display a Random Motivational Quote
st.sidebar.markdown("### 🌟 Today's Motivation")
st.sidebar.write(random.choice(QUOTES))

# Get Today's Date
today = datetime.date.today()

# User Input for Learning Goal
st.subheader("🎯 Set Your Learning Goal")
goal = st.text_input("Enter your learning goal for today:")
progress = st.slider("Progress (%)", 0, 100, 0)
notes = st.text_area("Write notes about today's learning:")

if st.button("Save Entry"):
    df = load_data()
    new_entry = pd.DataFrame({"Date": [today], "Goal": [goal], "Progress": [progress], "Notes": [notes]})
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    st.success("✅ Entry Saved Successfully!")

# Show Learning Progress
st.subheader("📊 Your Learning Progress")
df = load_data()

df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

df = df.dropna()

df = df.sort_values(by="Date")
if not df.empty:
    st.write(df)

    # Improved Progress Graph
    st.subheader("📈 Progress Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x="Date", y="Progress", marker="o", linestyle="-", color="#4CAF50", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Progress (%)")
    ax.set_title("Learning Progress Over Time", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("No progress recorded yet. Start tracking today!")

# Footer
st.markdown("---")
st.markdown("🚀 *Stay consistent, keep learning, and achieve your goals!*")

import streamlit as st
from google.generativeai import GenerativeModel, configure

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAd9reEF3kRFZX0DCY-5C4UbK3y4FHNdWk"
configure(api_key=GEMINI_API_KEY)

model = GenerativeModel("gemini-1.5-flash-latest")

def generate_career_path(stream, interests, location, budget, goals, perc_10, perc_11, perc_12):
    percent_info = f"10th Percentage: {perc_10}%\n11th Percentage: {perc_11}%\n"
    percent_info += f"12th Percentage: {perc_12}%" if perc_12 else "12th Percentage: Not Provided"

    prompt = f"""
    You are an expert Indian career counselor AI.

    Student Profile:
    - Stream: {stream}
    - Interests: {interests}
    - Preferred Location: {location}
    - Budget: {budget}
    - Career Goals: {goals}
    - Academic Performance:
      {percent_info}

    Please generate a personalized career roadmap:
    1. Suggest **at least 6 colleges in India** (top government & private), with **correct state locations**.
    2. List entrance exams required.
    3. Recommend suitable programs + certifications.
    4. Give step-by-step actions to reach goals.
    5. Suggest scholarships and free resources.
    """
    response = model.generate_content(prompt)
    return response.text

# 🌈 Streamlit App UI
def main():
    st.set_page_config(page_title="Career Path Advisor", layout="centered")

    # ✅ Custom CSS for better design
    st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #d4fc79, #96e6a1);
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background: linear-gradient(to right, #d4fc79, #96e6a1);
        }
        .card {
            background-color: #ffffffcc;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            max-width: 700px;
            margin: auto;
        }
        h1, h5 {
            color: #0b6e4f;
        }
        .stButton>button {
            background-color: #0b6e4f;
            color: white;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h1>🎓 Career Path Advisor</h1>", unsafe_allow_html=True)
    st.markdown("<h5>Smart, personalized career roadmap after 12th!</h5>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

    with st.form("career_form"):
        stream = st.selectbox("📘 Stream in 12th Standard", ["Science", "Commerce", "Arts", "Vocational", "Other"])
        interests = st.text_input("🧠 Your Interests (e.g., engineering, medicine, law, design)")
        location = st.text_input("📍 Preferred College Location (state/city or 'anywhere')")
        budget = st.text_input("💰 Budget for College (e.g., below 2L/year, 3-5L total)")
        goals = st.text_input("🎯 Career Goals (e.g., job, research, startup, civil services)")

        st.markdown("### 📊 Academic Performance")
        perc_10 = st.text_input("✔️ 10th Percentage (Required)", placeholder="e.g., 85.6")
        perc_11 = st.text_input("✔️ 11th Percentage (Required)", placeholder="e.g., 78.0")
        perc_12 = st.text_input("ℹ️ 12th Percentage (Optional)", placeholder="e.g., 82.5")

        submitted = st.form_submit_button("🚀 Generate My Career Path")

    if submitted:
        if not (stream and interests and location and budget and goals and perc_10 and perc_11):
            st.error("⚠️ Please fill in all required fields (10th and 11th percentages are mandatory).")
        else:
            with st.spinner("🔍 Analyzing your profile..."):
                output = generate_career_path(stream, interests, location, budget, goals, perc_10, perc_11, perc_12)
            st.success("✅ Career Roadmap Generated!")
            st.markdown("### 🧭 Your Personalized Career Path")
            st.markdown(output)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br><center><small>Made with ❤️ using Streamlit & Gemini</small></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

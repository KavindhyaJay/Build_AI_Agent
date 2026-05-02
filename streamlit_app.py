import streamlit as st
import time
from router import InterviewRouter
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import speech_to_text

# --- PREMIUM PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🕴️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    /* Premium Deep Black Background */
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    /* Bold Red Headers */
    h1, h2, h3 {
        color: #E50914; 
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Clean, elevated chat bubbles */
    .stChatMessage {
        background-color: #161616;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #2B2B2B;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
    }
    /* Luxury Sidebar */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 2px solid #E50914;
    }
    /* Red Accent for Metrics */
    [data-testid="stMetricValue"] {
        color: #E50914;
    }
</style>
""", unsafe_allow_html=True)

# --- VOICE ENGINE (Click to Play) ---
def generate_audio_bytes(text):
    """Converts text to speech and returns the raw audio bytes for the player."""
    try:
        sound_file = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(sound_file)
        return sound_file.getvalue()  # Return bytes so it can be saved in session state
    except Exception as e:
        st.error(f"Could not generate audio: {e}")
        return None

# --- FULL ROLE DATABASE ---
ROLE_DATABASE = {
    "Software Engineer": {"keywords": ["python", "java", "api", "oop", "system design", "algorithms"], "difficulty": "medium"},
    "Python Developer": {"keywords": ["django", "flask", "pandas", "asyncio", "generators", "pep8"], "difficulty": "medium"},
    "Data Analyst": {"keywords": ["sql", "excel", "pandas", "visualization", "power bi", "tableau"], "difficulty": "medium"},
    "Machine Learning Engineer": {"keywords": ["pytorch", "tensorflow", "rnn", "gradient", "deployment", "mlops"], "difficulty": "hard"},
    "Cyber Security Analyst": {"keywords": ["firewall", "penetration testing", "siem", "vulnerability", "encryption", "phishing"], "difficulty": "hard"},
    "Cloud Engineer": {"keywords": ["aws", "azure", "kubernetes", "docker", "ci/cd", "terraform"], "difficulty": "hard"},
    "Product Manager": {"keywords": ["agile", "roadmap", "stakeholder", "kpi", "user stories", "jira"], "difficulty": "medium"}
}

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "router" not in st.session_state:
    st.session_state.router = None
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False

# --- SIDEBAR: SETUP & PROGRESS ---
with st.sidebar:
    st.title("⚙️ Interview Setup")
    
    selected_role = st.selectbox("Select Target Role:", list(ROLE_DATABASE.keys()))
    
    if st.button("🚀 Start Interview", use_container_width=True, type="primary"):
        st.session_state.router = InterviewRouter(selected_role, ROLE_DATABASE[selected_role])
        st.session_state.messages = []
        st.session_state.interview_active = True
        
        # Get the first question & generate its audio
        first_step = st.session_state.router.next_step()
        audio_data = generate_audio_bytes(first_step["text"])
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": first_step["text"], 
            "type": "question",
            "audio": audio_data  # Save audio to message history
        })
        st.rerun()

    st.divider()
    if st.session_state.router:
        st.markdown(f"**Current Progress:** {st.session_state.router.question_count} / {st.session_state.router.max_questions}")
        st.progress(st.session_state.router.question_count / st.session_state.router.max_questions)

# --- MAIN CHAT INTERFACE ---
st.title("🕴️ AI Interview Coach")
st.markdown("Your personal AI hiring manager. Speak or type your answers to get real-time feedback.")

# Render previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display the audio player ONLY if audio exists for this message
        if msg.get("audio"):
            st.audio(msg["audio"], format="audio/mp3")
            
        # Render feedback blocks beautifully
        if msg.get("type") == "feedback":
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(label="Score", value=f"{msg['score']}/10")
            with col2:
                st.success(msg['brief_feedback'])
            with st.expander("🔍 View Detailed AI Feedback"):
                st.warning(f"**Missing Keywords/Points:** {msg['improvement_tips']}")
                st.info(f"**AI Analysis:** {msg['ai_feedback']}")

# --- HANDLE USER INPUT ---
if st.session_state.interview_active:
    
    st.markdown("---")
    st.write("🎙️ **Click to speak your answer:**")
    
    # FIX: Use a dynamic key based on the question count so the mic doesn't turn into a white box!
    current_q_num = st.session_state.router.question_count
    voice_answer = speech_to_text(
        language='en', 
        use_container_width=True, 
        just_once=True, 
        key=f'STT_Question_{current_q_num}'
    )
    
    # Text Input fallback
    text_answer = st.chat_input("Or type your interview answer here...")
    
    user_answer = text_answer or voice_answer
    
    if user_answer:
        st.session_state.messages.append({"role": "user", "content": user_answer})
        
        # Display the user's answer immediately before thinking
        with st.chat_message("user"):
            st.markdown(user_answer)
            
        with st.spinner("Analyzing your answer..."):
            analysis = st.session_state.router.next_step(user_answer)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Here is the feedback for your answer:", 
                "type": "feedback",
                "score": analysis["score"],
                "brief_feedback": analysis["brief_feedback"],
                "improvement_tips": analysis["improvement_tips"],
                "ai_feedback": analysis["ai_feedback"]
            })
            
            next_step = st.session_state.router.next_step()
            
            if next_step["type"] == "question":
                audio_data = generate_audio_bytes(next_step["text"])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": next_step["text"], 
                    "type": "question",
                    "audio": audio_data
                })
                
            elif next_step["type"] == "final_report":
                st.session_state.interview_active = False
                
                # Format bullet points without breaking Markdown
                strengths_list = "\n".join([f"- ✅ {s}" for s in next_step['strengths']]) if next_step['strengths'] else "- No clear strengths recorded yet."
                weaknesses_list = "\n".join([f"- 🎯 {w}" for w in next_step['weaknesses']]) if next_step['weaknesses'] else "- No clear weaknesses recorded."
                
                # Build the report completely flush left
                report_content = (
                    "### 🎉 Interview Complete!\n\n"
                    f"**Total Questions:** {next_step['total_questions']}\n\n"
                    "**Your Strengths:**\n"
                    f"{strengths_list}\n\n"
                    "**Areas to Improve:**\n"
                    f"{weaknesses_list}"
                )
                
                audio_data = generate_audio_bytes("Interview complete. Great job! Check your final report on the screen.")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": report_content, 
                    "type": "report",
                    "audio": audio_data
                })
        
        st.rerun()

elif not st.session_state.router:
    st.info("👈 Please select a role from the sidebar and click 'Start Interview' to begin.")
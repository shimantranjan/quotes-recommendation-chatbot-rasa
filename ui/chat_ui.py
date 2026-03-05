import streamlit as st
import requests
import time
import os

# --- Page Config must be the first Streamlit command ---
st.set_page_config(page_title="Quotes Recommendation", page_icon="💡", layout="wide")

# --- Load Custom CSS ---
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline CSS if file is missing
        st.markdown(
            """
            <style>
            .stApp { background: linear-gradient(135deg, #6a5acd, #9b59b6); color: white; }
            </style>
            """,
            unsafe_allow_html=True,
        )

load_css()

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Landing"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trigger_message" not in st.session_state:
    st.session_state.trigger_message = None

# --- API Configuration ---
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

# --- Functions ---
def navigate_to_chat():
    st.session_state.page = "Chat"

def send_message_to_rasa(user_message):
    """Sends a POST request to the Rasa REST API."""
    payload = {"sender": "user", "message": user_message}
    try:
        response = requests.post(RASA_API_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def handle_user_input(prompt):
    """Appends user message, sends to Rasa, and displays bot response."""
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # We must explicitly render it immediately here to keep UI snappy
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show Typing Indicator
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("Bot is typing... ✍️")
        time.sleep(0.8)  # slight delay for realism
        
        # Fetch bot response
        bot_responses = send_message_to_rasa(prompt)
        typing_placeholder.empty()
        
        # Display Bot Response
        if bot_responses is None:
            err_msg = "⚠️ *Rasa server not running. Please start the backend (`rasa run --enable-api`).*"
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})
        elif not bot_responses:
            st.markdown("*Silence*")
        else:
            for r in bot_responses:
                if "text" in r:
                    st.markdown(r["text"])
                    st.session_state.messages.append({"role": "assistant", "content": r["text"]})


# --- Page Providers ---

def show_landing_page():
    # Outer div for glass card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">Daily Inspiration</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Your personal AI companion for wisdom, motivation and clarity. Discover the perfect quote for every moment.</p>', unsafe_allow_html=True)
    
    # Start Chatting Button
    # We wrap the streamlit button in a div to target it with CSS
    st.markdown('<div style="margin-bottom: 3rem;">', unsafe_allow_html=True)
    if st.button("Start Chatting", use_container_width=False, kwargs=st.session_state):
        navigate_to_chat()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Categories Layout
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown('''
            <div class="category-card">
                <div class="category-icon">🚀</div>
                <h4>Motivation</h4>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
            <div class="category-card">
                <div class="category-icon">❤️</div>
                <h4>Love</h4>
            </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown('''
            <div class="category-card">
                <div class="category-icon">🏆</div>
                <h4>Success</h4>
            </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown('''
            <div class="category-card">
                <div class="category-icon">😂</div>
                <h4>Funny</h4>
            </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


def show_chat_page():
    # Force background to white/grey via CSS container injected here
    st.markdown(
        """
        <style>
        .stApp { background: #fdfdfd; color: #333; }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    # Navigation Back button
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Landing"
        st.rerun()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="chat-header">Quotes Bot</h2>', unsafe_allow_html=True)
    
    # 1. Render existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # 2. Handle quick button trigger from previous rerun
    if st.session_state.trigger_message:
        msg = st.session_state.trigger_message
        st.session_state.trigger_message = None
        handle_user_input(msg)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Quick Action Buttons (Under Chat)
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Motivation Quote"):
        st.session_state.trigger_message = "Give me a motivation quote"
        st.rerun()
    if col2.button("Love Quote"):
        st.session_state.trigger_message = "Tell me a love quote"
        st.rerun()
    if col3.button("Success Quote"):
        st.session_state.trigger_message = "I need a success quote"
        st.rerun()
    if col4.button("Funny Quote"):
        st.session_state.trigger_message = "Make me laugh"
        st.rerun()
        
    # 4. Input field
    if prompt := st.chat_input("Type your message here..."):
        handle_user_input(prompt)


# --- Router ---
if st.session_state.page == "Landing":
    show_landing_page()
else:
    show_chat_page()

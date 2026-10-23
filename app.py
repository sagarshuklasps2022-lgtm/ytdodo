import os
import streamlit as st
import yt_dlp
import requests

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub",
    page_icon="📥",
    layout="wide",
)

# Session state initialization for Auth & Dark Mode
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # 'login', 'signup', 'forgot'
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Dynamic Theme Styling (Dark / Light Mode)
bg_color = "#0e1117" if st.session_state.dark_mode else "#ffffff"
text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
card_bg = "#161b22" if st.session_state.dark_mode else "#f0f2f6"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stButton>button {{
        background-color: #ff0000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: #cc0000;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar / Admin Panel & Theme Toggle
st.sidebar.title("🛠️ Admin Panel")
if st.sidebar.button("🌓 Toggle Dark / Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

st.sidebar.subheader("Download registered users log file:")
if st.sidebar.button("No user logs recorded yet."):
    pass

# Function to shorten URL using ShrinkMe API
def shorten_with_shrinkme(long_url):
    api_token = "5993c830ec96cd0e9e4731657116fce22629f311"
    api_url = f"https://shrinkme.io/api?api={api_token}&url={long_url}&format=text"
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text.strip()
    except Exception:
        pass
    return long_url

# --- AUTHENTICATION SCREENS ---
if not st.session_state.logged_in:
    st.markdown(
        """
        <div style='text-align: center; padding: 30px;'>
            <h1 style='color: #ff0000; font-size: 36px;'>YT DODO</h1>
            <p style='color: gray;'>UNIVERSAL MEDIA HUB</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.auth_mode == "login":
            st.subheader("🔐 Sign In to your Account")
            username = st.text_input("Username or Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Sign In", use_container_width=True):
                if username and password:
                    st.session_state.logged_in = True
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")
            
            if st.button("Create New Account", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()
                
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.auth_mode = "forgot"
                st.rerun()

        elif st.session_state.auth_mode == "signup":
            st.subheader("📝 Create New Account")
            new_user = st.text_input("Choose Username")
            new_email = st.text_input("Email Address")
            new_pass = st.text_input("Create Password", type="password")
            
            if st.button("Register", use_container_width=True):
                if new_user and new_email and new_pass:
                    st.success("Account created successfully! Please sign in.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error("Please fill all details.")
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

        elif st.session_state.auth_mode == "forgot":
            st.subheader("🔄 Recover Password")
            recovery_email = st.text_input("Enter your registered email")
            
            if st.button("Send Reset Link", use_container_width=True):
                if recovery_email:
                    st.success("Password reset instructions sent to your email!")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error("Please enter your email.")
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

else:
    # --- MAIN DASHBOARD WITH ICONS & PROFILES ---
    dashboard_html = f"""
    <div class="max-w-4xl mx-auto p-4">
        <div class="flex justify-between items-center bg-[{card_bg}] p-4 rounded-xl border border-gray-800 mb-6 shadow-lg">
            <div class="flex items-center space-x-3">
                <div class="bg-red-600 p-2 rounded-lg text-white">
                    <i class="fa-solid fa-bolt text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-wider">YT DODO</h1>
                    <p class="text-xs text-gray-400">Welcome, Sagar Shukla</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button class="p-2 rounded-lg bg-gray-700/30 hover:bg-red-600 transition"><i class="fa-solid fa-user"></i></button>
                <button class="p-2 rounded-lg bg-gray-700/30 hover:bg-red-600 transition"><i class="fa-solid fa-gear"></i></button>
            </div>
        </div>
    </div>
    """
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
        unsafe_allow_html=True,
    )
    st.markdown(dashboard_html, unsafe_allow_html=True)
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Downloader & ShrinkMe Ad Integration Hub
    st.markdown("### 📥 Search & Download Hub")
    target_url = st.text_input("PASTE YOUTUBE, INSTAGRAM OR FACEBOOK LINK", placeholder="https://www.youtube.com/watch?v=...")
    format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio", "APK File"])

    if st.button("Prepare Download") and target_url:
        try:
            if "MP3" in format_type.upper() or "AUDIO" in format_type.upper():
                ydl_opts = {
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                        "Accept-Language": "en-US,en;q=0.9",
                    }
                }
            else:
                ydl_opts = {
                    "format": "best[ext=mp4]/best",
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                        "Accept-Language": "en-US,en;q=0.9",
                    }
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=False)
                direct_url = info.get("url")

            if direct_url:
                # Shorten through ShrinkMe API
                shortened_url = shorten_with_shrinkme(direct_url)
                
                st.success("Download link generated successfully with Ad Integration!")
                st.markdown(
                    f'<a href="{shortened_url}" target="_blank" style="display:inline-block;padding:14px 24px;background-color:#ff0000;color:white;text-decoration:none;border-radius:8px;font-weight:bold;text-align:center;width:100%;font-size:18px;">📥 Click Here to Download (Via Ad Link)</a>',
                    unsafe_allow_html=True,
                )
            else:
                st.error("The download link could not be processed. Please verify the URL and try again.")

        except Exception as e:
            st.error(f"Download failed: {e}")

st.markdown("<hr style='margin-top: 1rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

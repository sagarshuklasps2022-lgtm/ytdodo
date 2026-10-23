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
                # Optimized for best available single-file FHD without needing local ffmpeg
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

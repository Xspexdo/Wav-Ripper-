"""
WAV Media Ripper // Dark Minimal Gaming HUD (Edition 2.4)
Theme: #0a0a0c, Frameless Window, Rounded Corners, Custom WAV Brand Logo
Formats: WAV, MP3, MP4, BEST VIDEO
Features:
  - Multi-level Profile / Quality Stepper ([-] and [+] buttons for bitrate, sample rate, bit depth, resolution)
  - Multi-format download (Audio & Video)
  - History Catalog & Purge
  - Windows + V Clipboard Paste support (all keyboard languages)
Strictly NO EMOJIS.
"""

import os
import sys
import re
import json
import shutil
import threading
import subprocess
import traceback
from datetime import datetime
import tkinter as tk
import tkinter.messagebox as mb
from PIL import Image
import customtkinter as ctk

# Directory and Assets paths
if getattr(sys, "frozen", False):
    BUNDLE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    APP_DIR = os.path.dirname(sys.executable)
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = BUNDLE_DIR

BASE_DIR = APP_DIR
LOGO_PNG = os.path.join(BUNDLE_DIR, "logo_rounded.png")
LOGO_ICO = os.path.join(BUNDLE_DIR, "logo.ico")
HISTORY_FILE = os.path.join(APP_DIR, "history.json")

# Safe stream redirection for windowless pythonw execution
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")


def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        return
    log_path = os.path.join(BASE_DIR, "crash.log")
    err_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(err_text)
    except Exception:
        pass
    try:
        mb.showerror(
            "RIPPER // CRITICAL ERROR",
            f"Engine encountered an error:\n\n{err_text[:300]}...\n\nDetails saved to crash.log",
        )
    except Exception:
        pass


sys.excepthook = global_exception_handler

# Appearance Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Theme Palette: Deep Minimal Gaming HUD / Stealth Overlay
BG_MAIN = "#0a0a0c"
BG_CARD = "#11131a"
BG_INPUT = "#08090e"
BORDER_CARD = "#1d2130"

ACCENT_CYAN = "#00f0ff"
ACCENT_CYAN_HOVER = "#38bdf8"
ACCENT_RED = "#ff3366"
ACCENT_RED_HOVER = "#e11d48"
ACCENT_GREEN = "#10b981"
ACCENT_GRAY = "#1f2436"

TEXT_WHITE = "#f8fafc"
TEXT_SECONDARY = "#cbd5e1"
TEXT_MUTED = "#64748b"
TEXT_CYAN = "#38bdf8"

# Format presets with multi-level quality / bitrate / resolution adjustments
FORMAT_CONFIG = {
    "WAV": {
        "badge": "WAV",
        "type": "audio",
        "default_level": 0,
        "levels": [
            {
                "tag": "16b/44k",
                "label": "PROFILE: 16-BIT / 44.1kHz UNCOMPRESSED PCM (1411kbps) [CD STD]",
                "short": "16-BIT / 44.1kHz",
                "btn_tag": "WAV 16-BIT",
                "args": ["-x", "--audio-format", "wav", "--postprocessor-args", "ExtractAudio:-c:a pcm_s16le -ar 44100"],
            },
            {
                "tag": "24b/48k",
                "label": "PROFILE: 24-BIT / 48.0kHz PCM (2304kbps) [STUDIO MASTER]",
                "short": "24-BIT / 48kHz",
                "btn_tag": "WAV 24-BIT/48k",
                "args": ["-x", "--audio-format", "wav", "--postprocessor-args", "ExtractAudio:-c:a pcm_s24le -ar 48000"],
            },
            {
                "tag": "24b/96k",
                "label": "PROFILE: 24-BIT / 96.0kHz PCM (4608kbps) [HI-RES AUDIO]",
                "short": "24-BIT / 96kHz",
                "btn_tag": "WAV 24-BIT/96k",
                "args": ["-x", "--audio-format", "wav", "--postprocessor-args", "ExtractAudio:-c:a pcm_s24le -ar 96000"],
            },
            {
                "tag": "32b/192k",
                "label": "PROFILE: 32-BIT / 192kHz PCM (12288kbps) [AUDIOPHILE FLOAT]",
                "short": "32-BIT / 192kHz",
                "btn_tag": "WAV 32-BIT/192k",
                "args": ["-x", "--audio-format", "wav", "--postprocessor-args", "ExtractAudio:-c:a pcm_s32le -ar 192000"],
            },
        ],
    },
    "MP3": {
        "badge": "MP3",
        "type": "audio",
        "default_level": 3,
        "levels": [
            {
                "tag": "128k",
                "label": "PROFILE: 128kbps CBR STEREO [ECONOMY / COMPACT]",
                "short": "128kbps CBR",
                "btn_tag": "MP3 128kbps",
                "args": ["-x", "--audio-format", "mp3", "--postprocessor-args", "ExtractAudio:-b:a 128k"],
            },
            {
                "tag": "192k",
                "label": "PROFILE: 192kbps CBR STEREO [STANDARD QUALITY]",
                "short": "192kbps CBR",
                "btn_tag": "MP3 192kbps",
                "args": ["-x", "--audio-format", "mp3", "--postprocessor-args", "ExtractAudio:-b:a 192k"],
            },
            {
                "tag": "256k",
                "label": "PROFILE: 256kbps CBR STEREO [HIGH FIDELITY]",
                "short": "256kbps CBR",
                "btn_tag": "MP3 256kbps",
                "args": ["-x", "--audio-format", "mp3", "--postprocessor-args", "ExtractAudio:-b:a 256k"],
            },
            {
                "tag": "320k",
                "label": "PROFILE: 320kbps CBR STEREO [MAXIMUM MP3 QUALITY]",
                "short": "320kbps CBR",
                "btn_tag": "MP3 320kbps",
                "args": ["-x", "--audio-format", "mp3", "--postprocessor-args", "ExtractAudio:-b:a 320k"],
            },
        ],
    },
    "MP4": {
        "badge": "MP4",
        "type": "video",
        "default_level": 2,
        "levels": [
            {
                "tag": "480p",
                "label": "PROFILE: 480p SD RESOLUTION (H.264 + AAC MP4)",
                "short": "480p SD",
                "btn_tag": "MP4 480p",
                "args": ["-f", "bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480][ext=mp4]/bv*[height<=480]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "720p",
                "label": "PROFILE: 720p HD RESOLUTION (H.264 + AAC MP4)",
                "short": "720p HD",
                "btn_tag": "MP4 720p",
                "args": ["-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/bv*[height<=720]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "1080p",
                "label": "PROFILE: 1080p FULL HD RESOLUTION (H.264 + AAC MP4)",
                "short": "1080p FHD",
                "btn_tag": "MP4 1080p",
                "args": ["-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]/bv*[height<=1080]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "1440p",
                "label": "PROFILE: 1440p / 2K QUAD HD RESOLUTION (H.264 + AAC MP4)",
                "short": "1440p 2K",
                "btn_tag": "MP4 2K",
                "args": ["-f", "bv*[height<=1440][ext=mp4]+ba[ext=m4a]/b[height<=1440][ext=mp4]/bv*[height<=1440]+ba/b", "--merge-output-format", "mp4"],
            },
        ],
    },
    "BEST VIDEO": {
        "badge": "BEST",
        "type": "video",
        "default_level": 3,
        "levels": [
            {
                "tag": "720p",
                "label": "PROFILE: 720p HD MAXIMUM BITRATE STREAM",
                "short": "720p Max",
                "btn_tag": "VIDEO 720p",
                "args": ["-f", "bv*[height<=720]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "1080p",
                "label": "PROFILE: 1080p FULL HD MAXIMUM BITRATE STREAM",
                "short": "1080p Max",
                "btn_tag": "VIDEO 1080p",
                "args": ["-f", "bv*[height<=1080]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "1440p",
                "label": "PROFILE: 1440p / 2K QUAD HD STREAM",
                "short": "1440p 2K",
                "btn_tag": "VIDEO 2K",
                "args": ["-f", "bv*[height<=1440]+ba/b", "--merge-output-format", "mp4"],
            },
            {
                "tag": "MAX 4K",
                "label": "PROFILE: 4K / 2160p / SOURCE MAXIMUM RESOLUTION",
                "short": "4K Max",
                "btn_tag": "BEST VIDEO [4K/MAX]",
                "args": ["-f", "bv*+ba/b", "--merge-output-format", "mp4"],
            },
        ],
    },
}


def load_history():
    """Load extraction history from local JSON file."""
    if not os.path.isfile(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_history(items):
    """Save extraction history to local JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def find_yt_dlp():
    """Locate yt-dlp binary on PATH, local directory, or WinGet packages directory."""
    path = shutil.which("yt-dlp")
    if path:
        return path

    # Local bundled binary
    local_bin = os.path.join(BASE_DIR, "yt-dlp.exe")
    if os.path.isfile(local_bin):
        return local_bin

    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        import glob
        matches = glob.glob(
            os.path.join(local_appdata, r"Microsoft\WinGet\Packages\*yt-dlp*\**\yt-dlp.exe"),
            recursive=True,
        )
        if matches:
            return matches[0]

    return "yt-dlp"


def find_ffmpeg_dir():
    """Locate ffmpeg binary directory on PATH, local directory, or WinGet packages directory."""
    path = shutil.which("ffmpeg")
    if path:
        return os.path.dirname(path)

    # Local bundled ffmpeg
    for sub in [("ffmpeg", "bin"), ("bin",), ()]:
        candidate = os.path.join(BASE_DIR, *sub)
        if os.path.isfile(os.path.join(candidate, "ffmpeg.exe")):
            return candidate

    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        import glob
        matches = glob.glob(
            os.path.join(local_appdata, r"Microsoft\WinGet\Packages\*ffmpeg*\**\bin"),
            recursive=True,
        )
        for match in matches:
            if os.path.isfile(os.path.join(match, "ffmpeg.exe")):
                return match

    return None


class MediaRipperApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_MAIN)

        self.title("WAV // MEDIA RIPPER")
        self.resizable(False, False)

        # Set Window Taskbar Icon
        if os.path.isfile(LOGO_ICO):
            try:
                self.iconbitmap(LOGO_ICO)
            except Exception:
                pass

        # State variables
        self.is_downloading = False
        self.process = None
        self.yt_dlp_bin = find_yt_dlp()
        self.ffmpeg_dir = find_ffmpeg_dir()

        default_dl = os.path.normpath(os.path.expanduser("~/Downloads"))
        self.download_dir_var = tk.StringVar(value=default_dl)
        self.url_var = tk.StringVar()
        self.selected_format = "WAV"
        self.selected_levels = {
            "WAV": FORMAT_CONFIG["WAV"]["default_level"],
            "MP3": FORMAT_CONFIG["MP3"]["default_level"],
            "MP4": FORMAT_CONFIG["MP4"]["default_level"],
            "BEST VIDEO": FORMAT_CONFIG["BEST VIDEO"]["default_level"],
        }

        self.format_desc_var = tk.StringVar()
        self.status_var = tk.StringVar(value="STATUS // READY FOR STREAM")
        self.telemetry_var = tk.StringVar(value="SPEED: -- MB/s  |  ETA: --:--")

        self.format_buttons = {}
        self.history_items = load_history()
        self.current_tab = "ripper"
        self._last_download_title = ""
        self._is_minimized = False

        # Build Minimal HUD UI Components
        self.build_ui()

        # Initialize quality display
        self._update_quality_display()

        # Frameless Window & DPI Centering Setup
        self.setup_frameless(690, 536)

    def setup_frameless(self, width, height):
        self.update_idletasks()
        try:
            scaling = self._get_window_scaling()
        except Exception:
            scaling = 1.0

        actual_w = round(width * scaling)
        actual_h = round(height * scaling)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = max(0, int((screen_w - actual_w) / 2))
        y = max(0, int((screen_h - actual_h) / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.overrideredirect(True)
        self.lift()
        self.focus_force()

        self.bind("<FocusIn>", self._on_focus_in)

    def _on_focus_in(self, event):
        if getattr(self, "_is_minimized", False) and self.state() == "normal":
            self._is_minimized = False
            self.overrideredirect(True)
            self.lift()

    def minimize_window(self):
        self._is_minimized = True
        self.overrideredirect(False)
        self.iconify()

    def close_window(self):
        if self.is_downloading and self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
        self.destroy()

    def start_window_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_window_drag(self, event):
        if hasattr(self, "_drag_start_x"):
            deltax = event.x - self._drag_start_x
            deltay = event.y - self._drag_start_y
            new_x = self.winfo_x() + deltax
            new_y = self.winfo_y() + deltay
            self.geometry(f"+{new_x}+{new_y}")

    def get_current_level_cfg(self):
        fmt = self.selected_format
        cfg = FORMAT_CONFIG.get(fmt, FORMAT_CONFIG["WAV"])
        levels = cfg["levels"]
        idx = self.selected_levels.get(fmt, cfg.get("default_level", 0))
        idx = max(0, min(len(levels) - 1, idx))
        return levels[idx]

    def select_format(self, fmt):
        self.selected_format = fmt

        # Update button visual states
        for name, btn in self.format_buttons.items():
            if name == fmt:
                btn.configure(
                    fg_color=ACCENT_CYAN,
                    hover_color=ACCENT_CYAN_HOVER,
                    text_color="#0a0a0c",
                    border_width=0,
                )
            else:
                btn.configure(
                    fg_color="#141724",
                    hover_color="#1d2235",
                    text_color="#cbd5e1",
                    border_color="#2b3149",
                    border_width=1,
                )

        self._update_quality_display()

    def adjust_quality_level(self, delta):
        fmt = self.selected_format
        cfg = FORMAT_CONFIG.get(fmt, FORMAT_CONFIG["WAV"])
        levels = cfg["levels"]
        curr = self.selected_levels.get(fmt, cfg.get("default_level", 0))
        new_val = max(0, min(len(levels) - 1, curr + delta))
        if new_val != curr:
            self.selected_levels[fmt] = new_val
            self._update_quality_display()

    def _update_quality_display(self):
        fmt = self.selected_format
        cfg = FORMAT_CONFIG.get(fmt, FORMAT_CONFIG["WAV"])
        levels = cfg["levels"]
        idx = self.selected_levels.get(fmt, cfg.get("default_level", 0))
        idx = max(0, min(len(levels) - 1, idx))
        lvl_cfg = levels[idx]

        self.format_desc_var.set(lvl_cfg["label"])

        if hasattr(self, "quality_tag_lbl"):
            self.quality_tag_lbl.configure(text=f"[ {lvl_cfg['tag']} ]")

        if hasattr(self, "btn_quality_dec"):
            self.btn_quality_dec.configure(
                state="disabled" if idx == 0 else "normal",
                text_color=TEXT_MUTED if idx == 0 else ACCENT_CYAN,
            )
        if hasattr(self, "btn_quality_inc"):
            self.btn_quality_inc.configure(
                state="disabled" if idx == len(levels) - 1 else "normal",
                text_color=TEXT_MUTED if idx == len(levels) - 1 else ACCENT_CYAN,
            )

        if hasattr(self, "execute_btn") and not self.is_downloading:
            action_word = "DOWNLOAD" if cfg["type"] == "video" else "EXTRACTION"
            self.execute_btn.configure(text=f">>> START {action_word} [{lvl_cfg['btn_tag']}] <<<")

    # ---------------- UI Construction ---------------- #

    def build_ui(self):
        # Outer High-Tech Shell Bezel
        self.outer_frame = ctk.CTkFrame(
            self,
            fg_color=BG_MAIN,
            border_color=BORDER_CARD,
            border_width=1,
            corner_radius=14,
        )
        self.outer_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # 1. Custom Title Bar with Brand Logo
        self.build_titlebar()

        # 2. Sleek HUD Navigation Switcher (Ripper vs History)
        self.build_nav_bar()

        # 3. High-Tech Cyber Footer & Developer Credit (CR: xspexdo)
        self.build_footer()

        # 4. Main Body Container
        self.body_container = ctk.CTkFrame(self.outer_frame, fg_color="transparent")
        self.body_container.pack(fill="both", expand=True, padx=16, pady=(6, 8))

        # View Frames
        self.ripper_frame = ctk.CTkFrame(self.body_container, fg_color="transparent")
        self.history_frame = ctk.CTkFrame(self.body_container, fg_color="transparent")

        # Build Ripper HUD Components
        self.build_url_card(self.ripper_frame)
        self.build_settings_card(self.ripper_frame)
        self.build_progress_card(self.ripper_frame)

        # Build History Catalog View
        self.build_history_view(self.history_frame)

        # Default to Ripper View
        self.show_ripper_tab()

    def build_footer(self):
        self.footer_frame = ctk.CTkFrame(self.outer_frame, fg_color="transparent", height=24)
        self.footer_frame.pack(side="bottom", fill="x", padx=16, pady=(0, 10))
        self.footer_frame.pack_propagate(False)

        # Left tag: System engine & status
        engine_lbl = ctk.CTkLabel(
            self.footer_frame,
            text="// ENGINE: YT-DLP + FFMPEG HI-RES",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color="#334155",
        )
        engine_lbl.pack(side="left")

        # Right tag: Glowing High-Tech Developer Credit (CR: xspexdo)
        self.cr_btn = ctk.CTkButton(
            self.footer_frame,
            text="// CR: xspexdo",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#0e1724",
            hover_color="#16273d",
            border_color="#1e3452",
            border_width=1,
            text_color=ACCENT_CYAN,
            height=24,
            corner_radius=6,
            command=self._open_author_link,
        )
        self.cr_btn.pack(side="right")

    def _open_author_link(self):
        import webbrowser
        try:
            webbrowser.open_new_tab("https://github.com/xspexdo")
        except Exception:
            pass

    def build_titlebar(self):
        # Top Neon Accent Line
        top_accent = ctk.CTkFrame(
            self.outer_frame,
            fg_color=ACCENT_CYAN,
            height=2,
            corner_radius=0,
        )
        top_accent.pack(fill="x", side="top")

        self.titlebar_frame = ctk.CTkFrame(
            self.outer_frame,
            fg_color="#0e1017",
            height=42,
            corner_radius=0,
        )
        self.titlebar_frame.pack(fill="x", side="top")
        self.titlebar_frame.pack_propagate(False)

        self.titlebar_frame.bind("<Button-1>", self.start_window_drag)
        self.titlebar_frame.bind("<B1-Motion>", self.do_window_drag)

        # Left branding (Logo + Typography)
        brand_frame = ctk.CTkFrame(self.titlebar_frame, fg_color="transparent")
        brand_frame.pack(side="left", padx=(12, 0), fill="y")
        brand_frame.bind("<Button-1>", self.start_window_drag)

        if os.path.isfile(LOGO_PNG):
            try:
                pil_logo = Image.open(LOGO_PNG)
                self.logo_ctk = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(28, 28))
                logo_lbl = ctk.CTkLabel(brand_frame, text="", image=self.logo_ctk)
                logo_lbl.pack(side="left", padx=(0, 8))
                logo_lbl.bind("<Button-1>", self.start_window_drag)
            except Exception:
                pass

        title_lbl = ctk.CTkLabel(
            brand_frame,
            text="WAV RIPPER",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=TEXT_WHITE,
        )
        title_lbl.pack(side="left", padx=(0, 10))
        title_lbl.bind("<Button-1>", self.start_window_drag)

        tag_badge = ctk.CTkLabel(
            brand_frame,
            text="HUD v2.4",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_CYAN,
            fg_color="#121824",
            corner_radius=6,
            padx=8,
            pady=2,
        )
        tag_badge.pack(side="left")
        tag_badge.bind("<Button-1>", self.start_window_drag)

        # Right window control buttons
        controls_frame = ctk.CTkFrame(self.titlebar_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=(0, 8), fill="y")

        min_btn = ctk.CTkButton(
            controls_frame,
            text="_",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="transparent",
            hover_color=ACCENT_GRAY,
            text_color=TEXT_SECONDARY,
            width=36,
            height=28,
            corner_radius=8,
            command=self.minimize_window,
        )
        min_btn.pack(side="left", padx=(0, 4), pady=7)

        close_btn = ctk.CTkButton(
            controls_frame,
            text="X",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color="transparent",
            hover_color=ACCENT_RED,
            text_color=TEXT_SECONDARY,
            width=36,
            height=28,
            corner_radius=8,
            command=self.close_window,
        )
        close_btn.pack(side="left", pady=7)

    def build_nav_bar(self):
        nav_frame = ctk.CTkFrame(self.outer_frame, fg_color="#0e1017", height=36, corner_radius=0)
        nav_frame.pack(fill="x", side="top")
        nav_frame.pack_propagate(False)

        # Tab button container
        tabs_box = ctk.CTkFrame(nav_frame, fg_color="transparent")
        tabs_box.pack(side="left", padx=12, fill="y")

        self.btn_nav_ripper = ctk.CTkButton(
            tabs_box,
            text="// RIPPER HUD",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            width=124,
            height=26,
            corner_radius=6,
            command=self.show_ripper_tab,
        )
        self.btn_nav_ripper.pack(side="left", padx=(0, 6), pady=5)

        hist_count = len(self.history_items)
        self.btn_nav_history = ctk.CTkButton(
            tabs_box,
            text=f"// HISTORY [ {hist_count} ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            width=134,
            height=26,
            corner_radius=6,
            command=self.show_history_tab,
        )
        self.btn_nav_history.pack(side="left", pady=5)

        # Actions on right side of nav bar
        self.nav_actions_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        self.nav_actions_frame.pack(side="right", padx=12, fill="y")

        # Clear History Button (shown when in history tab)
        self.btn_clear_history = ctk.CTkButton(
            self.nav_actions_frame,
            text="[ CLEAR HISTORY ]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#1c1114",
            hover_color="#2b1419",
            border_color="#541a23",
            border_width=1,
            text_color=ACCENT_RED,
            width=120,
            height=26,
            corner_radius=6,
            command=self.clear_history,
        )

    def show_ripper_tab(self):
        self.current_tab = "ripper"
        self.btn_nav_ripper.configure(
            fg_color="#181c28",
            hover_color="#222838",
            text_color=ACCENT_CYAN,
            border_color="#2a334a",
            border_width=1,
        )
        self.btn_nav_history.configure(
            fg_color="transparent",
            hover_color="#141724",
            text_color=TEXT_MUTED,
            border_width=0,
        )
        self.btn_clear_history.pack_forget()

        self.history_frame.pack_forget()
        self.ripper_frame.pack(fill="both", expand=True)

    def show_history_tab(self):
        self.current_tab = "history"
        self.btn_nav_history.configure(
            fg_color="#181c28",
            hover_color="#222838",
            text_color=ACCENT_CYAN,
            border_color="#2a334a",
            border_width=1,
        )
        self.btn_nav_ripper.configure(
            fg_color="transparent",
            hover_color="#141724",
            text_color=TEXT_MUTED,
            border_width=0,
        )
        self.btn_clear_history.pack(side="right", pady=5)

        self.ripper_frame.pack_forget()
        self.history_frame.pack(fill="both", expand=True)
        self.render_history_items()

    def build_url_card(self, parent):
        header = ctk.CTkLabel(
            parent,
            text="// TARGET STREAM URL",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        header.pack(anchor="w", pady=(0, 4))

        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_color=BORDER_CARD,
            border_width=1,
            corner_radius=10,
        )
        card.pack(fill="x", pady=(0, 10))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=8)

        self.url_entry = ctk.CTkEntry(
            row,
            textvariable=self.url_var,
            font=ctk.CTkFont(family="Consolas", size=11),
            placeholder_text="Paste video or audio link (YouTube, SoundCloud, TikTok, Bilibili...)",
            placeholder_text_color=TEXT_MUTED,
            fg_color=BG_INPUT,
            border_color="#242838",
            border_width=1,
            text_color=TEXT_WHITE,
            corner_radius=8,
            height=36,
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.url_entry.bind("<Return>", lambda e: self.start_extraction())

        # Full Windows + V & cross-language keyboard paste support (KeyCode 86 = V)
        self.url_entry.bind(
            "<Control-KeyPress>",
            lambda e: self._on_paste_event() if getattr(e, "keycode", 0) == 86 else None,
        )
        self.url_entry.bind("<<Paste>>", self._on_paste_event)
        self.url_entry.bind("<Control-v>", self._on_paste_event)
        self.url_entry.bind("<Control-V>", self._on_paste_event)

        # Global window paste fallback (catches paste when window is focused via Win+V)
        self.bind(
            "<Control-KeyPress>",
            lambda e: self._on_paste_event() if getattr(e, "keycode", 0) == 86 else None,
        )
        self.bind("<<Paste>>", lambda e: self._on_paste_event())

        # Dark HUD Right-click Context Menu
        self.setup_entry_context_menu(self.url_entry)

        paste_btn = ctk.CTkButton(
            row,
            text="[PASTE]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=TEXT_CYAN,
            width=76,
            height=36,
            corner_radius=8,
            command=self.paste_clipboard,
        )
        paste_btn.pack(side="left", padx=(0, 6))

        clear_btn = ctk.CTkButton(
            row,
            text="[CLEAR]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=TEXT_MUTED,
            width=76,
            height=36,
            corner_radius=8,
            command=lambda: self.url_var.set(""),
        )
        clear_btn.pack(side="left")

    def build_settings_card(self, parent):
        header = ctk.CTkLabel(
            parent,
            text="// FORMAT SELECTION & DESTINATION",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        header.pack(anchor="w", pady=(0, 4))

        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_color=BORDER_CARD,
            border_width=1,
            corner_radius=10,
        )
        card.pack(fill="x", pady=(0, 10))

        # Row 1: Format Selector Pills
        row1 = ctk.CTkFrame(card, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=(8, 4))

        fmt_lbl = ctk.CTkLabel(
            row1,
            text="FORMAT:",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        fmt_lbl.pack(side="left")

        # Sleek format pill buttons with clean high-contrast text
        pills_frame = ctk.CTkFrame(row1, fg_color="transparent")
        pills_frame.pack(side="left")

        formats = ["WAV", "MP3", "MP4", "BEST VIDEO"]
        for fmt in formats:
            btn = ctk.CTkButton(
                pills_frame,
                text=fmt,
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                width=88 if fmt != "BEST VIDEO" else 104,
                height=32,
                corner_radius=8,
                command=lambda f=fmt: self.select_format(f),
            )
            btn.pack(side="left", padx=(0, 6))
            self.format_buttons[fmt] = btn

        # Initialize buttons style
        self.select_format("WAV")

        # Row 2: Interactive Quality Stepper & Profile description
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=(0, 6))

        q_lbl = ctk.CTkLabel(
            row2,
            text="QUALITY:",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        q_lbl.pack(side="left")

        # [-] Decrease Quality Button
        self.btn_quality_dec = ctk.CTkButton(
            row2,
            text="[ - ]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            width=30,
            height=26,
            corner_radius=6,
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=ACCENT_CYAN,
            command=lambda: self.adjust_quality_level(-1),
        )
        self.btn_quality_dec.pack(side="left", padx=(0, 4))

        # [+] Increase Quality Button
        self.btn_quality_inc = ctk.CTkButton(
            row2,
            text="[ + ]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            width=30,
            height=26,
            corner_radius=6,
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=ACCENT_CYAN,
            command=lambda: self.adjust_quality_level(1),
        )
        self.btn_quality_inc.pack(side="left", padx=(0, 8))

        # Tag Badge (e.g. [ 16b/44k ], [ 24b/96k ], [ 320k ])
        self.quality_tag_lbl = ctk.CTkLabel(
            row2,
            text="[ 16b/44k ]",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color=ACCENT_CYAN,
            fg_color="#0e232e",
            corner_radius=4,
            padx=6,
            pady=2,
        )
        self.quality_tag_lbl.pack(side="left", padx=(0, 8))
        self.quality_tag_lbl.bind("<Button-1>", lambda e: self.adjust_quality_level(1))

        # Profile description line
        self.spec_lbl = ctk.CTkLabel(
            row2,
            textvariable=self.format_desc_var,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_CYAN,
            anchor="w",
            cursor="hand2",
        )
        self.spec_lbl.pack(side="left", fill="x", expand=True)
        self.spec_lbl.bind("<Button-1>", lambda e: self.adjust_quality_level(1))

        # Row 3: Destination Folder
        row3 = ctk.CTkFrame(card, fg_color="transparent")
        row3.pack(fill="x", padx=10, pady=(0, 8))

        dest_lbl = ctk.CTkLabel(
            row3,
            text="SAVE TO:",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        dest_lbl.pack(side="left")

        dest_entry = ctk.CTkEntry(
            row3,
            textvariable=self.download_dir_var,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=BG_INPUT,
            border_color="#202330",
            border_width=1,
            text_color=TEXT_SECONDARY,
            corner_radius=8,
            height=32,
        )
        dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ctk.CTkButton(
            row3,
            text="[BROWSE]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=TEXT_SECONDARY,
            width=76,
            height=32,
            corner_radius=8,
            command=self.browse_destination,
        )
        browse_btn.pack(side="left", padx=(0, 6))

        open_btn = ctk.CTkButton(
            row3,
            text="[OPEN DIR]",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#151926",
            hover_color="#1f2538",
            border_color="#2e354d",
            border_width=1,
            text_color=TEXT_CYAN,
            width=78,
            height=32,
            corner_radius=8,
            command=self.open_destination,
        )
        open_btn.pack(side="left")

    def build_progress_card(self, parent):
        # Big Execute & Abort Button Bar
        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 8))

        self.execute_btn = ctk.CTkButton(
            btn_row,
            text=">>> START EXTRACTION [WAV 16-BIT] <<<",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            fg_color=ACCENT_CYAN,
            hover_color=ACCENT_CYAN_HOVER,
            text_color="#060709",
            height=44,
            corner_radius=10,
            command=self.start_extraction,
        )
        self.execute_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.abort_btn = ctk.CTkButton(
            btn_row,
            text="[ABORT]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#1c1114",
            hover_color="#2b1419",
            border_color="#541a23",
            border_width=1,
            text_color=ACCENT_RED,
            height=44,
            width=84,
            corner_radius=10,
            state="disabled",
            command=self.abort_process,
        )
        self.abort_btn.pack(side="left")

        # Telemetry Card
        telemetry_card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_color=BORDER_CARD,
            border_width=1,
            corner_radius=10,
        )
        telemetry_card.pack(fill="x")

        stat_row = ctk.CTkFrame(telemetry_card, fg_color="transparent")
        stat_row.pack(fill="x", padx=12, pady=(8, 4))

        self.status_display = ctk.CTkLabel(
            stat_row,
            textvariable=self.status_var,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=TEXT_CYAN,
        )
        self.status_display.pack(side="left")

        self.telemetry_display = ctk.CTkLabel(
            stat_row,
            textvariable=self.telemetry_var,
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_MUTED,
        )
        self.telemetry_display.pack(side="right")

        # Clean Progress Bar: initially matches background color to avoid weird floating dot
        self.progress_bar = ctk.CTkProgressBar(
            telemetry_card,
            height=8,
            corner_radius=4,
            fg_color="#141724",
            progress_color="#141724",
        )
        self.progress_bar.pack(fill="x", padx=12, pady=(0, 10))
        self.progress_bar.set(0.0)

    # ---------------- History View Construction ---------------- #

    def build_history_view(self, parent):
        summary_row = ctk.CTkFrame(parent, fg_color="transparent")
        summary_row.pack(fill="x", pady=(0, 6))

        count = len(self.history_items)
        self.history_total_lbl = ctk.CTkLabel(
            summary_row,
            text=f"TOTAL EXTRACTED: {count} ITEMS",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        self.history_total_lbl.pack(side="left")

        sub_lbl = ctk.CTkLabel(
            summary_row,
            text="PERSISTENT DOWNLOAD CATALOG",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_MUTED,
        )
        sub_lbl.pack(side="right")

        # Scrollable area for history items
        self.history_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="#0a0a0d",
            border_color=BORDER_CARD,
            border_width=1,
            corner_radius=10,
        )
        self.history_scroll.pack(fill="both", expand=True)

    def render_history_items(self):
        # Clear existing items
        for child in self.history_scroll.winfo_children():
            child.destroy()

        if not self.history_items:
            empty_box = ctk.CTkFrame(self.history_scroll, fg_color="transparent")
            empty_box.pack(fill="both", expand=True, pady=70)

            ctk.CTkLabel(
                empty_box,
                text="// NO EXTRACTION RECORDS FOUND",
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=TEXT_MUTED,
            ).pack(pady=(0, 6))

            ctk.CTkLabel(
                empty_box,
                text="Streams downloaded with WAV Ripper will be cataloged here automatically.",
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color="#475569",
            ).pack()
            return

        for item in self.history_items:
            card = ctk.CTkFrame(
                self.history_scroll,
                fg_color=BG_CARD,
                border_color=BORDER_CARD,
                border_width=1,
                corner_radius=8,
            )
            card.pack(fill="x", pady=(0, 8), padx=2)

            # Row 1: Format Badge, Profile info & Timestamp
            row1 = ctk.CTkFrame(card, fg_color="transparent")
            row1.pack(fill="x", padx=10, pady=(8, 2))

            fmt_badge = ctk.CTkLabel(
                row1,
                text=f"[ {item.get('badge', item.get('format', 'MEDIA'))} ]",
                font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                text_color=ACCENT_CYAN,
                fg_color="#0e232e",
                corner_radius=4,
                padx=6,
                pady=2,
            )
            fmt_badge.pack(side="left", padx=(0, 8))

            profile_lbl = ctk.CTkLabel(
                row1,
                text=item.get("profile", ""),
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=TEXT_CYAN,
            )
            profile_lbl.pack(side="left")

            time_lbl = ctk.CTkLabel(
                row1,
                text=item.get("timestamp", ""),
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=TEXT_MUTED,
            )
            time_lbl.pack(side="right")

            # Row 2: Track Title
            row2 = ctk.CTkFrame(card, fg_color="transparent")
            row2.pack(fill="x", padx=10, pady=(0, 4))

            title_text = item.get("title") or item.get("url") or "Unknown Stream"
            title_lbl = ctk.CTkLabel(
                row2,
                text=title_text,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=TEXT_WHITE,
                anchor="w",
            )
            title_lbl.pack(side="left", fill="x", expand=True)

            # Row 3: URL & Action buttons
            row3 = ctk.CTkFrame(card, fg_color="transparent")
            row3.pack(fill="x", padx=10, pady=(0, 8))

            url_str = item.get("url", "")
            display_url = url_str if len(url_str) <= 52 else url_str[:49] + "..."
            url_lbl = ctk.CTkLabel(
                row3,
                text=display_url,
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=TEXT_MUTED,
                anchor="w",
            )
            url_lbl.pack(side="left", fill="x", expand=True)

            btn_box = ctk.CTkFrame(row3, fg_color="transparent")
            btn_box.pack(side="right")

            copy_btn = ctk.CTkButton(
                btn_box,
                text="[COPY LINK]",
                font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                fg_color="#151926",
                hover_color="#1f2538",
                border_color="#2e354d",
                border_width=1,
                text_color=TEXT_CYAN,
                width=76,
                height=24,
                corner_radius=6,
                command=lambda u=url_str: self._copy_to_clip(u),
            )
            copy_btn.pack(side="left", padx=(0, 6))

            dest_path = item.get("dest_path", "")
            open_btn = ctk.CTkButton(
                btn_box,
                text="[OPEN DIR]",
                font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                fg_color="#151926",
                hover_color="#1f2538",
                border_color="#2e354d",
                border_width=1,
                text_color=TEXT_SECONDARY,
                width=76,
                height=24,
                corner_radius=6,
                command=lambda d=dest_path: self._open_history_dir(d),
            )
            open_btn.pack(side="left")

    def _copy_to_clip(self, text):
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_var.set("URL COPIED TO CLIPBOARD // OK")
            self.status_display.configure(text_color=TEXT_CYAN)
        except Exception:
            pass

    def _open_history_dir(self, dest_path):
        folder = dest_path if os.path.isdir(dest_path) else os.path.dirname(dest_path)
        if not folder or not os.path.exists(folder):
            folder = os.path.normpath(os.path.expanduser(self.download_dir_var.get()))
        if os.path.exists(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])

    def clear_history(self):
        if not self.history_items:
            return
        if mb.askyesno("CONFIRM PURGE", "Purge all extraction history records?"):
            self.history_items = []
            save_history([])
            self.update_history_badge()
            self.render_history_items()

    def update_history_badge(self):
        count = len(self.history_items)
        self.btn_nav_history.configure(text=f"// HISTORY [ {count} ]")
        if hasattr(self, "history_total_lbl"):
            self.history_total_lbl.configure(text=f"TOTAL EXTRACTED: {count} ITEMS")

    def _add_to_history(self, title, url, fmt_name, fmt_cfg, lvl_cfg, dest_dir):
        entry = {
            "title": title or url,
            "url": url,
            "format": fmt_name,
            "badge": f"{fmt_cfg.get('badge', fmt_name)} {lvl_cfg.get('tag', '')}",
            "profile": lvl_cfg.get("label", ""),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "dest_path": dest_dir,
        }
        self.history_items.insert(0, entry)
        if len(self.history_items) > 100:
            self.history_items = self.history_items[:100]
        save_history(self.history_items)
        self.update_history_badge()

    # ---------------- Clipboard & Helpers ---------------- #

    def _on_paste_event(self, event=None):
        try:
            clip = self.clipboard_get().strip()
            if clip:
                self.url_var.set(clip)
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, clip)
                self.status_var.set("URL LOADED // READY TO EXECUTE")
                self.status_display.configure(text_color=TEXT_CYAN)
        except Exception:
            pass
        return "break"

    def paste_clipboard(self):
        self._on_paste_event()

    def setup_entry_context_menu(self, entry):
        try:
            menu = tk.Menu(
                entry,
                tearoff=0,
                bg="#11131a",
                fg="#f8fafc",
                activebackground=ACCENT_CYAN,
                activeforeground="#0a0a0c",
                bd=1,
                relief="flat",
                font=("Consolas", 10),
            )
            menu.add_command(label="[ PASTE ]", command=self._on_paste_event)
            menu.add_command(label="[ COPY ]", command=lambda: self._copy_entry(entry))
            menu.add_separator()
            menu.add_command(label="[ CLEAR ]", command=lambda: self.url_var.set(""))

            def _show_menu(e):
                try:
                    menu.tk_popup(e.x_root, e.y_root)
                finally:
                    menu.grab_release()

            entry.bind("<Button-3>", _show_menu)
        except Exception:
            pass

    def _copy_entry(self, entry):
        try:
            val = entry.get()
            if val:
                self.clipboard_clear()
                self.clipboard_append(val)
        except Exception:
            pass

    def browse_destination(self):
        from tkinter import filedialog

        curr = os.path.normpath(os.path.expanduser(self.download_dir_var.get()))
        folder = filedialog.askdirectory(initialdir=curr)
        if folder:
            self.download_dir_var.set(os.path.normpath(folder))

    def open_destination(self):
        folder = os.path.normpath(os.path.expanduser(self.download_dir_var.get()))
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception:
                pass
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    # ---------------- Process Execution ---------------- #

    def start_extraction(self):
        if self.is_downloading:
            return

        url = self.url_var.get().strip()
        if not url:
            self.status_var.set("ERROR // EMPTY TARGET URL")
            self.status_display.configure(text_color=ACCENT_RED)
            return

        target_dir = os.path.normpath(os.path.expanduser(self.download_dir_var.get()))
        os.makedirs(target_dir, exist_ok=True)

        selected_fmt = self.selected_format
        fmt_cfg = FORMAT_CONFIG.get(selected_fmt, FORMAT_CONFIG["WAV"])
        lvl_cfg = self.get_current_level_cfg()

        cmd = [
            self.yt_dlp_bin,
            "-P", target_dir,
            "--no-playlist",
            "--newline",
        ]

        cmd.extend(lvl_cfg["args"])

        if self.ffmpeg_dir:
            cmd.extend(["--ffmpeg-location", self.ffmpeg_dir])

        cmd.append(url)

        self.is_downloading = True
        self._last_download_title = ""
        self._last_process_error = ""
        self.execute_btn.configure(
            state="disabled",
            text=f"[ DOWNLOADING {lvl_cfg['btn_tag']}... PLEASE WAIT ]",
            fg_color="#181a24",
            text_color=TEXT_MUTED,
        )
        self.abort_btn.configure(state="normal")
        self.status_var.set(f"CONNECTING // ACQUIRING {lvl_cfg['btn_tag']} STREAM...")
        self.status_display.configure(text_color=ACCENT_CYAN)
        self.telemetry_var.set("SPEED: ACQUIRING  |  ETA: --:--")

        # Light up progress bar
        self.progress_bar.configure(progress_color=ACCENT_CYAN)
        self.progress_bar.set(0.0)

        threading.Thread(
            target=self._run_process_thread,
            args=(cmd, selected_fmt, fmt_cfg, lvl_cfg, url, target_dir),
            daemon=True,
        ).start()

    def _run_process_thread(self, cmd, selected_fmt, fmt_cfg, lvl_cfg, url, target_dir):
        startupinfo = None
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                startupinfo=startupinfo,
                encoding="utf-8",
                errors="replace",
            )

            progress_regex = re.compile(
                r"\[download\]\s+(\d+(?:\.\d+)?)%\s+of\s+~?(\S+)(?:\s+at\s+(\S+))?(?:\s+ETA\s+(\S+))?"
            )
            dest_regex = re.compile(r"Destination:\s*(.+)$")
            merge_regex = re.compile(r'Merging formats into "(.+?)"')

            for line in iter(self.process.stdout.readline, ""):
                cleaned = line.rstrip()
                if not cleaned:
                    continue

                if "ERROR:" in cleaned:
                    err_info = cleaned.split("ERROR:", 1)[1].strip()
                    self._last_process_error = err_info

                d_match = dest_regex.search(cleaned)
                if d_match:
                    fpath = d_match.group(1).strip()
                    self._last_download_title = os.path.splitext(os.path.basename(fpath))[0]

                m_match = merge_regex.search(cleaned)
                if m_match:
                    fpath = m_match.group(1).strip()
                    self._last_download_title = os.path.splitext(os.path.basename(fpath))[0]

                match = progress_regex.search(cleaned)
                if match:
                    percent_val = float(match.group(1))
                    total_size = match.group(2) or "--"
                    speed = match.group(3) or "--"
                    eta = match.group(4) or "--"

                    self.after(0, self._update_progress, percent_val, total_size, speed, eta)
                elif "[ExtractAudio]" in cleaned:
                    self.after(0, self._update_status, "CONVERTING // ENCODING AUDIO...")
                elif "[Merger]" in cleaned:
                    self.after(0, self._update_status, "MERGING // COMBINING AUDIO + VIDEO...")
                elif "[info]" in cleaned:
                    self.after(0, self._update_status, "PARSING // STREAM METADATA OK")

            self.process.wait()
            rc = self.process.returncode
            self.after(0, self._process_finished, rc, selected_fmt, fmt_cfg, lvl_cfg, url, target_dir)

        except Exception as e:
            self.after(0, self._process_failed, str(e), selected_fmt)

    def _update_progress(self, percent, total_size, speed, eta):
        frac = min(max(percent / 100.0, 0.0), 1.0)
        self.progress_bar.set(frac)
        self.status_var.set(f"DOWNLOADING // {percent:.1f}%")
        self.telemetry_var.set(f"SPEED: {speed}  |  ETA: {eta}  |  SIZE: {total_size}")

    def _update_status(self, text):
        self.status_var.set(text)

    def _process_finished(self, returncode, selected_fmt, fmt_cfg, lvl_cfg, url, target_dir):
        self.is_downloading = False
        self.process = None

        self._update_quality_display()
        self.execute_btn.configure(
            state="normal",
            fg_color=ACCENT_CYAN,
            text_color="#060709",
        )
        self.abort_btn.configure(state="disabled")

        if returncode == 0:
            self.progress_bar.set(1.0)
            self.status_var.set(f"COMPLETE // {lvl_cfg['btn_tag']} SAVED TO DOWNLOADS")
            self.status_display.configure(text_color=ACCENT_GREEN)
            self.telemetry_var.set("STATUS: 100% OK  |  TASK FINISHED")

            # Catalog into persistent history
            title = self._last_download_title if self._last_download_title else url
            self._add_to_history(title, url, selected_fmt, fmt_cfg, lvl_cfg, target_dir)
        else:
            err_msg = getattr(self, "_last_process_error", "")
            if err_msg:
                short_err = err_msg if len(err_msg) <= 45 else err_msg[:42] + "..."
                self.status_var.set(f"FAILED // {short_err.upper()}")
            else:
                self.status_var.set(f"TERMINATED // CODE {returncode}")
            self.status_display.configure(text_color=ACCENT_RED)

    def _process_failed(self, error_msg, selected_fmt):
        self.is_downloading = False
        self.process = None
        self._update_quality_display()
        self.execute_btn.configure(
            state="normal",
            fg_color=ACCENT_CYAN,
            text_color="#060709",
        )
        self.abort_btn.configure(state="disabled")
        self.status_var.set("ERROR // PROCESS EXECUTION FAILED")
        self.status_display.configure(text_color=ACCENT_RED)

    def abort_process(self):
        if self.process and self.is_downloading:
            try:
                self.process.terminate()
            except Exception:
                pass


def main():
    app = MediaRipperApp()
    app.mainloop()


if __name__ == "__main__":
    main()

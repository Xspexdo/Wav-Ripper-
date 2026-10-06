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
CURRENT_VERSION = "v2.4.7"
GITHUB_REPO = "Xspexdo/Wav-Ripper-"

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


TRANSLATIONS = {
    "en": {
        "nav_ripper": "// RIPPER HUD",
        "nav_history": "// HISTORY [ {count} ]",
        "clear_history": "[ CLEAR HISTORY ]",
        "url_header": "// TARGET STREAM URL",
        "url_placeholder": "Paste video or audio link (YouTube, SoundCloud, TikTok, Bilibili...)",
        "btn_paste": "[PASTE]",
        "btn_clear": "[CLEAR]",
        "settings_header": "// FORMAT SELECTION & DESTINATION",
        "fmt_lbl": "FORMAT:",
        "q_lbl": "QUALITY:",
        "dest_lbl": "SAVE TO:",
        "browse_btn": "[BROWSE]",
        "open_btn": "[OPEN DIR]",
        "btn_extract": ">>> START EXTRACTION [{tag}] <<<",
        "btn_download": ">>> START DOWNLOAD [{tag}] <<<",
        "btn_downloading": "[ DOWNLOADING {tag}... PLEASE WAIT ]",
        "btn_abort": "[ABORT]",
        "status_ready": "STATUS // READY FOR STREAM",
        "telemetry_ready": "SPEED: -- MB/s  |  ETA: --:--",
        "engine_footer": "// ENGINE: YT-DLP + FFMPEG HI-RES",
        "history_total": "TOTAL EXTRACTED: {count} ITEMS",
        "history_sub": "PERSISTENT DOWNLOAD CATALOG",
        "history_empty_title": "// NO EXTRACTION RECORDS FOUND",
        "history_empty_desc": "Streams downloaded with WAV Ripper will be cataloged here automatically.",
        "history_copy": "[COPY LINK]",
        "history_open": "[OPEN DIR]",
        "copied": "URL COPIED TO CLIPBOARD // OK",
        "url_loaded": "URL LOADED // READY TO EXECUTE",
        "status_connecting": "CONNECTING // ACQUIRING {tag} STREAM...",
        "status_downloading": "DOWNLOADING // {percent:.1f}%",
        "status_converting": "CONVERTING // ENCODING AUDIO...",
        "status_merging": "MERGING // COMBINING AUDIO + VIDEO...",
        "status_parsing": "PARSING // STREAM METADATA OK",
        "status_complete": "COMPLETE // {tag} SAVED TO DOWNLOADS",
        "telemetry_finished": "STATUS: 100% OK  |  TASK FINISHED",
        "status_error_empty": "ERROR // EMPTY TARGET URL",
        "confirm_purge_title": "CONFIRM PURGE",
        "confirm_purge_msg": "Purge all extraction history records?",
        "status_engine_checking": "INITIALIZING // VERIFYING CORE ENGINES...",
        "status_engine_dl_ytdlp": "INITIALIZING // AUTO-DOWNLOADING YT-DLP ENGINE...",
        "status_engine_dl_ffmpeg": "INITIALIZING // AUTO-DOWNLOADING FFMPEG CODECS...",
        "status_engine_ready": "ENGINES READY // STARTING EXTRACTION...",
        "btn_engine_setup": "[ CONFIGURING ENGINES... PLEASE WAIT ]",
        "btn_update": "UPDATE",
        "update_checking": "CHECKING FOR UPDATES...",
        "update_latest": "WAV Ripper is up to date ({ver})",
        "update_found_title": "NEW VERSION AVAILABLE",
        "update_found_msg": "New version {tag} is available on GitHub!\n\nWould you like to update now?",
        "update_git_prompt": "Git repository detected.\n\nWould you like to pull the latest changes via 'git pull origin main'?",
        "update_git_success": "Repository updated successfully via Git!\n\nPlease restart the application to apply changes.",
        "update_git_latest": "Git repository is already up to date.",
        "update_downloading": "DOWNLOADING UPDATE {tag}...",
        "update_failed": "Failed to check or apply update: {err}",
    },
    "th": {
        "nav_ripper": "// หน้าดาวน์โหลด",
        "nav_history": "// ประวัติการโหลด [ {count} ]",
        "clear_history": "[ ล้างประวัติ ]",
        "url_header": "// ลิงก์ที่ต้องการดาวน์โหลด",
        "url_placeholder": "วางลิงก์วิดีโอหรือเพลง (YouTube, SoundCloud, TikTok, Bilibili...)",
        "btn_paste": "[วางลิงก์]",
        "btn_clear": "[ล้างช่อง]",
        "settings_header": "// เลือกฟอร์แมตและที่เก็บไฟล์",
        "fmt_lbl": "รูปแบบ:",
        "q_lbl": "คุณภาพ:",
        "dest_lbl": "บันทึกที่:",
        "browse_btn": "[เลือกโฟลเดอร์]",
        "open_btn": "[เปิดโฟลเดอร์]",
        "btn_extract": ">>> เริ่มแยกไฟล์เสียง [{tag}] <<<",
        "btn_download": ">>> เริ่มดาวน์โหลดวิดีโอ [{tag}] <<<",
        "btn_downloading": "[ กำลังดาวน์โหลด {tag}... กรุณารอสักครู่ ]",
        "btn_abort": "[ยกเลิก]",
        "status_ready": "สถานะ // พร้อมรับลิงก์ดาวน์โหลด",
        "telemetry_ready": "ความเร็ว: -- MB/s  |  เวลาที่เหลือ: --:--",
        "engine_footer": "// ขับเคลื่อนด้วย: YT-DLP + FFMPEG HI-RES",
        "history_total": "ดาวน์โหลดทั้งหมด: {count} รายการ",
        "history_sub": "สมุดบันทึกประวัติการดาวน์โหลดถาวร",
        "history_empty_title": "// ไม่พบบันทึกประวัติการดาวน์โหลด",
        "history_empty_desc": "ไฟล์ที่ดาวน์โหลดผ่าน WAV Ripper จะแสดงที่นี่อัตโนมัติ",
        "history_copy": "[คัดลอกลิงก์]",
        "history_open": "[เปิดโฟลเดอร์]",
        "copied": "คัดลอกลิงก์ลงคลิปบอร์ดแล้ว // เรียบร้อย",
        "url_loaded": "โหลดลิงก์แล้ว // พร้อมเริ่มดาวน์โหลด",
        "status_connecting": "กำลังเชื่อมต่อ // ค้นหาสตรีม {tag}...",
        "status_downloading": "กำลังดาวน์โหลด // {percent:.1f}%",
        "status_converting": "กำลังแปลงสัญญาณ // บันทึกไฟล์เสียง...",
        "status_merging": "กำลังรวมไฟล์ // รวมสัญญาณภาพและเสียง...",
        "status_parsing": "กำลังอ่านข้อมูล // ตรวจสอบสตรีมสำเร็จ",
        "status_complete": "เสร็จสิ้น // บันทึก {tag} ลงเครื่องเรียบร้อย",
        "telemetry_finished": "สถานะ: 100% สำเร็จ  |  เสร็จสมบูรณ์",
        "status_error_empty": "ข้อผิดพลาด // กรุณาใส่ลิงก์ก่อนเริ่ม",
        "confirm_purge_title": "ยืนยันการล้างประวัติ",
        "confirm_purge_msg": "ต้องการล้างประวัติการดาวน์โหลดทั้งหมดใช่หรือไม่?",
        "status_engine_checking": "กำลังตรวจสอบ // กำลังตรวจสอบระบบดาวน์โหลด...",
        "status_engine_dl_ytdlp": "กำลังติดตั้ง // ดาวน์โหลด ENGINE YT-DLP อัตโนมัติ...",
        "status_engine_dl_ffmpeg": "กำลังติดตั้ง // ดาวน์โหลด FFMPEG CODECS อัตโนมัติ...",
        "status_engine_ready": "ระบบพร้อมใช้งาน // เริ่มการดึงสตรีม...",
        "btn_engine_setup": "[ กำลังติดตั้งระบบดาวน์โหลด... กรุณารอสักครู่ ]",
        "btn_update": "อัปเดต",
        "update_checking": "กำลังตรวจอัปเดต...",
        "update_latest": "WAV Ripper เป็นเวอร์ชันล่าสุดแล้ว ({ver})",
        "update_found_title": "พบเวอร์ชันใหม่",
        "update_found_msg": "พบเวอร์ชัน {tag} บน GitHub!\\n\\nต้องการอัปเดตทันทีหรือไม่?",
        "update_git_prompt": "ตรวจพบ Git Repository ในโฟลเดอร์\\n\\nต้องการดึงเวอร์ชันล่าสุดด้วย 'git pull' หรือไม่?",
        "update_git_success": "อัปเดตโค้ดผ่าน Git สำเร็จแล้ว!\\n\\nกรุณารีสตาร์ทโปรแกรม",
        "update_git_latest": "โค้ดใน Git เป็นเวอร์ชันล่าสุดแล้ว",
        "update_downloading": "กำลังดาวน์โหลดอัปเดต {tag}...",
        "update_failed": "ไม่สามารถอัปเดตได้: {err}",
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


def get_engine_dir():
    """Returns directory where yt-dlp and ffmpeg are placed."""
    candidates = [
        os.path.join(APP_DIR, "bin"),
        APP_DIR,
        os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "WAV-Ripper", "bin"),
    ]
    for target in candidates:
        try:
            os.makedirs(target, exist_ok=True)
            test_file = os.path.join(target, ".perm_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            return target
        except Exception:
            continue
    return APP_DIR


def find_yt_dlp():
    """Locate yt-dlp binary on PATH, local app directory, or WinGet packages directory."""
    path = shutil.which("yt-dlp")
    if path:
        return path

    engine_dir = get_engine_dir()
    for cand in [
        os.path.join(engine_dir, "yt-dlp.exe"),
        os.path.join(APP_DIR, "bin", "yt-dlp.exe"),
        os.path.join(APP_DIR, "yt-dlp.exe"),
        os.path.join(BASE_DIR, "yt-dlp.exe"),
    ]:
        if os.path.isfile(cand):
            return cand

    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        import glob
        matches = glob.glob(
            os.path.join(local_appdata, r"Microsoft\WinGet\Packages\*yt-dlp*\**\yt-dlp.exe"),
            recursive=True,
        )
        if matches:
            return matches[0]

    return None


def find_ffmpeg_dir():
    """Locate ffmpeg binary directory on PATH, local app directory, or WinGet packages directory."""
    path = shutil.which("ffmpeg")
    if path:
        return os.path.dirname(path)

    engine_dir = get_engine_dir()
    for base in [engine_dir, os.path.join(APP_DIR, "bin"), APP_DIR, BASE_DIR]:
        for sub in [("ffmpeg", "bin"), ("bin",), ()]:
            candidate = os.path.join(base, *sub)
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


def download_file_with_progress(url, dest_path, progress_callback=None):
    import urllib.request
    import ssl

    # Bypass Python SSL certificate verification failures on Windows systems
    try:
        ctx = ssl._create_unverified_context()
    except Exception:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            chunk_size = 64 * 1024
            with open(dest_path, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total > 0:
                        progress_callback(downloaded, total)
        if os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
            return
    except Exception as urllib_err:
        # Fallback 1: curl.exe (uses native Windows Schannel certificate store)
        if shutil.which("curl"):
            try:
                cmd = ["curl.exe", "-k", "-L", "-A", "Mozilla/5.0", "-o", dest_path, url]
                res = subprocess.run(
                    cmd,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    timeout=120,
                )
                if res.returncode == 0 and os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
                    return
            except Exception:
                pass

        # Fallback 2: PowerShell with TLS 1.2/1.3 and certificate bypass
        try:
            ps_script = (
                "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13; "
                "[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}; "
                f"(New-Object System.Net.WebClient).DownloadFile('{url}', '{dest_path}')"
            )
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                timeout=120,
            )
            if res.returncode == 0 and os.path.isfile(dest_path) and os.path.getsize(dest_path) > 0:
                return
        except Exception:
            pass

        raise urllib_err


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

        # Language setup: auto-detect system locale
        import locale
        try:
            loc_name = (locale.getlocale()[0] or "").lower()
            self.current_lang = "th" if "thai" in loc_name else "en"
        except Exception:
            self.current_lang = "th"

        self.apply_language()

        # Initialize quality display
        self._update_quality_display()

        # Frameless Window & DPI Centering Setup
        self.setup_frameless(690, 536)

        # Background update check (non-blocking)
        self.update_available = False
        self.after(2000, lambda: self.check_for_updates(manual=False))

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
            key = "btn_download" if cfg["type"] == "video" else "btn_extract"
            self.execute_btn.configure(text=self.t(key, tag=lvl_cfg["btn_tag"]))

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
        self.footer_engine_lbl = ctk.CTkLabel(
            self.footer_frame,
            text=self.t("engine_footer"),
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color="#334155",
        )
        self.footer_engine_lbl.pack(side="left")

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

    def t(self, key, **kwargs):
        lang = getattr(self, "current_lang", "en")
        pack = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
        val = pack.get(key, TRANSLATIONS["en"].get(key, ""))
        if kwargs:
            try:
                val = val.format(**kwargs)
            except Exception:
                pass
        return val

    def toggle_language(self):
        self.current_lang = "th" if getattr(self, "current_lang", "en") == "en" else "en"
        self.apply_language()

    def apply_language(self):
        # Update toggle button text
        if hasattr(self, "btn_lang"):
            self.btn_lang.configure(text="EN" if self.current_lang == "th" else "TH")

        # Navigation Bar
        if hasattr(self, "btn_nav_ripper"):
            self.btn_nav_ripper.configure(text=self.t("nav_ripper"))
        if hasattr(self, "btn_nav_history"):
            self.btn_nav_history.configure(text=self.t("nav_history", count=len(self.history_items)))
        if hasattr(self, "btn_clear_history"):
            self.btn_clear_history.configure(text=self.t("clear_history"))

        # URL Card
        if hasattr(self, "url_header_lbl"):
            self.url_header_lbl.configure(text=self.t("url_header"))
        if hasattr(self, "url_entry"):
            self.url_entry.configure(placeholder_text=self.t("url_placeholder"))
        if hasattr(self, "paste_btn"):
            self.paste_btn.configure(text=self.t("btn_paste"))
        if hasattr(self, "clear_btn"):
            self.clear_btn.configure(text=self.t("btn_clear"))

        # Settings Card
        if hasattr(self, "settings_header_lbl"):
            self.settings_header_lbl.configure(text=self.t("settings_header"))
        if hasattr(self, "fmt_lbl"):
            self.fmt_lbl.configure(text=self.t("fmt_lbl"))
        if hasattr(self, "q_lbl"):
            self.q_lbl.configure(text=self.t("q_lbl"))
        if hasattr(self, "dest_lbl"):
            self.dest_lbl.configure(text=self.t("dest_lbl"))
        if hasattr(self, "browse_btn"):
            self.browse_btn.configure(text=self.t("browse_btn"))
        if hasattr(self, "open_btn"):
            self.open_btn.configure(text=self.t("open_btn"))

        # Progress Card
        if hasattr(self, "abort_btn"):
            self.abort_btn.configure(text=self.t("btn_abort"))

        # Idle Status & Telemetry
        if not self.is_downloading:
            self.status_var.set(self.t("status_ready"))
            self.telemetry_var.set(self.t("telemetry_ready"))

        # Footer
        if hasattr(self, "footer_engine_lbl"):
            self.footer_engine_lbl.configure(text=self.t("engine_footer"))

        # History View
        if hasattr(self, "history_sub_lbl"):
            self.history_sub_lbl.configure(text=self.t("history_sub"))
        self.update_history_badge()

        # Update execute button text
        self._update_quality_display()

        # Titlebar Update Button
        if hasattr(self, "btn_update") and not getattr(self, "update_available", False):
            self.btn_update.configure(text=self.t("btn_update"))

        # Re-render history if currently displayed
        if self.current_tab == "history":
            self.render_history_items()

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
            text=f"HUD {CURRENT_VERSION}",
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

        # Update / Git pull button
        self.btn_update = ctk.CTkButton(
            controls_frame,
            text=self.t("btn_update"),
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            fg_color="#141926",
            hover_color="#1f283d",
            border_color="#2b3754",
            border_width=1,
            text_color="#94a3b8",
            width=54,
            height=26,
            corner_radius=6,
            command=lambda: self.check_for_updates(manual=True),
        )
        self.btn_update.pack(side="left", padx=(0, 6), pady=8)

        # Language Switcher Toggle [ EN | TH ]
        self.btn_lang = ctk.CTkButton(
            controls_frame,
            text="EN" if getattr(self, "current_lang", "en") == "th" else "TH",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#141926",
            hover_color="#1f283d",
            border_color="#2b3754",
            border_width=1,
            text_color=ACCENT_CYAN,
            width=36,
            height=26,
            corner_radius=6,
            command=self.toggle_language,
        )
        self.btn_lang.pack(side="left", padx=(0, 6), pady=8)

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
        self.url_header_lbl = ctk.CTkLabel(
            parent,
            text=self.t("url_header"),
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        self.url_header_lbl.pack(anchor="w", pady=(0, 4))

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
            placeholder_text=self.t("url_placeholder"),
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

        self.paste_btn = ctk.CTkButton(
            row,
            text=self.t("btn_paste"),
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
        self.paste_btn.pack(side="left", padx=(0, 6))

        self.clear_btn = ctk.CTkButton(
            row,
            text=self.t("btn_clear"),
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
        self.clear_btn.pack(side="left")

    def build_settings_card(self, parent):
        self.settings_header_lbl = ctk.CTkLabel(
            parent,
            text=self.t("settings_header"),
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        self.settings_header_lbl.pack(anchor="w", pady=(0, 4))

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

        self.fmt_lbl = ctk.CTkLabel(
            row1,
            text=self.t("fmt_lbl"),
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        self.fmt_lbl.pack(side="left")

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

        self.q_lbl = ctk.CTkLabel(
            row2,
            text=self.t("q_lbl"),
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        self.q_lbl.pack(side="left")

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

        self.dest_lbl = ctk.CTkLabel(
            row3,
            text=self.t("dest_lbl"),
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=TEXT_MUTED,
            width=64,
            anchor="w",
        )
        self.dest_lbl.pack(side="left")

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

        self.browse_btn = ctk.CTkButton(
            row3,
            text=self.t("browse_btn"),
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
        self.browse_btn.pack(side="left", padx=(0, 6))

        self.open_btn = ctk.CTkButton(
            row3,
            text=self.t("open_btn"),
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
        self.open_btn.pack(side="left")

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
            text=self.t("history_total", count=count),
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=ACCENT_CYAN,
        )
        self.history_total_lbl.pack(side="left")

        self.history_sub_lbl = ctk.CTkLabel(
            summary_row,
            text=self.t("history_sub"),
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=TEXT_MUTED,
        )
        self.history_sub_lbl.pack(side="right")

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
                text=self.t("history_empty_title"),
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=TEXT_MUTED,
            ).pack(pady=(0, 6))

            ctk.CTkLabel(
                empty_box,
                text=self.t("history_empty_desc"),
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
                text=self.t("history_copy"),
                font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                fg_color="#151926",
                hover_color="#1f2538",
                border_color="#2e354d",
                border_width=1,
                text_color=TEXT_CYAN,
                width=86 if getattr(self, "current_lang", "en") == "th" else 76,
                height=24,
                corner_radius=6,
                command=lambda u=url_str: self._copy_to_clip(u),
            )
            copy_btn.pack(side="left", padx=(0, 6))

            dest_path = item.get("dest_path", "")
            open_btn = ctk.CTkButton(
                btn_box,
                text=self.t("history_open"),
                font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
                fg_color="#151926",
                hover_color="#1f2538",
                border_color="#2e354d",
                border_width=1,
                text_color=TEXT_SECONDARY,
                width=86 if getattr(self, "current_lang", "en") == "th" else 76,
                height=24,
                corner_radius=6,
                command=lambda d=dest_path: self._open_history_dir(d),
            )
            open_btn.pack(side="left")

    def _copy_to_clip(self, text):
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_var.set(self.t("copied"))
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
        if mb.askyesno(self.t("confirm_purge_title"), self.t("confirm_purge_msg")):
            self.history_items = []
            save_history([])
            self.update_history_badge()
            self.render_history_items()

    def update_history_badge(self):
        count = len(self.history_items)
        self.btn_nav_history.configure(text=self.t("nav_history", count=count))
        if hasattr(self, "history_total_lbl"):
            self.history_total_lbl.configure(text=self.t("history_total", count=count))

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
                self.status_var.set(self.t("url_loaded"))
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
            self.status_var.set(self.t("status_error_empty"))
            self.status_display.configure(text_color=ACCENT_RED)
            return

        # Ensure engines are ready
        self.yt_dlp_bin = find_yt_dlp()
        self.ffmpeg_dir = find_ffmpeg_dir()

        if not self.yt_dlp_bin or not self.ffmpeg_dir:
            self._setup_missing_engines_and_run(url)
            return

        self._execute_download(url)

    def _setup_missing_engines_and_run(self, url):
        self.is_downloading = True
        self.execute_btn.configure(
            state="disabled",
            text=self.t("btn_engine_setup"),
            fg_color="#181a24",
            text_color=TEXT_MUTED,
        )
        self.abort_btn.configure(state="disabled")
        self.progress_bar.configure(progress_color=ACCENT_CYAN)
        self.progress_bar.set(0.0)

        threading.Thread(
            target=self._engine_installer_thread,
            args=(url,),
            daemon=True,
        ).start()

    def _engine_installer_thread(self, target_url):
        engine_dir = get_engine_dir()
        os.makedirs(engine_dir, exist_ok=True)

        try:
            # 1. Download yt-dlp if missing
            if not self.yt_dlp_bin:
                self.after(0, self.status_var.set, self.t("status_engine_dl_ytdlp"))
                dest_ytdlp = os.path.join(engine_dir, "yt-dlp.exe")

                def _ytdlp_prog(dl, total):
                    pct = dl / total
                    dl_mb = dl / (1024 * 1024)
                    tot_mb = total / (1024 * 1024)
                    self.after(0, self._update_engine_progress, pct, dl_mb, tot_mb)

                download_file_with_progress(
                    "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe",
                    dest_ytdlp,
                    _ytdlp_prog,
                )
                self.yt_dlp_bin = dest_ytdlp

            # 2. Setup ffmpeg if missing
            if not self.ffmpeg_dir:
                self.after(0, self.status_var.set, self.t("status_engine_dl_ffmpeg"))
                zip_path = os.path.join(engine_dir, "ffmpeg.zip")

                def _ff_prog(dl, total):
                    pct = dl / total
                    dl_mb = dl / (1024 * 1024)
                    tot_mb = total / (1024 * 1024)
                    self.after(0, self._update_engine_progress, pct, dl_mb, tot_mb)

                download_file_with_progress(
                    "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v6.1/ffmpeg-6.1-win-64.zip",
                    zip_path,
                    _ff_prog,
                )

                import zipfile
                with zipfile.ZipFile(zip_path, "r") as z:
                    for item in z.namelist():
                        if item.lower().endswith("ffmpeg.exe"):
                            with z.open(item) as src, open(os.path.join(engine_dir, "ffmpeg.exe"), "wb") as dst:
                                shutil.copyfileobj(src, dst)
                            break
                try:
                    os.remove(zip_path)
                except Exception:
                    pass

                self.ffmpeg_dir = engine_dir

            # Engines ready: schedule download on main thread immediately
            self.after(0, self._on_engines_ready, target_url)

        except Exception as e:
            self.after(0, self._on_engine_setup_failed, str(e))

    def _update_engine_progress(self, percent, dl_mb, tot_mb):
        self.progress_bar.set(percent)
        self.telemetry_var.set(f"ENGINE SETUP: {percent*100:.0f}%  |  {dl_mb:.1f} / {tot_mb:.1f} MB")

    def _on_engines_ready(self, url):
        self.is_downloading = False
        self.status_var.set(self.t("status_engine_ready"))
        self._execute_download(url)

    def _on_engine_setup_failed(self, error_msg):
        self.is_downloading = False
        self._update_quality_display()
        self.execute_btn.configure(
            state="normal",
            fg_color=ACCENT_CYAN,
            text_color="#060709",
        )
        self.abort_btn.configure(state="disabled")
        short_err = error_msg if len(error_msg) <= 45 else error_msg[:42] + "..."
        self.status_var.set(f"ENGINE ERROR // {short_err.upper()}")
        self.status_display.configure(text_color=ACCENT_RED)
        self.telemetry_var.set("CHECK INTERNET CONNECTION & RETRY")

    # ---------------- Version Update Mechanisms ---------------- #

    def check_for_updates(self, manual=False):
        threading.Thread(
            target=self._check_updates_worker,
            args=(manual,),
            daemon=True,
        ).start()

    def _check_updates_worker(self, manual):
        # 1. If inside a Git clone, check and update via Git
        git_dir = os.path.join(APP_DIR, ".git")
        if os.path.isdir(git_dir) and shutil.which("git"):
            try:
                if manual:
                    self.after(0, self.status_var.set, self.t("update_checking"))
                subprocess.run(
                    ["git", "fetch", "origin", "main"],
                    cwd=APP_DIR,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    timeout=15,
                )
                diff_res = subprocess.run(
                    ["git", "rev-list", "HEAD..origin/main", "--count"],
                    cwd=APP_DIR,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    timeout=10,
                )
                behind_count = int(diff_res.stdout.strip()) if diff_res.stdout.strip().isdigit() else 0
                if behind_count > 0:
                    self.after(0, self._on_git_update_available, behind_count, manual)
                    return
                elif manual:
                    self.after(0, mb.showinfo, "GIT UPDATE", self.t("update_git_latest"))
                    self.after(0, self.status_var.set, self.t("status_ready"))
                    return
            except Exception as e:
                if manual:
                    self.after(0, mb.showerror, "GIT ERROR", self.t("update_failed", err=str(e)))
                    return

        # 2. Check GitHub Releases API
        try:
            if manual:
                self.after(0, self.status_var.set, self.t("update_checking"))
            import ssl, urllib.request
            try:
                ctx = ssl._create_unverified_context()
            except Exception:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

            api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            latest_tag = data.get("tag_name", "").strip()

            if latest_tag and latest_tag != CURRENT_VERSION:
                self.after(0, self._on_release_update_available, latest_tag, data, manual)
            elif manual:
                self.after(0, mb.showinfo, "UPDATE", self.t("update_latest", ver=CURRENT_VERSION))
                self.after(0, self.status_var.set, self.t("status_ready"))
        except Exception as e:
            if manual:
                self.after(0, mb.showerror, "UPDATE ERROR", self.t("update_failed", err=str(e)))
                self.after(0, self.status_var.set, self.t("status_ready"))

    def _on_git_update_available(self, count, manual):
        self.update_available = True
        self.btn_update.configure(
            text="GIT PULL",
            fg_color="#18273d",
            hover_color="#223b5c",
            border_color=ACCENT_CYAN,
            text_color=ACCENT_CYAN,
        )
        if manual:
            if mb.askyesno(self.t("update_found_title"), self.t("update_git_prompt")):
                self.status_var.set(self.t("update_downloading", tag="via Git"))
                try:
                    subprocess.run(
                        ["git", "pull", "origin", "main"],
                        cwd=APP_DIR,
                        check=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    )
                    mb.showinfo(self.t("update_found_title"), self.t("update_git_success"))
                    self.status_var.set(self.t("status_ready"))
                    self.btn_update.configure(text=self.t("btn_update"), text_color="#94a3b8", border_color="#2b3754")
                except Exception as e:
                    mb.showerror("GIT ERROR", self.t("update_failed", err=str(e)))

    def _on_release_update_available(self, latest_tag, release_data, manual):
        self.update_available = True
        self.btn_update.configure(
            text=f"NEW {latest_tag}",
            fg_color="#18273d",
            hover_color="#223b5c",
            border_color=ACCENT_CYAN,
            text_color=ACCENT_CYAN,
        )
        if manual:
            if mb.askyesno(self.t("update_found_title"), self.t("update_found_msg", tag=latest_tag)):
                # Find direct .exe asset if frozen
                exe_asset_url = None
                for asset in release_data.get("assets", []):
                    if asset.get("name") == "WAV-Ripper.exe":
                        exe_asset_url = asset.get("browser_download_url")
                        break

                if getattr(sys, "frozen", False) and exe_asset_url:
                    threading.Thread(
                        target=self._download_and_apply_exe_update,
                        args=(exe_asset_url, latest_tag),
                        daemon=True,
                    ).start()
                else:
                    import webbrowser
                    webbrowser.open_new_tab(release_data.get("html_url", f"https://github.com/{GITHUB_REPO}/releases"))

    def _download_and_apply_exe_update(self, download_url, tag):
        self.status_var.set(self.t("update_downloading", tag=tag))
        self.progress_bar.set(0.0)

        def _prog(dl, tot):
            self.after(0, self.progress_bar.set, dl / tot)
            self.after(0, self.telemetry_var.set, f"UPDATING: {dl/(1024*1024):.1f}/{tot/(1024*1024):.1f} MB")

        temp_exe = os.path.join(APP_DIR, "WAV-Ripper.new.exe")
        try:
            download_file_with_progress(download_url, temp_exe, _prog)
            curr_exe = sys.executable
            bat_file = os.path.join(APP_DIR, "update_apply.bat")
            bat_content = f"""@echo off
timeout /t 1 /nobreak >nul
move /y "{temp_exe}" "{curr_exe}" >nul
start "" "{curr_exe}"
del "%~f0"
"""
            with open(bat_file, "w", encoding="utf-8") as f:
                f.write(bat_content)

            subprocess.Popen(
                ["cmd.exe", "/c", bat_file],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
            os._exit(0)
        except Exception as e:
            self.after(0, mb.showerror, "UPDATE ERROR", self.t("update_failed", err=str(e)))

    def _execute_download(self, url):
        try:
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
                text=self.t("btn_downloading", tag=lvl_cfg["btn_tag"]),
                fg_color="#181a24",
                text_color=TEXT_MUTED,
            )
            self.abort_btn.configure(state="normal")
            self.status_var.set(self.t("status_connecting", tag=lvl_cfg["btn_tag"]))
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
        except Exception as e:
            self.is_downloading = False
            self._update_quality_display()
            self.execute_btn.configure(state="normal", fg_color=ACCENT_CYAN, text_color="#060709")
            self.status_var.set(f"ERROR // {str(e)[:40].upper()}")
            self.status_display.configure(text_color=ACCENT_RED)

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
                    self.after(0, self._update_status, self.t("status_converting"))
                elif "[Merger]" in cleaned:
                    self.after(0, self._update_status, self.t("status_merging"))
                elif "[info]" in cleaned:
                    self.after(0, self._update_status, self.t("status_parsing"))

            self.process.wait()
            rc = self.process.returncode
            self.after(0, self._process_finished, rc, selected_fmt, fmt_cfg, lvl_cfg, url, target_dir)

        except Exception as e:
            self.after(0, self._process_failed, str(e), selected_fmt)

    def _update_progress(self, percent, total_size, speed, eta):
        frac = min(max(percent / 100.0, 0.0), 1.0)
        self.progress_bar.set(frac)
        self.status_var.set(self.t("status_downloading", percent=percent))
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
            self.status_var.set(self.t("status_complete", tag=lvl_cfg["btn_tag"]))
            self.status_display.configure(text_color=ACCENT_GREEN)
            self.telemetry_var.set(self.t("telemetry_finished"))

            # Catalog into persistent history
            title = self._last_download_title if self._last_download_title else url
            self._add_to_history(title, url, selected_fmt, fmt_cfg, lvl_cfg, target_dir)

            # Automatically reveal output folder in Windows Explorer
            if os.path.exists(target_dir):
                if sys.platform == "win32":
                    try:
                        os.startfile(target_dir)
                    except Exception:
                        pass
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
        short_err = error_msg if len(error_msg) <= 45 else error_msg[:42] + "..."
        self.status_var.set(f"ERROR // {short_err.upper()}")
        self.status_display.configure(text_color=ACCENT_RED)

    def abort_process(self):
        self.is_downloading = False
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
            self.process = None
        self._update_quality_display()
        self.execute_btn.configure(
            state="normal",
            fg_color=ACCENT_CYAN,
            text_color="#060709",
        )
        self.abort_btn.configure(state="disabled")
        self.status_var.set(self.t("status_ready"))
        self.status_display.configure(text_color=TEXT_CYAN)
        self.telemetry_var.set(self.t("telemetry_ready"))


def main():
    app = MediaRipperApp()
    app.mainloop()


if __name__ == "__main__":
    main()

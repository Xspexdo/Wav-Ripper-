# WAV RIPPER // DARK MINIMAL GAMING HUD

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-CustomTkinter-00f0ff?style=for-the-badge)
![Engine](https://img.shields.io/badge/Engine-yt--dlp%20%7C%20ffmpeg-e11d48?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)
![Author](https://img.shields.io/badge/Developer-xspexdo-blue?style=for-the-badge)

A high-performance, lossless media ripper and stream extraction application styled as a **Dark Minimal / Cyber HUD Overlay** (`#0a0a0c`). Built with zero bloat, zero telemetry, and maximum audio-video fidelity.

---

## FEATURES

- **Interactive Quality Stepper `[ - ]` / `[ + ]`**:
  - **WAV (PCM)**: 16-Bit / 44.1kHz (CD Std) -> 24-Bit / 48kHz (Studio Master) -> 24-Bit / 96kHz (Hi-Res) -> 32-Bit / 192kHz (Audiophile Float)
  - **MP3 (CBR)**: 128kbps -> 192kbps -> 256kbps -> 320kbps Maximum Fidelity
  - **MP4 (Video)**: 480p SD -> 720p HD -> 1080p FHD -> 1440p 2K
  - **BEST VIDEO**: Highest available stream up to 4K / 2160p 60fps
- **Universal Clipboard History (`Win + V`)**:
  - Full support for `Windows + V` clipboard flyout and `Ctrl + V` across all keyboard layouts (English, Thai, etc.).
  - Right-click dark HUD context menu.
- **Persistent History Catalog (`// HISTORY [ N ]`)**:
  - Tracks downloaded tracks, URLs, profiles, timestamps, and target paths.
  - 1-click `[COPY LINK]`, `[OPEN DIR]`, and `[CLEAR HISTORY]`.
- **Pure Local & Standalone Architecture**:
  - 100% Client-side. Connects directly to media platforms via `yt-dlp` and processes streams through local `FFmpeg`.
  - No middleman servers, no rate limits, no accounts required.

---

## PREREQUISITES

1. **Python 3.10+** ([python.org](https://www.python.org/))
2. **FFmpeg** (Required for audio extraction & video merging):
   ```powershell
   winget install Gyan.FFmpeg
   # or
   winget install yt-dlp.FFmpeg
   ```
3. **yt-dlp**:
   ```powershell
   winget install yt-dlp.yt-dlp
   # or via pip
   pip install yt-dlp
   ```

---

## INSTALLATION & QUICK START

1. **Clone the repository**:
   ```bash
   git clone https://github.com/xspexdo/wav-ripper.git
   cd wav-ripper
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**:
   - Double-click **`run.bat`**
   - Or run via Python:
     ```bash
     pythonw wav_hud.pyw
     ```

4. **(Optional) Create Desktop Shortcut with Icon**:
   ```bash
   python create_shortcut.py
   ```
   This generates a glowing desktop shortcut pointing directly to the app with the custom brand icon.

---

## PROJECT STRUCTURE

```
wav-ripper/
├── wav_hud.pyw          # Main Application (Windowless Python HUD)
├── wav_hud.py           # CLI / Terminal compatible mirror
├── test_hud.py          # Standalone verification self-test
├── create_shortcut.py   # Desktop shortcut generator
├── run.bat              # 1-Click launcher
├── requirements.txt     # Python package requirements
├── logo.ico             # High-resolution glowing WAV icon
├── logo_rounded.png     # HUD Titlebar brand mark
├── LICENSE              # MIT License
└── README.md            # Documentation
```

---

## CREDITS

- **Created & Engineered by**: **xspexdo** ([@xspexdo](https://github.com/xspexdo))
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp), [FFmpeg](https://ffmpeg.org/), and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## LICENSE

Distributed under the **MIT License**. See `LICENSE` for more information.

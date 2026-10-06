# WAV RIPPER // DARK MINIMAL GAMING HUD

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![UI](https://img.shields.io/badge/UI-CustomTkinter-00f0ff?style=for-the-badge)
![Engine](https://img.shields.io/badge/Engine-yt--dlp%20%7C%20ffmpeg-e11d48?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)
![Author](https://img.shields.io/badge/Developer-xspexdo-blue?style=for-the-badge)

[ English ](#english) | [ ภาษาไทย ](#ภาษาไทย)

---

<a name="english"></a>
## ENGLISH (EN)

A high-performance, lossless media ripper and stream extraction tool designed with a **Dark Minimal / Cyber HUD Overlay** aesthetic (`#0a0a0c`). Engineered with zero bloat, zero telemetry, and maximum audio-video fidelity.

### KEY FEATURES

- **Interactive Quality Stepper `[ - ]` / `[ + ]`**:
  - **WAV (Lossless PCM)**: 
    - `16b/44k`: 16-Bit / 44.1kHz (CD Standard, 1411 kbps)
    - `24b/48k`: 24-Bit / 48.0kHz (Studio Master, 2304 kbps)
    - `24b/96k`: 24-Bit / 96.0kHz (Hi-Res Audio, 4608 kbps)
    - `32b/192k`: 32-Bit / 192.0kHz (Audiophile Float, 12288 kbps)
  - **MP3 (Compressed Audio)**:
    - `128k`: 128 kbps CBR (Compact / Economy)
    - `192k`: 192 kbps CBR (Standard Quality)
    - `256k`: 256 kbps CBR (High Fidelity)
    - `320k`: 320 kbps CBR (Maximum MP3 Quality)
  - **MP4 (Video Container)**:
    - 480p SD | 720p HD | 1080p FHD | 1440p 2K QHD
  - **BEST VIDEO**:
    - Direct stream capture up to 4K / 2160p 60fps
- **Universal Clipboard History (`Win + V`)**:
  - Deep integration with `Windows + V` clipboard flyout and `Ctrl + V` across all keyboard languages (English, Thai, etc.).
  - Right-click dark HUD context menu (`[PASTE]`, `[COPY]`, `[CLEAR]`).
- **Persistent History Catalog (`// HISTORY [ N ]`)**:
  - Automatically logs tracks, source URLs, exact audio profiles, timestamps, and save paths.
  - Quick action buttons: `[COPY LINK]`, `[OPEN DIR]`, and `[CLEAR HISTORY]`.
- **100% Local & Standalone Architecture**:
  - Operates completely offline/client-side. Directly accesses media streams via `yt-dlp` and processes codecs through local `FFmpeg`.
  - No middleman servers, no rate limits, no accounts required.

### PREREQUISITES

1. **Python 3.10 or higher** ([python.org](https://www.python.org/))
2. **FFmpeg** (Required for audio conversion and muxing):
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

### QUICK START

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Xspexdo/Wav-Ripper-.git
   cd Wav-Ripper-
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**:
   - Double-click **`run.bat`**
   - Or run via terminal:
     ```bash
     pythonw wav_hud.pyw
     ```

4. **(Optional) Create Desktop Shortcut**:
   ```bash
   python create_shortcut.py
   ```
   Generates a dedicated desktop shortcut with the glowing custom brand icon.

---

<a name="ภาษาไทย"></a>
## ภาษาไทย (TH)

โปรแกรมดาวน์โหลดและแปลงไฟล์เสียง/วิดีโอคุณภาพสูงระดับ Lossless สไตล์ **Dark Minimal / Cyber HUD Overlay** (`#0a0a0c`) ออกแบบมาเพื่อความคลีน เบาเครื่อง ไม่มีโฆษณา ไม่เก็บข้อมูลส่วนตัว และให้คุณภาพไฟล์เสียงสูงสุด

### ฟีเจอร์เด่น

- **ปุ่มปรับระดับคุณภาพเสียงและวิดีโอ `[ - ]` / `[ + ]`**:
  - **WAV (ไฟล์เสียงไม่บีบอัด PCM)**:
    - `16b/44k`: 16-Bit / 44.1kHz (มาตรฐานแผ่นซีดี CD Standard, 1411 kbps)
    - `24b/48k`: 24-Bit / 48.0kHz (ระดับงานสตูดิโอ Studio Master, 2304 kbps)
    - `24b/96k`: 24-Bit / 96.0kHz (ความละเอียดสูง Hi-Res Audio, 4608 kbps)
    - `32b/192k`: 32-Bit / 192.0kHz (ระดับสูงสุด Audiophile Float, 12288 kbps)
  - **MP3 (ไฟล์เพลงสเตอริโอ CBR)**:
    - เลือกระดับบิตเรตได้ตั้งแต่ 128kbps, 192kbps, 256kbps จนถึงสูงสุด **320kbps**
  - **MP4 (วิดีโอ)**:
    - 480p SD, 720p HD, 1080p Full HD, และ 1440p 2K
  - **BEST VIDEO**:
    - ดึงความละเอียดสูงสุดจากต้นทาง รองรับถึง 4K 2160p 60fps
- **รองรับประวัติคลิปบอร์ด Windows (`Win + V`)**:
  - รองรับการวางลิงก์ด้วยปุ่ม `Windows + V` และ `Ctrl + V` อย่างสมบูรณ์แบบ ไม่ว่าจะใช้คีย์บอร์ดภาษาไทยหรือภาษาอังกฤษ
  - มีเมนูคลิกขวาสไตล์ Dark HUD สำหรับกด Paste / Copy / Clear
- **สมุดบันทึกประวัติการดาวน์โหลด (`// HISTORY [ N ]`)**:
  - บันทึกชื่อเพลง ลิงก์ต้นทาง บิตเรต วันเวลา และโฟลเดอร์ปลายทางอัตโนมัติ
  - มีปุ่มลัด `[COPY LINK]` ก๊อปปี้ลิงก์เดิม, `[OPEN DIR]` เปิดโฟลเดอร์ไฟล์, และ `[CLEAR HISTORY]` ล้างประวัติ
- **ทำงานในเครื่อง 100% (Standalone / Local)**:
  - ไม่ผ่านเซิร์ฟเวอร์ตัวกลาง ปลอดภัยสูง ดึงสตรีมตรงผ่าน `yt-dlp` และประมวลผลด้วย `FFmpeg` ภายในเครื่อง

### สิ่งที่ต้องติดตั้งก่อนใช้งาน

1. **Python 3.10 ขึ้นไป** ([python.org](https://www.python.org/))
2. **FFmpeg** (ใช้สำหรับแปลงสัญญาณเสียงและรวมไฟล์):
   ```powershell
   winget install Gyan.FFmpeg
   # หรือ
   winget install yt-dlp.FFmpeg
   ```
3. **yt-dlp**:
   ```powershell
   winget install yt-dlp.yt-dlp
   # หรือผ่าน pip
   pip install yt-dlp
   ```

### วิธีติดตั้งและเริ่มใช้งาน

1. **ดาวน์โหลดโปรเจกต์ (Clone Repo)**:
   ```bash
   git clone https://github.com/Xspexdo/Wav-Ripper-.git
   cd Wav-Ripper-
   ```

2. **ติดตั้งไลบรารีที่จำเป็น**:
   ```bash
   pip install -r requirements.txt
   ```

3. **เปิดใช้งานโปรแกรม**:
   - ดับเบิลคลิกไฟล์ **`run.bat`**
   - หรือรันผ่านคำสั่ง:
     ```bash
     pythonw wav_hud.pyw
     ```

4. **(แนะนำ) สร้างไอคอนช็อตคัตบนหน้า Desktop**:
   ```bash
   python create_shortcut.py
   ```
   โปรแกรมจะสร้างช็อตคัต **WAV Ripper** พร้อมไอคอนโลโก้ความละเอียดสูงบน Desktop ให้อัตโนมัติ

---

## โครงสร้างโปรเจกต์ (PROJECT STRUCTURE)

```
Wav-Ripper-/
├── wav_hud.pyw          # ตัวโปรแกรมหลัก (Windowless Python HUD)
├── wav_hud.py           # ตัวโปรแกรมสำรอง (สำหรับรันผ่าน Command Line)
├── test_hud.py          # สคริปต์ตรวจสอบระบบอัตโนมัติ (Self-check Suite)
├── create_shortcut.py   # สคริปต์สร้างไอคอนช็อตคัตบนหน้า Desktop
├── run.bat              # สคริปต์เปิดโปรแกรมแบบ 1-Click
├── requirements.txt     # รายการโมดูล Python ที่ต้องใช้
├── logo.ico             # ไอคอนโปรแกรมความละเอียดสูง
├── logo_rounded.png     # โลโก้แบรนด์ WAV มุมโค้งสำหรับ Titlebar
├── LICENSE              # ใบอนุญาตเปิดเผยซอร์สโค้ด (MIT License)
└── README.md            # คู่มือการใช้งาน (TH / EN)
```

---

## เครดิตผู้พัฒนา (CREDITS)

- **Engineered & Maintained by**: **xspexdo** ([@xspexdo](https://github.com/xspexdo))
- ขับเคลื่อนด้วยพลังของ [yt-dlp](https://github.com/yt-dlp/yt-dlp), [FFmpeg](https://ffmpeg.org/), และ [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## ใบอนุญาต (LICENSE)

โปรเจกต์นี้เผยแพร่ภายใต้เงื่อนไข **MIT License** ดูรายละเอียดเพิ่มเติมได้ที่ไฟล์ `LICENSE`

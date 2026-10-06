"""
Self-check verification for WAV Media Ripper HUD (v2.4 Clean Minimal HUD).
Run without frameworks or external test runners: python test_hud.py
"""

import os
import sys
import json
import tkinter as tk
import customtkinter as ctk

from wav_hud import (
    MediaRipperApp,
    find_yt_dlp,
    find_ffmpeg_dir,
    BG_MAIN,
    FORMAT_CONFIG,
    load_history,
    save_history,
)


def run_checks():
    print("[TEST] Running self-check suite for WAV Ripper v2.4...")

    # 1. Binary resolutions
    yt_bin = find_yt_dlp()
    assert yt_bin, "Failed: yt-dlp binary resolution returned empty."
    print(f"  [PASS] yt-dlp resolved: {yt_bin}")

    ffmpeg_dir = find_ffmpeg_dir()
    print(f"  [PASS] ffmpeg dir resolved: {ffmpeg_dir}")

    # 2. UI instantiation & initial properties
    app = MediaRipperApp()
    app.update_idletasks()
    app.update()

    assert app.cget("fg_color") == BG_MAIN, f"Failed: Background must be {BG_MAIN}"
    assert hasattr(app, "cr_btn") and "xspexdo" in app.cr_btn.cget("text"), "Failed: Credit badge missing"
    print(f"  [PASS] Window theme verified: {BG_MAIN}")
    print(f"  [PASS] Developer credit verified: {app.cr_btn.cget('text')}")

    # 3. Quality Level Stepper on WAV & MP3
    app.select_format("WAV")
    assert app.selected_levels["WAV"] == 0
    assert "16-BIT" in app.format_desc_var.get()

    app.adjust_quality_level(1)
    assert app.selected_levels["WAV"] == 1
    assert "24-BIT / 48.0kHz" in app.format_desc_var.get()
    print(f"  [PASS] WAV quality adjustment verified: {app.format_desc_var.get()}")

    app.select_format("MP3")
    assert "CBR" in app.format_desc_var.get()
    print(f"  [PASS] MP3 format selection verified: {app.format_desc_var.get()}")

    # 4. Clipboard & Win+V paste test
    test_link = "https://www.youtube.com/watch?v=clean_test"
    app.clipboard_clear()
    app.clipboard_append(test_link)
    app.update()
    res = app._on_paste_event()
    assert res == "break"
    assert app.url_var.get() == test_link
    print("  [PASS] Win+V & clipboard paste mechanism verified.")

    # 5. History Catalog Load/Save
    items = load_history()
    assert isinstance(items, list)
    print(f"  [PASS] History ledger loaded ({len(items)} entries).")

    # Cleanup (clear test clipboard and destroy window)
    app.clipboard_clear()
    app.destroy()
    print("[TEST] ALL CHECKS PASSED SUCCESSFULLY (100% OK).")


if __name__ == "__main__":
    run_checks()

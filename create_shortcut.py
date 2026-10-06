import os
import sys
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
target_script = os.path.join(BASE_DIR, "wav_hud.pyw")
icon_path = os.path.join(BASE_DIR, "logo.ico")

# Locate pythonw.exe
py_dir = os.path.dirname(sys.executable)
pyw_candidate = os.path.join(py_dir, "pythonw.exe")
if os.path.isfile(pyw_candidate):
    pyw_exe = pyw_candidate
else:
    pyw_exe = shutil.which("pythonw") or sys.executable

desktop = os.path.expanduser("~/Desktop")
targets = [
    os.path.join(desktop, "WAV Ripper.lnk"),
    os.path.join(BASE_DIR, "WAV Ripper.lnk"),
]

def make_shortcut(lnk_path):
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        s = shell.CreateShortCut(lnk_path)
        s.TargetPath = pyw_exe
        s.Arguments = f'"{target_script}"'
        s.WorkingDirectory = BASE_DIR
        if os.path.isfile(icon_path):
            s.IconLocation = f"{icon_path},0"
        s.Description = "WAV Media Ripper // Dark Minimal HUD"
        s.Save()
        print(f"[OK] Created shortcut via COM: {lnk_path}")
    except Exception:
        # Fallback to native PowerShell WScript.Shell
        ps_cmd = (
            f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{lnk_path}');"
            f"$s.TargetPath = '{pyw_exe}';"
            f"$s.Arguments = '\"{target_script}\"';"
            f"$s.WorkingDirectory = '{BASE_DIR}';"
            f"$s.IconLocation = '{icon_path},0';"
            f"$s.Description = 'WAV Media Ripper // Dark Minimal HUD';"
            f"$s.Save()"
        )
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[OK] Created shortcut via PowerShell: {lnk_path}")
        else:
            print(f"[FAIL] Could not create shortcut: {lnk_path}")

for t in targets:
    make_shortcut(t)

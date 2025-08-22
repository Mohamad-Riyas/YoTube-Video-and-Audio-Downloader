import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import threading
from yt_dlp import YoutubeDL

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

def download_video():
    video_url = url_entry.get()
    folder_path = folder_entry.get()
    choice = var.get()

    if not video_url or not folder_path:
        messagebox.showwarning("Input Error", "Please enter both URL and download folder.")
        return

    if choice == "video":
        format_code = "18"  # Video + Audio
    else:
        format_code = "bestaudio"  # Audio only

    download_btn.config(state=tk.DISABLED)
    progress_bar['value'] = 0
    status_label.config(text="Starting download...")

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            try:
                progress_bar['value'] = float(percent.replace('%',''))
                status_label.config(text=f"Downloading... {percent}")
            except:
                pass
        elif d['status'] == 'finished':
            status_label.config(text="Download finished!")

    def run_download():
        ydl_opts = {
            'format': format_code,
            'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title_label.config(text=f"Title: {info.get('title', 'Unknown')}")
                ydl.download([video_url])
            messagebox.showinfo("Success", f"Download completed ({choice})!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            download_btn.config(state=tk.NORMAL)

    threading.Thread(target=run_download).start()


# --- GUI Setup ---
root = tk.Tk()
root.title("🎬 YouTube Downloader Pro")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

# Title
tk.Label(root, text="YouTube Downloader Pro", font=("Helvetica", 18, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=10)

# URL Input
tk.Label(root, text="Video URL:", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=55, font=("Helvetica", 12))
url_entry.pack(pady=5)

# Folder selection
tk.Label(root, text="Download Folder:", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
folder_frame = tk.Frame(root, bg="#1e1e2f")
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, width=40, font=("Helvetica", 12))
folder_entry.pack(side=tk.LEFT, padx=5)
folder_btn = tk.Button(folder_frame, text="Browse", command=select_folder, bg="#4caf50", fg="white", font=("Helvetica", 10))
folder_btn.pack(side=tk.LEFT)

# Options
tk.Label(root, text="Download Option:", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
var = tk.StringVar(value="video")
option_frame = tk.Frame(root, bg="#1e1e2f")
option_frame.pack(pady=5)
tk.Radiobutton(option_frame, text="Video + Audio", variable=var, value="video", bg="#1e1e2f", fg="#ffffff", selectcolor="#4caf50", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(option_frame, text="Audio Only", variable=var, value="audio", bg="#1e1e2f", fg="#ffffff", selectcolor="#4caf50", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

# Download Button
download_btn = tk.Button(root, text="Download", command=download_video, bg="#4caf50", fg="white", font=("Helvetica", 14, "bold"), width=20)
download_btn.pack(pady=15)

# Video Title
title_label = tk.Label(root, text="", bg="#1e1e2f", fg="#ffcc00", font=("Helvetica", 12))
title_label.pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="", bg="#1e1e2f", fg="#ffcc00", font=("Helvetica", 12))
status_label.pack(pady=5)

root.mainloop()

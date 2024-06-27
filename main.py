import tkinter as tk
from tkinter import messagebox,ttk
from pytube import YouTube
import os
import moviepy.editor as mp
import ctypes
import threading


myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def download_and_convert():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Uyarı", "Bir Youtube URL Girin")
        return
    
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        output_path = stream.download()
        

        progress_bar['value'] = 50
        root.update_idletasks()
        
        # Convert mp4 to mp3
        base, ext = os.path.splitext(output_path)
        mp3_path = base + '.mp3'
        
        clip = mp.AudioFileClip(output_path)
        clip.write_audiofile(mp3_path)
        clip.close()
        
        os.remove(output_path)

        progress_bar["value"] = 100
        root.update_idletasks()
        
        messagebox.showinfo("Info", f"Indirildi ve MP3'e donusturuldu: {mp3_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Bir hata olustu: {e}")
    finally:
        progress_bar['value'] = 0


    progress_bar['value'] = 0
    root.update_idletasks()
    
# main window
root = tk.Tk()
root.title("Youtube MP3 Donusturucu")
root.iconbitmap(default="favicon.ico")
root.minsize(200, 200)
root.maxsize(600, 200)

tk.Label(root, text="YouTube URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

download_button = tk.Button(root, text="Indir Ve Donustur", command=download_and_convert)
download_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=20)

root.mainloop()

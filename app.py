import os
import threading
import customtkinter as ctk
from tkinter import filedialog
from downloader import download_mp3

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube to MP3")
        self.geometry("540x270")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # URL row
        url_frame = ctk.CTkFrame(self, fg_color="transparent")
        url_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 8))
        url_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(url_frame, text="YouTube URL:", width=100, anchor="w").grid(row=0, column=0, padx=(0, 8))
        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="https://youtube.com/watch?v=...")
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ctk.CTkButton(url_frame, text="Paste", width=65, command=self._paste).grid(row=0, column=2)

        # Save-to row
        dir_frame = ctk.CTkFrame(self, fg_color="transparent")
        dir_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))
        dir_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(dir_frame, text="Save to:", width=100, anchor="w").grid(row=0, column=0, padx=(0, 8))
        self.dir_var = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        ctk.CTkEntry(dir_frame, textvariable=self.dir_var).grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ctk.CTkButton(dir_frame, text="Change", width=65, command=self._choose_dir).grid(row=0, column=2)

        # Download button
        self.download_btn = ctk.CTkButton(
            self, text="Download MP3", height=42, font=ctk.CTkFont(size=15, weight="bold"),
            command=self._start_download,
        )
        self.download_btn.grid(row=2, column=0, pady=(10, 14))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=480)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(0, 8))

        # Status label
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 20))

    def _paste(self):
        try:
            text = self.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, text.strip())
        except Exception:
            pass

    def _choose_dir(self):
        folder = filedialog.askdirectory(initialdir=self.dir_var.get())
        if folder:
            self.dir_var.set(folder)

    def _set_status(self, text, color="gray"):
        self.status_label.configure(text=text, text_color=color)

    def _on_progress(self, pct, message):
        self.after(0, lambda p=pct, m=message: (
            self.progress_bar.set(p),
            self._set_status(m),
        ))

    def _on_done(self):
        self.after(0, self._finish_success)

    def _finish_success(self):
        self.progress_bar.set(1.0)
        self._set_status("Done! MP3 saved to your folder.", "green")
        self.download_btn.configure(state="normal")

    def _on_error(self, msg):
        self.after(0, lambda m=msg: self._finish_error(m))

    def _finish_error(self, msg):
        self.progress_bar.set(0)
        self._set_status(f"Error: {msg}", "red")
        self.download_btn.configure(state="normal")

    def _start_download(self):
        url = self.url_entry.get().strip()
        output_dir = self.dir_var.get().strip()

        if not url:
            self._set_status("Please paste a YouTube URL first.", "red")
            return
        if not os.path.isdir(output_dir):
            self._set_status("Save folder not found. Please choose a valid folder.", "red")
            return

        self.download_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self._set_status("Starting...", "gray")

        threading.Thread(
            target=download_mp3,
            args=(url, output_dir, self._on_progress, self._on_done, self._on_error),
            daemon=True,
        ).start()


if __name__ == "__main__":
    App().mainloop()

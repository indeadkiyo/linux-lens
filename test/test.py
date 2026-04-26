#!/usr/bin/env python3
from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import tkinter as tk
import tkinter.messagebox as messagebox
import tempfile
import webbrowser as wb
import requests
import customtkinter as ctk
import pytesseract
import cv2
import threading
import time
import re
import pyttsx3



time = 10

screenshot = ImageGrab.grab()

# helll ya this way works much better 
#added way more then i though i would 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # base theme

class bigimagebox:
    def __init__(self, boxa):
        self.boxa = boxa
        self.boxa.attributes("-fullscreen", True)

        screen_width = self.boxa.winfo_screenwidth()
        screen_height = self.boxa.winfo_screenheight()

        self.canvas = tk.Canvas(
            self.boxa,
            width=screen_width,
            height=screen_height,
            highlightthickness=0,
            cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.focus_set()

        try:
            image = screenshot.resize((screen_width, screen_height), Image.LANCZOS)
            enhancer = ImageEnhance.Brightness(image)
            dimmed_image = enhancer.enhance(0.5)
            self.photo = ImageTk.PhotoImage(dimmed_image)

            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        except Exception as e:
            print(f"Error displaying image: {e}")
            messagebox.showerror("Image Error", f"Error processing image:\n{e}")
            self.canvas.configure(bg="black")

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.bind("<Escape>", lambda e: self.boxa.destroy())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="red",
            width=2,
        )

    def on_move_press(self, event):
        curX, curY = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        left = min(x1, x2)         
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        if right - left < 5 or bottom - top < 5:
            messagebox.showwarning(
                "Selection Too Small", "pls draw something bigger than you own high."
            )
            return

        try:
            cropped = screenshot.crop((left, top, right, bottom))

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                cropped.save(tmp.name)
                self.tempfile_path = tmp.name

            self.boxa.destroy()

        except Exception as e:
            print(f"Cropping failed: {e}")
            messagebox.showerror(
                "Cropping Error", f"hmm.... idk dude your geuss is as good as myn:\n{e}"
            )
# i dont know that will about gui so gpt helped make the gui look nicer all the extra
# that make this look good way better then i made (windows xp) is by my bro gpt

class bluat:
    def __init__(self, root, img_path):
        self.root = root
        self.img_path = img_path

        self.tts_engine = pyttsx3.init()

        self.root.geometry("700x700")
        self.root.title("ScreenSearch")
        self.root.configure(fg_color="#1e1e2e")

        # ===== GRID LAYOUT =====
        self.root.grid_rowconfigure(1, weight=1)  # main area expands
        self.root.grid_columnconfigure(0, weight=1)

        # ===== TOOLBAR =====
        self.toolbar = ctk.CTkFrame(self.root, fg_color="#181825", height=40)
        self.toolbar.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(
            self.toolbar,
            text="🔍 Search",
            command=self.search,
            fg_color="#89b4fa",
            hover_color="#74c7ec",
            width=100
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            self.toolbar,
            text="💬 OCR",
            command=self.ocr,
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            width=100
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            self.toolbar,
            text="speech",
            command=self.speech,
            fg_color="#FFF200",
            hover_color="#9C9207",
            width=100
        ).pack(side="left",padx=5,pady=5)

        ctk.CTkButton(
            self.toolbar,
            text="🧹 Clear",
            command=self.clear_text,
            fg_color="#f38ba8",
            hover_color="#eba0ac",
            width=100
        ).pack(side="left", padx=5, pady=5)

        # main
        self.main = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main.grid(row=1, column=0, sticky="nsew")

        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        # Image preview
        img = Image.open(self.img_path)
        self.ctk_img = ctk.CTkImage(img, size=(700, 300))

        self.image_label = ctk.CTkLabel(
            self.main,
            image=self.ctk_img,
            text="",
        )
        self.image_label.grid(row=0, column=0, pady=10)

        # Textbox (main content)
        self.textbox = ctk.CTkTextbox(
            self.main,
            fg_color="#1a1b26",
            text_color="#c0caf5",
            corner_radius=10
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.textbox.configure(font=("JetBrains Mono", 12))

        # ===== STATUS BAR =====
        self.status = ctk.CTkLabel(
            self.root,
            text="Ready",
            anchor="w",
            fg_color="#181825",
            height=25
        )
        self.status.grid(row=2, column=0, sticky="ew")


    def search(self):
        confirm = messagebox.askyesno(
            "Upload Image",
            "This will upload your image to an external server. Continue?"
        )

        if confirm:
            self.status.configure(text="Uploading for search...")
            YesImageMe(self.img_path)
            self.status.configure(text="Opened in browser")

    def ocr(self):
        self.status.configure(text="Running OCR...")
        threading.Thread(target=self._ocr_worker, daemon=True).start()

    def _ocr_worker(self):
        text = textmebro(self.img_path)
        text = format_text(text)
        self.root.after(0, self._update_textbox, text)

    def _update_textbox(self, text):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self.status.configure(text="OCR complete")

    def clear_text(self):
        self.textbox.delete("1.0", "end")
        self.status.configure(text="Cleared")
    
    def _speak_worker(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
        self.root.after(0, lambda: self.status.configure(text="Done speaking"))


    def speech(self):
        text = self.textbox.get("1.0", "end").strip()

        if not text:
            self.status.configure(text="No text to read")
            return

        self.status.configure(text="Speaking...")
        threading.Thread(target=self._speak_worker, args=(text,), daemon=True).start()

class YesImageMe:
    def __init__(self, img_path):
        self.img_path = img_path

        self.url = "https://tmpfiles.org/api/v1/upload"
        responses = requests.post(self.url, files={"file": open(self.img_path, "rb")})

        data = responses.json()
        url = data["data"]["url"]
        direct_url = url.replace("http://tmpfiles.org/", "https://tmpfiles.org/dl/")
        print(direct_url)

        link = f"https://imgops.com/{direct_url}"
        wb.open(link)

def textmebro(img_path):
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError("Image not found")

    #upscale (helps ocr a lot)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #grayscale + blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    #threshold
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    #ocr
    text = pytesseract.image_to_string(
        thresh,
        config="--oem 3 --psm 6"
    )

    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'[ \t]+', ' ', text)

    lines = text.split('\n')

    return text.strip()

def format_text(text):
    lines = text.split('\n')
    formatted = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith(('-', '*', '•')):
            formatted.append(f"• {line[1:].strip()}")
        else:
            formatted.append(line)

    return '\n'.join(formatted)

if __name__ == "__main__":
    boxa = tk.Tk()
    selector = bigimagebox(boxa)   
    boxa.mainloop()

    if hasattr(selector, "tempfile_path"):
        root = ctk.CTk()
        ui = bluat(root, selector.tempfile_path)  
        root.mainloop()
    else:
        print("No image selected — nothing to upload.")



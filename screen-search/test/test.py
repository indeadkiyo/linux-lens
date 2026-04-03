#!/usr/bin/env python3
from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import tkinter as tk
import tkinter.messagebox as messagebox
import tempfile
import webbrowser as wb
import requests
import easyocr

screenshot = ImageGrab.grab()
ocr_reader = None

# helll ya this way works much better then that blooted mess of a code

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
                "Selection Too Small", "pls draw something bigger than you high."
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

class bluat:
    def __init__(self, root, img_path):
        self.root = root
        self.img_path = img_path

        self.root.geometry("600x600")

        tk.Button(root, text='🔍', command=self.search).pack()
        tk.Button(root, text='💬', command=self.ocr).pack()

    def search(self):
        YesImageMe(self.img_path)

    def ocr(self):
        textmebro(self.img_path)


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

class textmebro:
    def __init__(self, img_path):
        self.reader = easyocr.Reader(['ch_sim','en'])
        self.result = self.reader.readtext(img_path)

        text = "\n".join([r[1] for r in self.result])
        print(text)

if __name__ == "__main__":
    boxa = tk.Tk()
    selector = bigimagebox(boxa)   
    boxa.mainloop()

    if hasattr(selector, "tempfile_path"):
        root = tk.Tk()
        ui = bluat(root, selector.tempfile_path)  
        root.mainloop()
    else:
        print("No image selected — nothing to upload.")

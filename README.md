# linux-lens

![Under Construction GIF](https://media.tenor.com/42bcTn0iuVgAAAAj/under-construction-pikachu.gif)

> the Android  Circle to Search. is really usefull so i wanted one for my linux to
:
> made it to work with any distro since mostly relay on py and not system api's
:
> the code is open so if there is bugs or etc you can modify it yourself or tell me and i can try to fix it 
---
## What this is:

A desktop app that lets you:
1. Draw a  little rectangle on your screen
2. Either **search** what's inside or run **OCR** to get the text (ps:offline so use that for privet stuff)
Built because I wanted to learn. Also because I'm too lazy to type text on images myself.
---

##  Features (that actually work... mostly)

- Search via ImgOps | ✅
- OCR text extraction | ✅ 
- Dark mode | ✅ |there only dark mode|
- speech to text | ❌
- Translator | ❌ | future me's problem |

---

##  What you need installed (no skipping)
- Python
- Poetry (https://python-poetry.org/)
- (ps: if you want you can set up all the packages yourself but poetry makes it a little easer)
- pyTesseract (the OCR brain)
- linux (idk if you experienced this problem but if you see a error based on tk then install tkinter in your os)

**This is required. your lap is lazy without it.**

```bash
# macOS (bless your heart)
brew install tesseract

# Ubuntu/Debian
sudo apt install tesseract-ocr
(or search your tesseract arch or fedora online you get the package name)

# Windows (my condolences)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH or we'll have problems
```

### 3. Python packages (handled by poetry but here's the list)
```
customtkinter
Pillow
pytesseract
opencv-python
requests
```
---
## dev :

## 🐛 Known bugs (aka: im to lazy to fix )

- Tesseract sometimes is not really good at formatting
- code is not pritty
- idk how it even runs at this  point it just does
- there a timer in the test file to test stuff so if you want it to work instant remove that
- not good for copying code from image or format's like that since may goal was to make it lightwaight i had to give up on accuracy a little 
---

---

##  Credits

- **Me** – for the bad ideas and worse code
- **GPT** – for fixing my GUI so it doesn't look like Windows XP
- **tea** – for existing
- **Ikaros** – go watch  Heaven's Lost Property you will know what i mean its peak  

---

## License

Do whatever you want. Learn from it. Break it. Fix it. Make it better.  
Just don't blame me if it didnt work
---

![hola](https://media1.tenor.com/m/ps-qhH6Wea4AAAAd/heavens-lost-property.gif)


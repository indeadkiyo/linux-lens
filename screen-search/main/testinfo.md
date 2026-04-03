thanks gpt for this

[Start Program]
       |
       v
[Tkinter GUI opens full-screen screenshot]
       |
       v
[User draws rectangle on screen]
       |
       v
[Mouse button released → crop selection]
       |
       v
[Crop the screenshot according to rectangle]
       |
       v
[Save cropped image to TEMP FILE]
       |  (stored in: app.tempfile_path)
       v
[GUI closes (boxa.mainloop() ends)]
       |
       v
[Check if temp file exists]
       |  (hasattr(app, "tempfile_path"))
       |--No--> [Skip upload, print "No image selected"]
       |
       Yes
       |
       v
[Instantiate YesImageMe(tempfile_path)]
       |
       v
[Open temp file in binary mode ("rb")]
       |
       v
[Send POST request to tmpfiles.org with file]
       |
       v
[Server responds with JSON data]
       |
       v
[Extract uploaded image URL: data["data"]["url"]]
       |
       v
[Print URL → can send to another site / use anywhere]
       |
       v
[End]

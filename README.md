# A python interface for V4L2 webcam
By using the `webcam` module, you can interact with a webcam device.

```python
from webcam import WebCam

# open and set /dev/video0
camera = WebCam(0)
camera.open()

# capture a frame of picture and save it
content = camera.capture()
with open("image.jpg", "wb") as f:
    f.write(content)

camera.close()
```

You also have access to some controls like brightness, contrast and so on.

```python
print(camera.controls["brightness"])
camera.controls["contrast"] += 1
```

`example.py` provide a GUI to view pictures captured by webcam.

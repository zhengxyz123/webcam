from io import BytesIO

from pyglet import app
from pyglet import clock
from pyglet.image import load as load_image
from pyglet.sprite import Sprite
from pyglet.window import Window

from webcam import WebCam

class ExampleWindow(Window):
    def __init__(self):
        super().__init__(width=640, height=480, caption="webcam")
        self.webcam = WebCam(0)
        pic = BytesIO(self.webcam.capture())
        img = load_image("image.jpg", pic)
        self.sprite = Sprite(img)
        clock.schedule_once(self._update, 1 / 60)

    def on_close(self):
        self.webcam.close()
        self.close()

    def on_draw(self):
        self.clear()
        self.sprite.draw()

    def _update(self, dt):
        pic = BytesIO(self.webcam.capture())
        img = load_image("image.jpg", pic)
        self.sprite.image = img
        clock.schedule_once(self._update, 1 / 60)


if __name__ == "__main__":
    win = ExampleWindow()
    clock.schedule_interval(win.draw, 1 / 60)
    app.run()

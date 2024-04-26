from io import BytesIO

from pyglet import app, clock
from pyglet.image import load as load_image
from pyglet.window import Window, key

from webcam import WebCam


class ExampleWindow(Window):
    def __init__(self):
        super().__init__(width=640, height=480, caption="webcam")
        self.webcam = WebCam(0)
        pic = BytesIO(self.webcam.capture())
        self.image = load_image("image.jpg", pic)
        clock.schedule_once(self._update, 1 / 30)

    def on_close(self):
        self.webcam.close()
        self.close()

    def on_draw(self):
        self.clear()
        self.image.blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.B:
            if modifiers & key.LSHIFT:
                self.webcam["brightness"] -= 1
            else:
                self.webcam["brightness"] += 1
        elif symbol == key.C:
            if modifiers & key.LSHIFT:
                self.webcam["contrast"] -= 1
            else:
                self.webcam["contrast"] += 1
        elif symbol == key.G:
            if modifiers & key.LSHIFT:
                self.webcam["gamma"] -= 1
            else:
                self.webcam["gamma"] += 1
        elif symbol == key.S:
            if modifiers & key.LSHIFT:
                self.webcam["sharpness"] -= 1
            else:
                self.webcam["sharpness"] += 1

    def _update(self, dt):
        pic = BytesIO(self.webcam.capture())
        self.image = load_image("image.jpg", pic)
        clock.schedule_once(self._update, 1 / 30)


if __name__ == "__main__":
    win = ExampleWindow()
    clock.schedule_interval(win.draw, 1 / 60)
    app.run()

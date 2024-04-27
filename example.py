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
        self.keyhandler = key.KeyStateHandler()
        self.push_handlers(self.keyhandler)
        clock.schedule_once(self._update, 1 / 30)

    def on_close(self):
        self.webcam.close()
        self.close()

    def on_draw(self):
        self.clear()
        self.image.blit(0, 0)

    def _update(self, dt):
        ctrl = "none"
        if self.keyhandler[key.B]:
            ctrl = "brightness"
        elif self.keyhandler[key.C]:
            ctrl = "contrast"
        elif self.keyhandler[key.G]:
            ctrl = "gamma"
        elif self.keyhandler[key.S]:
            ctrl = "sharpness"

        delta = 0
        if self.keyhandler[key.UP]:
            delta = 1
        elif self.keyhandler[key.DOWN]:
            delta = -1

        if ctrl != "none":
            self.webcam.controls[ctrl] += delta

        pic = BytesIO(self.webcam.capture())
        self.image = load_image("image.jpg", pic)
        clock.schedule_once(self._update, 1 / 30)


if __name__ == "__main__":
    win = ExampleWindow()
    clock.schedule_interval(win.draw, 1 / 60)
    app.run()

from pyglet import app, clock
from pyglet.sprite import Sprite
from pyglet.window import Window, key

from webcam import WebCam


class ExampleWindow(Window):
    def __init__(self):
        super().__init__(width=640, height=480, caption="webcam", resizable=True)

        self.webcam = WebCam(0)
        self.webcam.open()

        image = self.webcam.capture()
        image.anchor_x, image.anchor_y = image.width // 2, image.height // 2
        self.sprite = Sprite(image)

        self.keyhandler = key.KeyStateHandler()
        self.push_handlers(self.keyhandler)

    def on_close(self):
        self.webcam.close()
        self.close()

    def on_draw(self):
        self.clear()
        self.sprite.draw()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        w_img, h_img = self.sprite.image.width, self.sprite.image.height
        if self.width * h_img < self.height * w_img:
            self.sprite.scale = self.width / w_img
        else:
            self.sprite.scale = self.height / h_img
        self.sprite.position = (width // 2, height // 2, 0)

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

        image = self.webcam.capture()
        image.anchor_x, image.anchor_y = image.width // 2, image.height // 2
        self.sprite.image = image
        clock.schedule_once(self._update, 1 / 30)


if __name__ == "__main__":
    win = ExampleWindow()
    clock.schedule_interval(win.draw, 1 / 60)
    clock.schedule_once(win._update, 1 / 30)
    app.run()

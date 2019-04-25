from PIL import Image, ImageFilter

class Action():
    def __init__(self, app, img, log):
        self.app = app
        self.img = img
        self.log = log

    def stack(self):
        self.app.undo_stack.append(self)

    def restore(self):
        self.app.restoreImage(self.img)
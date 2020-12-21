from toga.widgets.base import Widget

class CameraFeed(Widget):
    def __init__(self, image=None, id=None, style=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.CameraFeed(interface=self)

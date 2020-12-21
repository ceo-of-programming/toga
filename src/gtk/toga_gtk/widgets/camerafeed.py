from ..libs.gtk import Gtk, Gst, GstVideo, GdkX11
from .base import Widget

class CameraFeed(Widget):
    def create(self):
        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface
        
        self.pipeline = Gst.parse_launch("v4l2src ! autovideosink")

        # Get events from the Gstreamer pipeline
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', self.on_eos)
        bus.connect('message::error', self.on_error)

        # Draw the video frames on the drawing area.
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

        self.pipeline.set_state(Gst.State.PLAYING)

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_property('force-aspect-ratio', True)
            self.native.realize()
            window = self.native.get_window()
            msg.src.set_window_handle(window.get_xid())


    def on_eos(self, bus, msg):
        self.pipeline.set_state(Gst.State.NULL)

    def on_error(self, bus, msg):
        error, debug = msg.parse_error()
        print("Error: {s}".format(s=error), debug)
        self.pipeline.set_state(Gst.State.NULL)


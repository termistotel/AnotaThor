from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty

class ToggleButtonAlt(ToggleButton):
	stateAlt = StringProperty("normal")
	toggleFunction = lambda *x: x

	def __init__(self, *args, **kwargs):
		super(ToggleButtonAlt, self).__init__(*args, **kwargs)

	def on_state(self, *args):
		self.toggleFunction(*args)


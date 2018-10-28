from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class ToolbarContainer(BoxLayout):
  pass

class AnotationSelect(Button):
  def __init__(self, **kwargs):
    super(AnotationSelect, self).__init__(**kwargs)

    dropdown = DropDown()
    for index in range(10):
      btn = Button(text='Value %d' % index, size_hint_y=None, height=44)
      btn.bind(on_release=lambda btn: dropdown.select(btn.text))
      dropdown.add_widget(btn)

    dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
    self.dropdown = dropdown

  def on_release(self, *args, **kwargs):
    self.dropdown.open(self, *args, **kwargs)

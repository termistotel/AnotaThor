from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

from functools import partial

class ToolbarContainer(BoxLayout):
  pass

class DropDownItem(ButtonBehavior, Label):
  def __init__(self, *args, **kwargs):
    super(DropDownItem, self).__init__(*args, **kwargs)

class AnotationSelect(Button):
  pipeSelectedValue = lambda *x: x

  def __init__(self, **kwargs):
    super(AnotationSelect, self).__init__(**kwargs)

    dropdown = DropDown()

    landmarkSelect = DropDownItem(text='Landmark', size_hint_y=None, height=44)
    landmarkSelect.bind(on_release = partial(self.select, landmarkSelect.text))

    lineSelect = DropDownItem(text='Line', size_hint_y=None, height=44)
    lineSelect.bind(on_release = partial(self.select, lineSelect.text))

    dropdown.add_widget(landmarkSelect)
    dropdown.add_widget(lineSelect)

    dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))
    self.dropdown = dropdown

  def select(self, value, *args, **kwargs):
    self.dropdown.select(value)
    self.pipeSelectedValue(value)

  def on_release(self, *args, **kwargs):
    self.dropdown.open(self, *args, **kwargs)

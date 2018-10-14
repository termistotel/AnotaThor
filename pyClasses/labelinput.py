from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class LabelInput(BoxLayout):
   def __init__(self, *args, **kwargs):
      super(LabelInput,self).__init__(*args,**kwargs)

      self.orientation='horizontal'
      self.size_hint=[0.11,0.025]

      self.newLabel=TextInput()
      self.newLabel.size_hint=[0.7, 1]
      self.newLabel.font_size=18
      self.add_widget(self.newLabel)

      self.newButton=Button()
      self.newButton.text="Save"
      self.newButton.size_hint=[0.3, 1]
      self.newButton.font_size=16

      self.add_widget(self.newButton)

# class LabelInput(TextInput):
#   def __init__(self, *args, **kwargs):
#     super(LabelInput,self).__init__(*args, **kwargs)
#     print("Ovdje mi printa",self.size_hint)

#     self.size_hint=[0.09,0.025]
#     self.font_size=18
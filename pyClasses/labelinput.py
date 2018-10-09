from kivy.uix.textinput import TextInput

class LabelInput(TextInput):
  def __init__(self, *args, **kwargs):
    super(LabelInput,self).__init__(*args, **kwargs)
    print("Ovdje mi printa",self.size_hint)

    self.size_hint=[0.09,0.025]
    self.font_size=18
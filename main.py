import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from pyClasses.mainbox import MainBox

class AnotathorApp(App):
  def build(self):
    mainbox = MainBox()
    return mainbox

if __name__ == '__main__':
    AnotathorApp().run()
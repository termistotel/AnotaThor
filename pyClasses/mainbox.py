import os
from functools import partial

from pyClasses.displaylayout import DisplayLayout
from pyClasses.toolbar import ToolbarContainer
from pyClasses.buttons import ToggleButtonAlt
from pyClasses.scaler import Scaler

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

def cleanTouchDown(fun, scroll):
  def tmp(touch):
    if touch.is_mouse_scrolling:
      return scroll(touch)
    else:
      return fun(touch)
  return tmp

def appendFuns(*funs):
  def tmp(*args, **kwargs):
    for fun in funs:
      ret = fun(*args, **kwargs)
    return ret
  return tmp

class KeyBoardHandler():
  def __init__(self, widget, mode):
    self.keyboard = Window.request_keyboard(self.closeKeyboard, widget, mode)
    self.keyboard.bind(on_key_down=self.on_key_down)
    self.keyboard.bind(on_key_up=self.on_key_up)
    self.downActions = []

  def closeKeyboard(self):
    self.keyboard.unbind(on_key_down=self.on_key_down)
    self.keyboard.unbind(on_key_up=self.on_key_up)
    self.keyboard = None

  def addShortkey(self, keys, function):
    self.downActions.append((keys, function))

  def on_key_down(self, keyboard, keycode, text, modifiers):
    for keys, fun in self.downActions:
      if set(keys) == set([keycode[1]]+modifiers):
        fun()

  def on_key_up(self, keyboard, keycode):
    pass
  #   for keys, fun in self.downActions:
  #     if set(keys) == set([keycode[1]]):
  #       fun()

class MainBox(BoxLayout):
  def __init__(self, **kwargs):
    super(MainBox, self).__init__(**kwargs)

    self.previousList = []
    self.nextList = []

    # References to main widgets
    displayLayout = self.ids.display
    annotationParent = displayLayout.newImage
    reloadButton = self.ids.reload
    nextButton = self.ids.next
    prevButton = self.ids.prev
    dragButton = self.ids.drag
    insertButton = self.ids.insert
    saveButton = self.ids.save
    deleteButton = self.ids.deleteToggle
    clearButton = self.ids.clearall
    anotationSelect = self.ids.anotationselect

    # Annotation parent's on_touch_down modes
    dragFunction = cleanTouchDown(annotationParent.on_touch_down, self.on_mouse_scroll)
    insertFunction =  cleanTouchDown(appendFuns( annotationParent.on_touch_down, partial(self.addAnnotation, annotationParent) ), self.on_mouse_scroll)
    deleteFunction = cleanTouchDown(annotationParent.on_touch_down, self.on_mouse_scroll)
    defaultFunction = dragFunction

    # ToggleButton toggler functions
    dragButton.toggleFunction = partial(self.toggleMouseFunction, annotationParent, dragFunction, defaultFunction)
    insertButton.toggleFunction = partial(self.toggleMouseFunction, annotationParent, insertFunction, defaultFunction)
    deleteButton.toggleFunction = partial(self.annotationSuicideModeToggle, annotationParent)

    # Button operations
    reloadButton.on_press = self.updateImageList
    nextButton.on_press = self.nextImage
    prevButton.on_press = self.prevImage
    saveButton.on_press = partial(self.saveAnnotations, annotationParent)
    clearButton.on_press = partial(self.clearAnnotations, annotationParent)

    # Dropdown select operations
    anotationSelect.pipeSelectedValue = displayLayout.changeAnnotationType

    # Starting states
    insertButton.state = "down"
    reloadButton.on_press()
    anotationSelect.select("Landmark")
    self.ids.annotationsize.annotationParent = annotationParent

    # Property bindings
    annotationParent.bind(children=self.anotationNumberDisplay)

    # Keyboard request and hotkey bindings
    def modeToggle(button):
      # First deactivate all other modes
      for but in ToggleButtonAlt.get_widgets("modeSelect"):
        if but != button:
          but.state="normal"
      # Activate target mode
      button.state="down"

    self.kbh = KeyBoardHandler(self, 'text')
    self.kbh.addShortkey(['1'], partial(modeToggle, dragButton))
    self.kbh.addShortkey(['2'], partial(modeToggle, insertButton))
    self.kbh.addShortkey(['3'], partial(modeToggle, deleteButton))
    self.kbh.addShortkey(['s'], saveButton.on_press)
    self.kbh.addShortkey(['a'], prevButton.on_press)
    self.kbh.addShortkey(['d'], nextButton.on_press)

  def on_mouse_scroll(self, touch):
    if touch.button == 'scrolldown':
      value = -0.01
    elif touch.button == "scrollup":
      value = 0.01
    else:
      return

    annotationParent = self.ids.display.newImage
    for child in annotationParent.children:
      if child.collide_point(*touch.pos):
        child.scroll_to(value)
        return


  def anotationNumberDisplay(self, object, children):
    self.ids.anotationnumber.text=str(len(children))

  def clearAnnotations(self, annotationParent, *args, **kwargs):
    for child in list(annotationParent.children):
      annotationParent.remove_widget(child)
      del child

  def saveAnnotations(self, annotationParent, *args, **kwargs):
    with open('annotations.json', 'a') as saveFile:
      jsonString = self.ids.display.saveAnnotations(self.nextList[len(self.nextList)-1], annotationParent)
      saveFile.write(jsonString)
      saveFile.write("\n")

  def addAnnotation(self, annotationParent, touch, *args, **kwargs):
    self.ids.display.addAnnotation(annotationParent, self.ids.annotationsize, touch, *args, **kwargs)

  def annotationSuicideModeToggle(self, annotationParent, *args, **kwargs):
    self.ids.display.annotationSuicideModeToggle(annotationParent, *args, **kwargs)

  def toggleMouseFunction(self, widget, function1, function2,  *args, **kwargs):
    if widget.on_touch_down == function1:
      widget.on_touch_down = function2
    else:
      widget.on_touch_down = function1

  def updateImageList(self, *args, **kwargs):
    self.nextList = os.listdir('images/')
    self.previousList = []
    self.nextList.sort(reverse=True)
    self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

  def nextImage(self, *args, **kwargs):
    if len(self.nextList) > 1:
      self.previousList.append(self.nextList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

  def prevImage(self, *args, **kwargs):
    if len(self.previousList) >=1:
      self.nextList.append(self.previousList.pop())
      self.ids.display.changeImg('images/' + self.nextList[len(self.nextList)-1])

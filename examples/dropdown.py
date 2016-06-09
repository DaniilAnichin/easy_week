from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

# create a drop_down with 10 buttons
dropdown = DropDown()
for index in range(10):
    # when adding widgets, we need to specify the height manually (disabling
    # the size_hint_y) so the drop_down can calculate the area it needs.
    btn = Button(text='Value %d' % index, size_hint_y=None, size_hint_x=None,
                 pos_hint_x=0, width=300, height=44)

    # for each button, attach a callback that will call the select() method
    # on the drop_down. We'll pass the text of the button as the data of the
    # selection.
    btn.bind(on_release=lambda btn: dropdown.select(btn.text))

    # then add the button inside the drop_down
    dropdown.add_widget(btn)

# create a big main button
mainbutton = Button(text='Hello', size_hint=(None, None))

# show the drop_down menu when the main button is released
# note: all the bind() calls pass the instance of the caller (here, the
# mainbutton instance) as the first argument of the callback (here,
# drop_down.open.).
mainbutton.bind(on_release=dropdown.open)

# one last thing, listen for the selection in the drop_down list and
# assign the data to the button text.
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

runTouchApp(mainbutton)
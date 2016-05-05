import kivy
kivy.require('1.0.8')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class ScrollViewApp(App):

    def build(self):
        box = BoxLayout(orientation='vertical')
        # create a default grid layout with custom width/height
        layout = GridLayout(cols=1, padding=10, spacing=10,
                            size_hint=(None, None), width=500)

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required to
        # contain all the childs. (otherwise, we'll child outside the bounding
        # box of the childs)
        layout.bind(minimum_height=layout.setter('height'))

        # add button into that grid
        for i in range(30):
            btn = Button(text=str(i), size=(480, 40),
                         size_hint=(None, None))
            layout.add_widget(btn)

        # create a scroll view, with a size < size of the grid
        root = ScrollView(
                          pos_hint={'top': 1.0, 'left': 1.0})
        root.add_widget(layout)
        b = Button(text='gyumkiu', size=(480, 40),
                   size_hint=(None, None)
                   )
        box.add_widget(b)
        box.add_widget(root)
        return box

if __name__ == '__main__':

    ScrollViewApp().run()


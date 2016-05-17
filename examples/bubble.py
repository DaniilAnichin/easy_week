#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.app import App


class MyBubbleApp(App):
    def build(self):
        root = GridLayout()
        layout = FloatLayout(orientation='horizontal',
                             size=(150, 100),
                             size_hint=(None, None))
        my_btn = Button(text='Press to view bubble',
                        pos=(300, 300),
                        on_press=show_bubble)
        layout.add_widget(my_btn)
        root.add_widget(layout)
        return root


def show_bubble(self, *args):
        my_bubble = Bubble(orientation='horizontal', pos=(280, 400))
        # Customizing my bubble
        my_bubble.background_color = (0, 0, 0, .5)
        my_bubble.border = [50, 50, 50, 10]
        my_bubble.arrow_pos = 'top_left'
        my_bub_btn1 = BubbleButton(text='Copy',
                                   size_hint=(None, None),
                                   size=(80, 50),
                                   pos=(200, 400))
        my_bub_btn2 = BubbleButton(text='Cut',
                                   size_hint=(None, None),
                                   size=(80, 50),
                                   pos=(300, 400))
        my_bub_btn3 = BubbleButton(text='Paste',
                                   size_hint=(None, None),
                                   size=(80, 50),
                                   pos=(300, 400))
        # Add items to bubble
        my_bubble.add_widget(my_bub_btn1)
        my_bubble.add_widget(my_bub_btn2)
        my_bubble.add_widget(my_bub_btn3)
        self.add_widget(my_bubble)


if __name__ == '__main__':
    MyBubbleApp().run()
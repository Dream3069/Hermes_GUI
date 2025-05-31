import matplotlib.pyplot as plt
import pandas as pd
import os
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ColorProperty

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')

from list_akt import get_all_trading_symbols
from grahic_ch import plot_candlestick
from portfely import ii
from helper import TradingHelper
Builder.load_string("""

<Test>:
    do_default_tab: False
    TabbedPanelItem:
        text: 'page1'
        ScrollView:
            Table:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: 50, 50, 50, 50
    TabbedPanelItem:
        text: 'партфель'
        You1:
<You>:
    orientation: "vertical"
    BoxLayout:
        size_hint: (1, .1)
        Label:
            text: ''
            id: name
            multiline: False
        Button:
            text: 'exit'
            color: 1,0,0,1
            background_color: 0,0,0,0
            size_hint: (.2, .2)
            pos_hint:{"right":.9, "top":.6}
            on_press: root.exit()
    ScrollView:
        Table_my:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: 50, 50, 50, 50


<Row>:
    spacing: 50
    size_hint_y: None
    size_hint_x: 1
    height: 100
    padding: 20
    Label:
        text: root.txt 
        id: name
        multiline: False
    Label:
        text: root.buy_sell
        id: tf
        multiline: False
    Label:
        text: root.profit 
        color: root.color
        id: profit
        multiline: False
    Button:
        text: 'больше'
        on_press: root.open()
<Rows>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: akk
            multiline: False
            orientation: 'vertical'
            BoxLayout:
                size_hint: (1, .2)
                Label:
                    text: root.txt 
                    id: name
                    multiline: False
                Button:
                    text: 'X'
                    color: 1,0,0,1
                    background_color: 0,0,0,0
                    size_hint: (.2, .2)
                    pos_hint:{"right":1, "top":.9}
                    on_press: root.return1()
        BoxLayout:
            spacing: 50
            size_hint_y: None
            size_hint_x: 1
            height: 100
            padding: 20
            Button:
                text: 'купить'
                on_press: root.buy(root.ak)
            Button:
                text: 'продать'
                on_press: root.sell(root.ak)

<HelloWidget>:
    orientation: 'vertical'
    padding: 20
    spacing: 20
    size_hint: (.5, .6)
    pos_hint:{"center_x":0.5, "top":1}
    name_input: name
    password_input: password
    TextInput:
        id: name
        size_hint: (1, .4)
        multiline: False
    TextInput:
        id: password
        size_hint: (1, .4)
        multiline: False
    Button:
        text: 'Войти'
        background_color: 'green'
        on_press: root.say_hello()

""")
txt1 = ''  # логин (сам меняется)

api_key = os.getenv('12cfLqsr1J72rSAUIe')
api_secret = os.getenv('JKVgRkBOMh6iEJJziAIIHvCAIoa0xmosG1S0')
lst_ak = get_all_trading_symbols(api_key, api_secret, testnet=True)  # названия акций всех
lst_ak = lst_ak.get("spot", [])[:6]
lst_ak_my = ['BTCUSDT']  # названия акций в твоём партфеле


def DataFrame_pd(name):  # вывод по названию акции график
    stock_prices = plot_candlestick(name, interval=15, count=20)
    profit = -9
    print(stock_prices)
    return stock_prices, profit


def all_pd(lst):
    for x in range(len(lst)):
        n, h = DataFrame_pd(lst[x])
        lst[x] = [lst[x], n, h]
    return lst


class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        for row in range(len(lst_ak)):
            print(lst_ak[row])
            self.add_widget(Row(lst_ak[row][0],lst_ak[row][1],lst_ak[row][2]))

    def A_Z(self, a_z=False):
        print(111111)
        lst_ak.sort(reverse=a_z)
        self.clear_widgets()
        for row in range(len(lst_ak)):
            print(lst_ak[row])
            self.add_widget(Row(lst_ak[row][0],lst_ak[row][1],lst_ak[row][2]))


class Table_my(BoxLayout):
    def __init__(self, **kwargs):
        super(Table_my, self).__init__(**kwargs)
        for row in range(len(lst_ak_my)):
            print(lst_ak_my[row])
            self.add_widget(Row(lst_ak[row][0],lst_ak[row][1],lst_ak[row][2]))


class You1(BoxLayout):
    def __init__(self, **kwargs):
        super(You1, self).__init__(**kwargs)
        self.add_widget(You(txt1))


class You(BoxLayout):
    def __init__(self, txt, **kwargs):
        super(You, self).__init__(**kwargs)
        self.ids.name.text = 'логин ' + txt + "\n ваш портфель"

    def exit(self):
        sm.clear_widgets()
        sm.add_widget(screen0())


class Row(BoxLayout):
    txt = StringProperty()
    buy_sell = StringProperty()
    profit = StringProperty()
    color = ColorProperty()

    def __init__(self, name,grafic,profit, **kwargs):
        super(Row, self).__init__(**kwargs)
        profit = 0
        self.txt = str(name)
        self.grafic = grafic
        self.profit = str(profit) + ' %'
        if profit > 0:
            self.color = 0, 1, 0, 1
        elif profit < 0:
            self.color = 1, 0, 0, 1
        g = TradingHelper().start(name)

        if g==1:
            self.buy_sell = 'рекомендуем к продаже'
        elif g==-1:
            self.buy_sell = 'рекомендуем к покупке'
        else:
            self.buy_sell = 'ожидать'

    def open(self):
        scren2 = sm.get_screen('2')
        scren2.clear_widgets()
        scren2.reRows(self.txt, self.grafic)
        sm.current = '2'
        return 0


def plot_grafic(grafic):
    up = grafic[grafic.close >= grafic.open]

    down = grafic[grafic.close < grafic.open]

    col1 = 'red'

    col2 = 'green'

    width = 0.4
    width2 = 0.05
    plt.close()
    plt.bar(up.index, up.close - up.open, width, bottom=up.open, color=col2)
    plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col2)
    plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col2)

    plt.bar(down.index, down.close - down.open, width, bottom=down.open, color=col1)
    plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col1)
    plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col1)
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    plt.gcf().set_facecolor("black")


class Test(TabbedPanel):
    pass


class screen0(Screen):
    def __init__(self):
        super().__init__()
        self.name = '0'
        self.add_widget(HelloWidget())


class screen1(Screen):
    def __init__(self):
        super().__init__()
        self.name = '1'
        self.add_widget(Test())


class screen2(Screen):
    def __init__(self):
        super().__init__()
        self.name = '2'

    def reRows(self, txt, grafic):
        self.add_widget(Rows(txt, grafic))


class Rows(BoxLayout):
    txt = StringProperty()

    def __init__(self, txt, grafic, **kwargs):
        super(Rows, self).__init__(**kwargs)
        self.txt = txt
        self.grafic = grafic
        plot_grafic(self.grafic)
        box = self.ids.akk
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def duy(self):
        pass

    def sell(self):
        pass

    def return1(self):
        sm.current = '1'


class HelloWidget(BoxLayout):
    name_input = ObjectProperty()
    password_input = ObjectProperty()

    def say_hello(self):
        global txt1
        if self.name_input.text != "" and self.password_input.text != "":
            II = ii()
            II.main(self.name_input.text, self.password_input.text)
            print(self.name_input.text, self.password_input.text)  # логин и пароль
            txt1 = self.name_input.text
            sm.add_widget(screen1())
            sm.add_widget(screen2())
            sm.current = '1'


sm = ScreenManager()


class MyApp(App):
    def build(self):
        sm.add_widget(screen0())
        return sm


if __name__ == '__main__':
    lst_ak = all_pd(lst_ak)
    lst_ak_my = all_pd(lst_ak_my)
    myapp = MyApp()
    myapp.run()
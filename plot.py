"""all flight statistical plot module use"""
import matplotlib, pandas as pd
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from datetime import datetime
import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent, df):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.RIGHT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def show_airlines(self, df):
        ax = df.Carrier.groupby(df.Carrier).count().sort_values(ascending = False).head(8).plot(
            ax = self.axes, kind = "barh", fontsize = 8, grid = False, legend = False)
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y() + .1,
                    str(round((i.get_width()), 2)), fontsize=10, color='black')

    def continent(self, df):
        ax = df.Continent.groupby(df.Continent).count().plot.barh(ax=self.axes, fontsize = 8, grid = False, legend = False)
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y() + .1,
                    str(round((i.get_width()), 2)), fontsize=10, color='black')

    def airleague(self, df):
        df.League.groupby(df.League).count().plot(kind='pie', ax=self.axes, autopct='%1.1f%%', startangle=0, shadow=False)

    def city(self, df):
        ax = df.groupby(['City', 'Country']).size().sort_values(ascending=False).head(8).plot(
            ax = self.axes, kind = "barh",fontsize = 8, grid = False)
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y() + .1,
                    str(round((i.get_width()), 2)), fontsize=10, color='black')

    def airport(self, df):
        ax = df.AirportIATA.groupby(df.AirportIATA).count().sort_values(ascending=False).head(10).plot(
            ax=self.axes, fontsize=8, grid=False, kind = "bar")
        for i in ax.patches:
            # get_x pulls left or right; get_height pushes up or down
            ax.text(i.get_x() + .1, i.get_height() + .2,
                    str(round((i.get_height()), 2)), fontsize=10, color='black')

    def country(self, df):
        ax = df.Country.groupby(df.Country).count().sort_values(ascending=False).head(8).plot(
            ax=self.axes, fontsize=8, grid=False, kind = "barh")
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y(),
                    str(round((i.get_width()), 2)), fontsize=10, color='black')

    def compare(self, df, me):
        airport = pd.read_pickle("airports.pkl")
        me_country = list(airport[airport.AirportIATA == me].Country.values)[0]
        domestic = len(df[df.Country == me_country])
        intl = len(df[~(df.Country == me_country)])
        lst = [domestic, intl]
        labels = ['Domestic', 'International']
        self.axes.pie(lst, labels=labels, autopct='%1.1f%%')  # 画饼图（数据，数据对应的标签，百分数保留两位小数点）
        self.axes.axis('equal')

    def intl(self, df, me):
        airport = pd.read_pickle("airports.pkl")
        me_country = list(airport[airport.AirportIATA == me].Country.values)[0]
        intl_country = df[~(df.Country == me_country)]
        ax = intl_country.Country.groupby(intl_country.Country).count().sort_values(ascending=False).head(8).plot(
            ax=self.axes, fontsize=8, grid=False, kind = "barh")
        for i in ax.patches:
            ax.text(i.get_width() + .3, i.get_y(),
                    str(round((i.get_width()), 2)), fontsize=10, color='black')

    def time(self, df):
        today = datetime.today().strftime('%Y-%m-%d')
        mylist = []
        for i in df['Departure']:
            total = today + " " + i
            format = '%Y-%m-%d %I:%M %p'
            my_date = datetime.strptime(total, format)
            mylist.append(my_date)
        se = pd.Series(mylist)
        df['datetime'] = se.values
        df.index = df.datetime
        df.datetime.resample('30T').count().plot(ax=self.axes, grid=True)


def airline_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='Airlines Statistics', size = (1100,400))
    panel = CanvasPanel(fr, df)
    panel.show_airlines(df)
    fr.Show()
    app.MainLoop()

def continent_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='Continent Statistics', size=(1000, 400))
    panel = CanvasPanel(fr, df)
    panel.continent(df)
    fr.Show()
    app.MainLoop()

def airleague_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='AirLeague Market Share', size=(500, 500))
    panel = CanvasPanel(fr, df)
    panel.airleague(df)
    fr.Show()
    app.MainLoop()

def city_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='City Statistics', size=(1100, 400))
    panel = CanvasPanel(fr, df)
    panel.city(df)
    fr.Show()
    app.MainLoop()

def airport_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='Airport Statistics', size=(500, 650))
    panel = CanvasPanel(fr, df)
    panel.airport(df)
    fr.Show()
    app.MainLoop()

def country_stats(df):
    app = wx.App()
    fr = wx.Frame(None, title='Country Statistics', size=(1000, 400))
    panel = CanvasPanel(fr, df)
    panel.country(df)
    fr.Show()
    app.MainLoop()

def compare_stats(df, me):
    app = wx.App()
    fr = wx.Frame(None, title='International and Domestic Flight Comparison', size=(450, 350))
    panel = CanvasPanel(fr, df)
    panel.compare(df, me)
    fr.Show()
    app.MainLoop()

def intl_stats(df, me):
    app = wx.App()
    fr = wx.Frame(None, title='International Countries Destination', size=(1000, 400))
    panel = CanvasPanel(fr, df)
    panel.intl(df, me)
    fr.Show()
    app.MainLoop()

def time_range(df):
    app = wx.App()
    fr = wx.Frame(None, title='Popular Times', size=(900, 400))
    panel = CanvasPanel(fr, df)
    panel.time(df)
    fr.Show()
    app.MainLoop()
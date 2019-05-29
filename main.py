import wx, airport, table, os, test, pandas as pd, airport_fx as fx, datetime, download_data as dldata
from time import gmtime, strftime
#import matplotlib.pyplot as plt
import urllib.request, ssl, plot
from geopy.distance import geodesic

class Departure(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.InitUI()

    def InitUI(self):
        '''THIS IS FOR THE MAIN FONT'''
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        '''THIS IS FOR THE EXAMPLE FONT'''
        ex_font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        ex_font.SetPointSize(11)

        vbox = wx.BoxSizer(wx.VERTICAL)

        '''ENTER THE AIRPORT INFO'''
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.st1 = wx.StaticText(self, label='Airport Code:')
        self.st1.SetFont(font)
        hbox1.Add(self.st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(self)
        self.tc.SetMaxLength(3)
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex1 = wx.StaticText(self, label='(Example: IND, ORD, LAX, etc.)')
        self.ex1.SetFont(ex_font)
        exbox1.Add(self.ex1, flag=wx.RIGHT, border=8)
        vbox.Add(exbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        '''ENTER THE AIRLINE INFO'''
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.st2 = wx.StaticText(self, label='Airline:')
        self.st2.SetFont(font)
        hbox2.Add(self.st2, flag=wx.RIGHT, border=8)
        self.tc2 = wx.TextCtrl(self)
        self.tc2.SetMaxLength(3)
        hbox2.Add(self.tc2, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex2 = wx.StaticText(self, label='(Example: AA, UA, DL, etc.)')
        self.ex2.SetFont(ex_font)
        exbox2.Add(self.ex2, flag=wx.RIGHT, border=8)
        vbox.Add(exbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        '''ENTER THE DESTINATION INFO'''
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.st3 = wx.StaticText(self, label='Destination:')
        self.st3.SetFont(font)
        hbox3.Add(self.st3, flag=wx.RIGHT, border=8)
        self.tc3 = wx.TextCtrl(self)
        # self.tc3.SetMaxLength(3)
        hbox3.Add(self.tc3, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex3 = wx.StaticText(self, label='(Example: ORD or Chicago etc.)')
        self.ex3.SetFont(ex_font)
        exbox3.Add(self.ex3, flag=wx.RIGHT, border=8)
        vbox.Add(exbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        '''ENTER THE FLIGHT NUMBER'''
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.st4 = wx.StaticText(self, label='Flight Number:')
        self.st4.SetFont(font)
        hbox4.Add(self.st4, flag=wx.RIGHT, border=8)
        self.tc4 = wx.TextCtrl(self)
        # self.tc3.SetMaxLength(3)
        hbox4.Add(self.tc4, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex4 = wx.StaticText(self, label='(Example: UA 123 or 123 etc.)')
        self.ex4.SetFont(ex_font)
        exbox4.Add(self.ex4, flag=wx.RIGHT, border=8)
        vbox.Add(exbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 35))

        '''BUTTON AND CHECKBOX'''
        b1 = wx.Button(self, label="Download Data")
        b1.Bind(wx.EVT_BUTTON, self.download)
        vbox.Add(b1)
        b2 = wx.Button(self, label="Show TimeTable")
        b2.Bind(wx.EVT_BUTTON, self.show_table)
        vbox.Add(b2)
        cb = wx.CheckBox(self, label='No Codeshare')
        cb.Bind(wx.EVT_CHECKBOX, self.onChecked)
        cb2 = wx.CheckBox(self, label='No Cargo (Not Accurate)')
        cb2.Bind(wx.EVT_CHECKBOX, self.onChecked2)
        vbox.Add(cb)
        vbox.Add(cb2)
        self.cbcs = False
        self.cbnc = False

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        closeBtn = wx.Button(self, label='Close', size=(70, 30))
        hbox5.Add(closeBtn, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        self.SetSizer(vbox)

    def info(self, text):
        wx.MessageBox(text, 'Information', wx.OK | wx.ICON_INFORMATION)

    def show_table(self, event):
        code = self.tc.GetValue().upper()
        if code == '':
            return self.info('Please Enter the Airport Code!')
        airline = self.tc2.GetValue().upper()
        location = self.tc3.GetValue()
        flight_num = self.tc4.GetValue()
        result = 'dep/' + code + '_DEP.pkl'
        # print(self.onChecked)
        if test.check_data(code, '0') is False:
            return self.info('The current Airport is not in the Library')
        else:
            df = pd.read_pickle(result)
            if airline != '':
                df = fx.search_by_airline(df, airline)
            if location != '':
                df = fx.search_location(df, location)
            if flight_num != '':
                df = fx.search_flight_num(df, flight_num)
            if self.cbcs is False:
                if self.cbnc is False:
                    return table.main(df)
                else:
                    return table.main(fx.no_cargo(df))
            else:
                if self.cbnc is False:
                    return table.main(fx.no_codeshare(df))
                else:
                    df = fx.no_codeshare(df)
                    return table.main(fx.no_cargo(df))

    def onChecked(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            self.cbcs = True
        else:
            self.cbcs = False

    def onChecked2(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            self.cbnc = True
        else:
            self.cbnc = False

    def download(self, event):
        code = self.tc.GetValue()
        return airport.main(code, '0'), self.info("Success!")

    def value(self, event):
        return self.tc.GetValue()

    def onClose(self, event):
        self.Close()


class Search(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.InitUI()

        self.st1.SetPosition((20, 20))
        self.search.SetPosition((30, 50))

    def InitUI(self):
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(13)

        self.st1 = wx.StaticText(self, label='This is the library to look up the Airline and Airport Code')
        self.st1.SetFont(font)

        '''searchbar'''
        self.search = wx.SearchCtrl(self, size = (200,-1))
        self.search.ShowCancelButton(True)

        lst = ['Airport', 'Airline']
        self.rbox = wx.RadioBox(self, pos=(30, 85), choices=lst, majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        b1 = wx.Button(self, label="Start Search", pos = (30, 130))
        b1.Bind(wx.EVT_BUTTON, self.search_list)
        b2 = wx.Button(self, label="More Information", pos=(170, 130))
        b2.Bind(wx.EVT_BUTTON, self.advanced_search)

        self.list_ctrl = wx.ListCtrl(self, pos = (3, 170), size=(375, 200), style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_SORT_ASCENDING)
        self.list_ctrl.InsertColumn(0, "IATA", width = 38)
        self.list_ctrl.InsertColumn(1, "ICAO", width = 45)
        self.list_ctrl.InsertColumn(2, "Name", width = 198)
        self.list_ctrl.InsertColumn(3, "Country", width = 95)

    def advanced_search(self, e):
        text = self.search.GetValue()
        if len(text) <= 1:
            return self.info('You need provide more information!')
        method = self.rbox.GetStringSelection()
        if method == 'Airport':
            df = pd.read_pickle('airports.pkl')
            if (len(text) <= 4) and (text.isupper() == True):
                df = df[(df.AirportIATA.str.contains(text, na=False)) | (df.AirlineICAO.str.contains(text, na=False))]
            else:
                df = df[(df.Airport_Name.str.contains(text, na=False)) | (df.Ariport_City.str.contains(text, na=False))]
            return table.main(df)
        if method == 'Airline':
            df = pd.read_pickle('airlines.pkl')
            df = df[(df.AirlineIATA.str.contains(text, na=False))|(df.AirlineICAO.str.contains(text, na=False))|(df.Airline.str.contains(text, na=False))]
            return table.main(df)

    def search_list(self, e):
        self.list_ctrl.DeleteAllItems()
        text = self.search.GetValue()
        if len(text) <= 1:
            return self.info('You need provide more information!')
        method = self.rbox.GetStringSelection()

        if method == 'Airport':
            #print(method,'success')
            df = pd.read_pickle('airports.pkl')
            if (len(text) <= 4) and (text.isupper() == True):
                df = df[(df.AirportIATA.str.contains(text, na=False)) | (df.AirlineICAO.str.contains(text, na=False))]
            else:
                df = df[(df.Airport_Name.str.contains(text, na=False)) | (df.Ariport_City.str.contains(text, na=False))]
            data = fx.airport_to_list(df)
            index = 0
            for i in data:
                self.list_ctrl.InsertItem(index, i[0])
                self.list_ctrl.SetItem(index, 1, i[1])
                self.list_ctrl.SetItem(index, 2, i[2])
                self.list_ctrl.SetItem(index, 3, i[3])
                index += 1
        if method == 'Airline':
            df = pd.read_pickle('airlines.pkl')
            df = df[(df.AirlineIATA.str.contains(text, na=False))|(df.AirlineICAO.str.contains(text, na=False))|(df.Airline.str.contains(text, na=False))]
            data = fx.airline_to_list(df)
            index = 0
            for i in data:
                self.list_ctrl.InsertItem(index, i[0])
                self.list_ctrl.SetItem(index, 1, i[1])
                self.list_ctrl.SetItem(index, 2, i[2])
                self.list_ctrl.SetItem(index, 3, i[3])
                index += 1

    def info(self, text):
        wx.MessageBox(text, 'Information', wx.OK | wx.ICON_INFORMATION)

    def onRadioBox(self, e):
        print(self.rbox.GetStringSelection(), ' is clicked from Radio Box')


class Analysis(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.InitUI()

    def InitUI(self):
        self.search = wx.SearchCtrl(self, size=(200, -1), pos = (20,20))
        self.search.ShowCancelButton(True)
        self.search.SetMaxLength(3)

        lst = ['Departure', 'Arrival']
        self.rbox = wx.RadioBox(self, pos=(20, 60), choices=lst, majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        self.data = ""
        b1 = wx.Button(self, label="Load Data", pos=(20, 110))
        b1.Bind(wx.EVT_BUTTON, self.load_df)
        b2 = wx.Button(self, label="Clear", pos=(135, 110))
        b3 = wx.Button(self, label="Show Table", pos=(255, 110))
        b3.Bind(wx.EVT_BUTTON, self.show_table)

        line = '*' * 55
        self.st1 = wx.StaticText(self, label= line, pos = (15, 140))
        #self.st1.SetFont(font)

        b4 = wx.Button(self, label="Airline Statistics", pos=(20, 170))
        b4.Bind(wx.EVT_BUTTON, self.carrier)
        b5 = wx.Button(self, label="Continent", pos=(20, 200))
        b5.Bind(wx.EVT_BUTTON, self.continent)
        b6 = wx.Button(self, label="AirLeague Share", pos=(20, 230))
        b6.Bind(wx.EVT_BUTTON, self.airleague)
        b7 = wx.Button(self, label="City Statistics", pos=(20, 260))
        b7.Bind(wx.EVT_BUTTON, self.city)
        b8 = wx.Button(self, label="Airport Statistics", pos=(20, 290))
        b8.Bind(wx.EVT_BUTTON, self.IATA)
        b9 = wx.Button(self, label="Country Statistics", pos=(20, 320))
        b9.Bind(wx.EVT_BUTTON, self.country)
        b10 = wx.Button(self, label="International Comparison", pos=(190, 170))
        b10.Bind(wx.EVT_BUTTON, self.compare)
        b11 = wx.Button(self, label="Other Countries", pos=(190, 200))
        b11.Bind(wx.EVT_BUTTON, self.intl_countries)
        b12 = wx.Button(self, label="Top 10 Furthest Cities", pos=(190, 230))
        b12.Bind(wx.EVT_BUTTON, self.furthest)
        b13 = wx.Button(self, label="Top 10 Closest Cities", pos=(190, 260))
        b13.Bind(wx.EVT_BUTTON, self.closest)
        b14 = wx.Button(self, label="Popular Times", pos=(190, 290))
        b14.Bind(wx.EVT_BUTTON, self.times)

    def load_df(self, event):
        airlines = pd.read_pickle("airlines.pkl")
        airports = pd.read_pickle("airports.pkl")  # should clean the column
        busiest = pd.read_csv("busiest airport.csv")
        league = pd.read_pickle("airleague.pkl")
        code = self.search.GetValue().upper()
        method = self.rbox.GetStringSelection()
        if method == "Departure":
            selection = "0"
        if method == "Arrival":
            selection = "1"
        df = dldata.download_all(code, selection)
        df = fx.no_cargo(df)
        df = fx.no_codeshare(df)
        airports = pd.merge(airports, busiest, on=['AirportIATA'], how='outer')
        #airports = airports.drop(columns=['Geoname ID'])
        airports = airports.rename(columns={'Ariport_City': 'Airport_City'})
        airlines = pd.merge(airlines, league, left_on='AirlineIATA', right_on='Airline', how='outer')
        airlines = airlines.drop(columns=['AirlineID', 'Airline_y', 'AirlineICAO', 'Airline_x'])
        airlines = airlines.rename(columns={'Country': 'Airline_Country'})
        airlines.League = airlines.League.fillna(value='None')
        airports.RANK = airports.RANK.fillna(value=0)
        df['AirlineIATA'], df['Number'] = df.Flight.str.split(' ', 1).str
        df['AirportIATA'], df['City'] = df.Destination.str.split(' ', 1).str
        df.AirportIATA = df.AirportIATA.str[1:-1]
        df = df.drop(columns=['Flight', 'Destination'])
        df = pd.merge(df, airlines, on='AirlineIATA', how='left')
        df = pd.merge(df, airports, on='AirportIATA', how='left')
        df = df.dropna()
        self.info("Loading Successful!")
        self.data = df

    def show_table(self, event):
        return table.main(self.data)

    def carrier(self, event):
        df = self.data
        return plot.airline_stats(df)

    def continent(self, event):
        df = self.data
        return plot.continent_stats(df)

    def airleague(self, event):
        df = self.data
        return plot.airleague_stats(df)

    def city(self, event):
        df = self.data
        return plot.city_stats(df)

    def IATA(self, event):
        df = self.data
        return plot.airport_stats(df)

    def country(self, event):
        df = self.data
        return plot.country_stats(df)

    def compare(self, event):
        df = self.data
        me = self.search.GetValue().upper()
        return plot.compare_stats(df, me)

    def intl_countries(self, event):
        df = self.data
        me = self.search.GetValue().upper()
        return plot.intl_stats(df, me)

    def times(self, event):
        df = self.data
        return plot.time_range(df)

    def furthest(self, event):
        df = self.data
        me = self.search.GetValue().upper()
        airports = pd.read_pickle("airports.pkl")
        distance = df.loc[:, ['City', 'Country', 'AirportIATA', 'Airport_Name', 'Latitude', 'Longitude']]
        distance = distance.drop_duplicates()
        lat = list(airports[airports.AirportIATA == me].Latitude.values)[0]
        long = list(airports[airports.AirportIATA == me].Longitude.values)[0]
        distance['Distance (km)'] = ''
        for indexs in distance.index:
            a = distance.loc[indexs].values[4]
            b = distance.loc[indexs].values[5]
            distance["Distance (km)"][indexs] = round(geodesic((lat, long), (a, b)).km, 2)
        d = distance.sort_values(by='Distance (km)', ascending=False).head(10)
        return table.main(d)

    def closest(self, event):
        df = self.data
        me = self.search.GetValue().upper()
        airports = pd.read_pickle("airports.pkl")
        distance = df.loc[:, ['City', 'Country', 'AirportIATA', 'Airport_Name', 'Latitude', 'Longitude']]
        distance = distance.drop_duplicates()
        lat = list(airports[airports.AirportIATA == me].Latitude.values)[0]
        long = list(airports[airports.AirportIATA == me].Longitude.values)[0]
        distance['Distance (km)'] = ''
        for indexs in distance.index:
            a = distance.loc[indexs].values[4]
            b = distance.loc[indexs].values[5]
            distance["Distance (km)"][indexs] = round(geodesic((lat, long), (a, b)).km, 2)
        d = distance.sort_values(by='Distance (km)', ascending=False).tail(10)
        return table.main(d)

    def info(self, text):
        wx.MessageBox(text, 'Information', wx.OK | wx.ICON_INFORMATION)


class InstantSearch(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.InitUI()

    def InitUI(self):
        '''THIS IS FOR THE MAIN FONT'''
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        '''THIS IS FOR THE EXAMPLE FONT'''
        ex_font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        ex_font.SetPointSize(11)
        """entering information"""
        self.st1 = wx.StaticText(self, label='Airport Code: *', pos = (20,20))
        self.st1.SetFont(font)
        self.search = wx.SearchCtrl(self, size=(190, -1), pos = (120, 20))
        self.search.ShowCancelButton(True)
        self.search.SetMaxLength(3)

        self.st2 = wx.StaticText(self, label='Origin/Arrival:', pos=(20, 60))
        self.st2.SetFont(font)
        self.search2 = wx.SearchCtrl(self, size=(190, -1), pos=(120, 60))
        self.search2.ShowCancelButton(True)

        self.st3 = wx.StaticText(self, label='Airline:', pos=(20, 100))
        self.st3.SetFont(font)
        self.search3 = wx.SearchCtrl(self, size=(190, -1), pos=(120, 100))
        self.search3.ShowCancelButton(True)

        self.st4 = wx.StaticText(self, label='Flight Number:', pos=(20, 140))
        self.st4.SetFont(font)
        self.search4 = wx.SearchCtrl(self, size=(190, -1), pos=(120, 140))
        self.search4.ShowCancelButton(True)
        """choice"""
        lst = ['Departure', 'Arrival']
        self.rbox = wx.RadioBox(self, pos=(20, 180), choices=lst, majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        self.time = ['12 AM - 3 AM', '3 AM - 6 AM', '6 AM - 9 AM', '9 AM - 12 PM', '12 PM - 3 PM', '3 PM - 6 PM', '6 PM - 9 PM', '9 PM - 12 AM', "All Day"]
        self.combo = wx.Choice(self, choices=self.time, pos = (230, 187))
        """search"""
        b1 = wx.Button(self, label="Search", pos=(20, 230))
        b1.Bind(wx.EVT_BUTTON, self.show_table)
        cb = wx.CheckBox(self, label='No Codeshare', pos = (20, 270))
        cb.Bind(wx.EVT_CHECKBOX, self.onChecked)
        cb2 = wx.CheckBox(self, label='No Cargo', pos = (20, 295))
        cb2.Bind(wx.EVT_CHECKBOX, self.onChecked2)
        self.cbcs = False
        self.cbnc = False

        self.st5 = wx.StaticText(self, label="Today's Date:", pos=(20, 345))
        self.st5.SetFont(ex_font)
        '''date and time'''
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d, %A ")
        zone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        self.st6 = wx.StaticText(self, label=now + zone, pos=(20, 360))
        self.st6.SetFont(ex_font)

    def info(self, text):
        wx.MessageBox(text, 'Information', wx.OK | wx.ICON_INFORMATION)

    def show_table(self, event):
        code = self.search.GetValue().upper()
        method = self.rbox.GetStringSelection()
        choice = str(self.combo.GetSelection() + 1)
        if method == "Departure":
            selection = "0"
        if method == "Arrival":
            selection = "1"
        if code == '':
            return self.info('Please Enter the Airport Code!')
        if (len(code) != 3) or (code.isalpha() is False):
            return self.info('This is a invalid Airport Code!')
        if choice == "9":
            df = dldata.download_all(code, selection)
        else:
            df = dldata.ontime(code, choice, selection)
        #filter
        airline = self.search3.GetValue().upper()
        location = self.search2.GetValue()
        flight_num = self.search4.GetValue()
        if airline != '':
            df = fx.search_by_airline(df, airline)
        if location != '':
            df = fx.search_location(df, location, selection)
        if flight_num != '':
            df = fx.search_flight_num(df, flight_num)
        if self.cbcs is False:
            if self.cbnc is False:
                return table.main(df)
            else:
                return table.main(fx.no_cargo(df))
        else:
            if self.cbnc is False:
                return table.main(fx.no_codeshare(df))
            else:
                df = fx.no_codeshare(df)
                return table.main(fx.no_cargo(df))

    def onChecked(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            self.cbcs = True
        else:
            self.cbcs = False

    def onChecked2(self, e):
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            self.cbnc = True
        else:
            self.cbnc = False



class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Airport Query System", size = (600,800), style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

        p = wx.Panel(self)

        nb = wx.Notebook(p)
        tab1 = InstantSearch(nb)
        tab2 = Search(nb)
        tab3 = Analysis(nb)
        tab4 = Departure(nb)
        nb.AddPage(tab1, 'Flight')
        nb.AddPage(tab2, 'Library')
        nb.AddPage(tab3, 'Analysis')
        nb.AddPage(tab4, 'Departure')

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


def main():
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
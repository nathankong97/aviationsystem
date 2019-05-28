import wx, airport, table, os, test, pandas as pd, airport_fx as fx

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size = (350,400))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        txt_font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        txt_font.SetPointSize(11)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.st1 = wx.StaticText(panel, label='Airport Code:')
        self.st1.SetFont(font)
        hbox1.Add(self.st1, flag=wx.RIGHT, border=8)
        self.tc = wx.TextCtrl(panel, size=(300, -1))
        self.tc.SetMaxLength(3)
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        exbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex1 = wx.StaticText(panel, label='(Example: IND, ORD, LAX, etc.)')
        self.ex1.SetFont(txt_font)
        exbox1.Add(self.ex1, flag=wx.RIGHT, border=8)
        vbox.Add(exbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.st2 = wx.StaticText(panel, label='Airline:')
        self.st2.SetFont(font)
        hbox2.Add(self.st2, flag=wx.RIGHT, border=8)
        self.tc2 = wx.TextCtrl(panel)
        self.tc2.SetMaxLength(3)
        hbox2.Add(self.tc2, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex2 = wx.StaticText(panel, label='(Example: AA, UA, DL, etc.)')
        self.ex2.SetFont(txt_font)
        exbox2.Add(self.ex2, flag=wx.RIGHT, border=8)
        vbox.Add(exbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.st3 = wx.StaticText(panel, label='Destination:')
        self.st3.SetFont(font)
        hbox3.Add(self.st3, flag=wx.RIGHT, border=8)
        self.tc3 = wx.TextCtrl(panel)
        #self.tc3.SetMaxLength(3)
        hbox3.Add(self.tc3, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex3 = wx.StaticText(panel, label='(Example: ORD or Chicago etc.)')
        self.ex3.SetFont(txt_font)
        exbox3.Add(self.ex3, flag=wx.RIGHT, border=8)
        vbox.Add(exbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.st4 = wx.StaticText(panel, label='Flight Number:')
        self.st4.SetFont(font)
        hbox4.Add(self.st4, flag=wx.RIGHT, border=8)
        self.tc4 = wx.TextCtrl(panel)
        # self.tc3.SetMaxLength(3)
        hbox4.Add(self.tc4, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        exbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.ex4 = wx.StaticText(panel, label='(Example: UA123 or 123 etc.)')
        self.ex4.SetFont(txt_font)
        exbox4.Add(self.ex4, flag=wx.RIGHT, border=8)
        vbox.Add(exbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 35))

        b1 = wx.Button(panel, label="Download Data")
        b1.Bind(wx.EVT_BUTTON, self.download)
        vbox.Add(b1)
        b2 = wx.Button(panel, label="Show TimeTable")
        b2.Bind(wx.EVT_BUTTON, self.show_table)
        vbox.Add(b2)
        cb = wx.CheckBox(panel, label = 'No Codeshare')
        cb.Bind(wx.EVT_CHECKBOX, self.onChecked)
        cb2 = wx.CheckBox(panel, label='No Cargo (Not Accurate)')
        cb2.Bind(wx.EVT_CHECKBOX, self.onChecked2)
        vbox.Add(cb)
        vbox.Add(cb2)
        self.cbcs = False
        self.cbnc = False

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        #btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        #hbox5.Add(btn1)
        #btn1.Bind(wx.EVT_BUTTON, self.value)
        closeBtn = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(closeBtn, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

        panel.SetSizer(vbox)


    def info(self, text):
        wx.MessageBox(text, 'Information', wx.OK | wx.ICON_INFORMATION)

    def show_table(self, event):
        code = self.tc.GetValue().upper()
        if code == '':
            return self.info('Please Enter the Airport Code!')
        airline = self.tc2.GetValue().upper()
        location = self.tc3.GetValue()
        flight_num = self.tc4.GetValue().replace(" ", "")
        result = 'data/' + code + '_DEP.pkl'
        #print(self.onChecked)
        if test.check_data(code) is False:
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
        return airport.main(code), self.info("Success!")

    def value(self, event):
        return self.tc.GetValue()

    def onClose(self, event):
        self.Close()

def main():

    app = wx.App()
    ex = Example(None, title='Airport Query System')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
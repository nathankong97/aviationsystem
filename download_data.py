import urllib.request
import urllib.parse
import pandas as pd, numpy as np, json
from bs4 import BeautifulSoup
from datetime import datetime
import ssl


def time():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%Y-%m-%d %H:%M")

    return date, current_time


def flightstats(code, type):
    try:
        # parse the website and download data
        url = "https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:46cf2cff:137a5643c65:-5b5f&weblet=status&action=AirportFlightStatus&airportCode=" + code
        pageInputs = {"airportQueryTimePeriod": "1", 'airportQueryType': type}
        pageGets = urllib.parse.urlencode(pageInputs)
        pageGets = pageGets.encode("ascii")
        serReq = urllib.request.Request(url, pageGets)
        opReq = urllib.request.urlopen(serReq, context=ssl._create_unverified_context())
        rdReq = opReq.read().decode()
        rdReq = rdReq.rstrip()

        # intialing table for the first time range
        soup = BeautifulSoup(rdReq, 'html.parser')
        table = soup.find_all("table")
        df = pd.read_html(str(table))[3]

        # download the data for the rest of the time range
        for i in range(7):
            url = "https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:46cf2cff:137a5643c65:-5b5f&weblet=status&action=AirportFlightStatus&airportCode=" + code
            pageInputs = {"airportQueryTimePeriod": str(i + 2), 'airportQueryType': type}
            pageGets = urllib.parse.urlencode(pageInputs)
            pageGets = pageGets.encode("ascii")
            serReq = urllib.request.Request(url, pageGets)
            opReq = urllib.request.urlopen(serReq,context=ssl._create_unverified_context())
            rdReq = opReq.read().decode()
            rdReq = rdReq.rstrip()
            soup = BeautifulSoup(rdReq, 'html.parser')
            table = soup.find_all("table")
            df_add = pd.read_html(str(table))[3]
            df = pd.concat([df, df_add])

        # clean the duplicates
        df.columns = df.iloc[0]
        df = df.drop_duplicates()
        df = df.drop(0)

        # save the data
        if type == '0':
            df.to_pickle("dep/" + code + "_DEP.pkl")
        if type == '1':
            df.to_pickle("arr/" + code + "_ARR.pkl")
        return True

    except (urllib.error.URLError):
        #print('you need to get online!')
        return False

def ontime(code, time, type):
    try:
        url = "https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:46cf2cff:137a5643c65:-5b5f&weblet=status&action=AirportFlightStatus&airportCode=" + code
        pageInputs = {"airportQueryTimePeriod": time, 'airportQueryType': type}
        pageGets = urllib.parse.urlencode(pageInputs)
        pageGets = pageGets.encode("ascii")
        serReq = urllib.request.Request(url, pageGets)
        opReq = urllib.request.urlopen(serReq, context=ssl._create_unverified_context())
        rdReq = opReq.read().decode()
        rdReq = rdReq.rstrip()

        soup = BeautifulSoup(rdReq, 'html.parser')
        table = soup.find_all("table")
        df = pd.read_html(str(table))[3]
        df.columns = df.iloc[0]
        df = df.drop_duplicates()
        df = df.drop(0)
        return df

    except (urllib.error.URLError):
        #print('you need to get online!')
        return False

def download_all(code, type):
    try:
        # parse the website and download data
        url = "https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:46cf2cff:137a5643c65:-5b5f&weblet=status&action=AirportFlightStatus&airportCode=" + code
        pageInputs = {"airportQueryTimePeriod": "1", 'airportQueryType': type}
        pageGets = urllib.parse.urlencode(pageInputs)
        pageGets = pageGets.encode("ascii")
        serReq = urllib.request.Request(url, pageGets)
        opReq = urllib.request.urlopen(serReq, context=ssl._create_unverified_context())
        rdReq = opReq.read().decode()
        rdReq = rdReq.rstrip()
        # intialing the base table for the first time range 12-3am
        soup = BeautifulSoup(rdReq, 'html.parser')
        table = soup.find_all("table")
        df = pd.read_html(str(table))[3]

        # download the data for the rest of the time range
        for i in range(7):
            url = "https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:46cf2cff:137a5643c65:-5b5f&weblet=status&action=AirportFlightStatus&airportCode=" + code
            pageInputs = {"airportQueryTimePeriod": str(i + 2), 'airportQueryType': type}
            pageGets = urllib.parse.urlencode(pageInputs)
            pageGets = pageGets.encode("ascii")
            serReq = urllib.request.Request(url, pageGets)
            opReq = urllib.request.urlopen(serReq,context=ssl._create_unverified_context())
            rdReq = opReq.read().decode()
            rdReq = rdReq.rstrip()
            soup = BeautifulSoup(rdReq, 'html.parser')
            table = soup.find_all("table")
            df_add = pd.read_html(str(table))[3]
            df = pd.concat([df, df_add])
        # clean the duplicates
        df.columns = df.iloc[0]
        df = df.drop_duplicates()
        df = df.drop(0)

        return df

    except (urllib.error.URLError):
        #print('you need to get online!')
        return False
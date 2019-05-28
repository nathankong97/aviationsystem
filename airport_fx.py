import urllib.request
import urllib.parse
import pandas as pd, numpy as np, json, pymongo
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib as plt
import os

def split_airport(file):
    df = pd.read_pickle(file)
    try:
        df['AirportIATA'] = df['Destination'].str[1:4]
        df['City'] = df['Destination'].str[6:]
        df = df.drop(columns = ['Destination'])
        df.to_pickle(file)
        print("split_airport success")
    except:
        print("already did!")
        pass


def no_codeshare(df):
    return df[df.Flight.str[-1] != '^']

def no_cargo(df):
    df = df[~df.Carrier.str.contains("Cargo")]
    df = df[~df.Carrier.str.contains("UPS|FedEx|SF|Atlas|AHK|Suparna|Postal|Shell Aircraft")]
    return df


def split_flight(file):
    df = pd.read_pickle(file)
    try:
        df = df[df.Flight.str[-1] != '^']
        df['AirlineIATA'] = df['Flight'].str[0:2]
        df['Number'] = df['Flight'].str[3:]
        df = df.drop(columns = ['Flight'])
        df.to_pickle(file)
        print("split_flight success")
    except:
        print("already did!")
        pass

def convert_time(file):
    '''NEED TO DROP THE NULL VALUE!!!'''
    df = pd.read_pickle(file)
    try:
        mylist = []
        for i in df['Departure']:
            format = '%I:%M %p'
            my_date = datetime.strptime(i, format)
            mylist.append(my_date)
        se = pd.Series(mylist)
        df['datetime'] = se.values
        df.index = df.datetime
        df.to_pickle(file)
        print("convert_time success")
    except (TypeError):
        df.datetime = pd.to_datetime(df["Departure"])
        df.index = df.datetime
        df.index.names = ['datetime']
        df.to_pickle(file)
        print("convert_time success")
    except Exception as e:
        print(e)
        pass

def search_by_airline(df, airline):
    df['A'], df['B'] = df['Flight'].str.split('(?= ).+', 1).str
    df = df[df.A == airline]
    df = df.drop(columns = ['A','B'])
    return df

def search_location(df, location, code):
    if code == "0":
        return df[df.Destination.str.contains(location)]
    if code == "1":
        return df[df.Origin.str.contains(location)]

def search_flight_num(df, num):
    return df[df.Flight.str.contains(num)]

def airport_to_list(df):
    mylist = [i[0:5] for i in df.values.tolist()]
    myorder = [3, 4, 0, 2, 1]
    mylist = [[x[i] for i in myorder][0:4] for x in mylist]
    return mylist

def airline_to_list(df):
    mylist = [i[1:5] for i in df.values.tolist()]
    myorder = [1, 2, 0, 3]
    mylist = [[x[i] for i in myorder] for x in mylist]
    return mylist



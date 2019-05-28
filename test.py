import airport, table, os

def check_data(code, type):
    lst = [i[0:3] for i in os.listdir('/Users/apple/PycharmProjects/AirportSystem/venv/dep')]
    lst2 = [i[0:3] for i in os.listdir('/Users/apple/PycharmProjects/AirportSystem/venv/arr')]
    #print(lst)
    if type == '0':
        if code not in lst:
            return False
        else:
            return True
    if type == '1':
        if code not in lst2:
            return False
        else:
            return True
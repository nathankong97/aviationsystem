import download_data


def main(code, type):
    code = code.upper()

    data = download_data.flightstats(code, type)

    if data:
        write(code, download_data.time()[1], type)
    else:
        return "Try to connect the Internet"

def write(code, time, type):
    if type == '0':
        type = 'Departure'
    if type == '1':
        type = 'Arrival'
    f= open("record.txt","a+")

    f.write('the data ' + code + ' '+ type + ' has been download in '+ time + '\n')

    f.close()

    print("record succeed!")

if __name__ == '__main__':
    main(code)

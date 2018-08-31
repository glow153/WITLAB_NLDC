import happybase


def getSpectra(date: str, time: str):
    connection = happybase.Connection('210.102.142.14')
    print(connection.tables())
    table = connection.table('natural_light')
    return table.row(date, [time])


if __name__ == '__main__':
    date = '2017-04-13'
    time = '100000'
    print(getSpectra(date, time))

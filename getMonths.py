# from datetime import date
def getMonths():
    import datetime

    today = datetime.datetime.now()
    weekLater = today + datetime.timedelta(days=7)

    todayMonthNum = int(today.strftime("%m"))
    weekLaterMonthNum = int(weekLater.strftime("%m"))

    if(todayMonthNum == weekLaterMonthNum):
        return[1]
    else:
        return[1, 2]
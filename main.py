from autoBrowse import getPracPage
from findSlots import parsePage
from getMonths import getMonths
from bot import sendInfo
from db_helper import checkStatus, update_db

from datetime import datetime
timingDict = {
    1: "07:30 - 09:10",
    2: "09:20 - 11:00",
    3: "11:30 - 13:10",
    4: "13:20 - 15:00",
    5: "15:20 - 17:00",
    6: "17:10 - 18:50",
    7: "19:20 - 21:00",
    8: "21:10 - 22:50"
}

if __name__ == "__main__":
    # ONLY RUNS IF STATUS IS "ON"
    if(checkStatus()):
        SELECTED_DATES = getMonths()
        
        pageString = getPracPage(SELECTED_DATES)
        
        slotsList = parsePage(pageString)

        # Get lilst of new slots in [MONTH, DATE, DAY, SLOTS]
        newSlotsList = update_db(slotsList)

        # MESSAGING =====================================================
        txt = ""
        for slot in newSlotsList:
            month, date, day, slots = slot

            date_day = datetime.strptime(date, "%d/%m/%Y").day

            txt += f"\n{date_day} {month} [ {day} ]:\n"

            for x in slots:
                txt += f"{x}: {timingDict[x]}\n"
        
        if(not txt == ""):
            sendInfo("NEW SLOTS✨" + txt)
        # ================================================================
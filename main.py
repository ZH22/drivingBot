from autoBrowse import getPage
from findSlots import parsePage
from getMonths import getMonths
from bot import sendInfo

from datetime import date

if __name__ == "__main__":

    # Get current month and month of 1 week later
    today = date.today()


    SELECTED_DATES = getMonths()

    pageString = getPage(SELECTED_DATES)
    slotsList = parsePage(pageString)

    slotMessage = ""
    for slot in slotsList:
        print(slot.date)
        slotMessage += f"{slot.date} {str(slot.slots)}\n"
    
    if(not slotMessage == ""):
        sendInfo(slotMessage)
from autoBrowse import getTPDS
from findSlots import parsePage
from getMonths import getMonths
from bot import sendInfo
from db_helper import checkModNum, update_db

if __name__ == "__main__":
    SELECTED_DATES = getMonths()
    pageString = getTPDS(checkModNum() ,SELECTED_DATES)
    
    # If there's no limit error
    if(pageString):
        # Parse the pageString and get slotsList
        print('parsing string')

        # Update DB and get list of new slots


        # Send New slots

    else:
        sendInfo("TPDS Limit Hit T^T")
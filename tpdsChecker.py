from autoBrowse import getTPDS
from findSlots import parseTPDS
from getMonths import getMonths
from bot import sendInfo
from db_helper import checkModNum, getUserName, getUserTries, update_db, getNexUserTele, incrementUserTries
from datetime import datetime

if __name__ == "__main__":
    SELECTED_DATES = getMonths()
    teleID = getNexUserTele()
    
    # If next user is available then run
    if(teleID):
        pageString = getTPDS(teleID, checkModNum() ,SELECTED_DATES)
        
        # If there's no limit error
        if(pageString):
            # Parse the pageString and get slotsList
            slotsList = parseTPDS(pageString)

            # Update DB and get list of new slots
            newSlotsList = update_db(slotsList, "tpds")

            # Send New slots
            txt = ""
            for slot in newSlotsList:
                month, date, day, slots = slot

                date_day = datetime.strptime(date, "%d/%m/%Y").day

                txt += f"\n{date_day} {month} [ {day} ]:\n"

                for x in slots:
                    txt += f"{x}: session {x}\n"
            
            if(not txt == ""):
                sendInfo("🚨 TPDS NEW SLOTS 🚨 (testing)" + txt)

        else:
            sendInfo("TPDS Limit Hit T^T")
        
        incrementUserTries(teleID)
        sendInfo(f"TPDS checker ran using {getUserName(teleID)}'s account\nTries today: {getUserTries(teleID)}\nTESTING ONLY, WILL REMOVE AFT 24HRS")
        

        
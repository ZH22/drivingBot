import json
from datetime import datetime

MONTHS = ["Jan", "Feb", "Mar", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def update_db(slotsList):
    # List to hold all the newly added slots 
    diff_slots_list = []

    # Get Prev Data
    with open("./database/data", "r") as f:
        prevData = f.read()
        prevJsonObj = json.loads(prevData)

    # Get Template
    with open("./database/data_template", "r") as f:
        jsonObj = json.loads(f.read())

    for slot in slotsList:
        slotDateObj = datetime.strptime(slot.date, "%d/%m/%Y")

        month = MONTHS[slotDateObj.month -1]
        date = slot.date
        day = slot.day
        slotTimings = slot.slots

        # Populate new json object
        newSlotDict = {"day": day, "slots": slotTimings}
        jsonObj[month][date] = newSlotDict

        # Compare with previous slots for that day
        prevDate = prevJsonObj.get(month).get(date)
        # If date not in, all slots are new
        if(prevDate is None): 
            slot_diff = slotTimings

        # If already in, find different slots (New from prev time)
        else:
            prevSlots = prevDate.get("slots")
            slot_diff = [slot for slot in slotTimings if slot not in prevSlots]
        
        # only append the "new" slots if there are
        if(len(slot_diff) > 0):
            diff_slots_list.append([month, date, day, slot_diff])

    # Save new Data
    newJsonObj = json.dumps(jsonObj, indent=2)
    with open("./database/data", "w") as f:
        f.write(newJsonObj)

    # Return data for new slots
    return(diff_slots_list)
from getpass import getuser
from inspect import currentframe
import json
from datetime import datetime

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def update_db(slotsList, mode):
    # List to hold all the newly added slots 
    diff_slots_list = []

    # Get Prev Data
    if(mode == 'prac'):
        dbPath = "./database/data"
    
    elif(mode == 'tpds'):
        dbPath = "./database/tpds_data"

    with open(dbPath, "r") as f:
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
    with open(dbPath, "w") as f:
        f.write(newJsonObj)

    # Return data for new slots
    return(diff_slots_list)


# CONFIGURATION FUNCTIONS
def getConfigJSON():
    with open("./database/bot_config", "r") as f:
        data = f.read()
        return json.loads(data)

def setConfigJSON(newJSON):
    with open("./database/bot_config", "w") as f:
        f.write(json.dumps(newJSON, indent=2))

# Toggle bot on and off 
def toggleStatus():
    configJSON = getConfigJSON()
    currentStatus = configJSON.get("status")
    
    if(currentStatus == "ON"):
        currentStatus = "OFF"
    
    elif(currentStatus == "OFF"):
        currentStatus = "ON"
    
    configJSON["status"] = currentStatus
    setConfigJSON(configJSON)
    return currentStatus

def checkStatus():
    return getConfigJSON().get("status") == "ON"

# TPDS modNUM
def toggleModNum():
    configJSON = getConfigJSON()
    currentModNum = configJSON.get("TPDS_modNum")
    newModNum = currentModNum + 1
    if(newModNum > 3):
        newModNum = 1
    configJSON["TPDS_modNum"] = newModNum
    setConfigJSON(configJSON)
    return newModNum

def checkModNum():
    return getConfigJSON().get("TPDS_modNum")

# User DB ================================================
def getUsers():
    with open("./database/users", "r") as f:
        data = f.read()
        return json.loads(data)

# Check if user exists
def checkUser(teleID):
    users = getUsers()
    for user in users:
        if(user == str(teleID)):
            return True
    return False

def setUsers(newJSON):
    with open("./database/users", "w") as f:
        f.write(json.dumps(newJSON, indent=2))

def getAccount(teleID):
    # Run only if user exists
    if checkUser(teleID):
        users = getUsers()
        teleID = str(teleID)
        username = users[teleID].get("bbdc_username")
        password = users[teleID].get("password")
        return [username, password]

def getUserName(teleID):
    users = getUsers()
    return users[str(teleID)].get("name")

def getUserTries(teleID):
    return getUsers()[str(teleID)].get("tries_today")

def getNexUserTele():
    users = getUsers()
    tries_list = []
    teleList = []
    for user in users:
        teleList.append(user)
        tries_list.append(users[user].get("tries_today"))
    # If all same tries use first user
    if(all(x == tries_list[0] for x in tries_list) and tries_list[0] < 4):
        return teleList[0]
    # If not check for the next in line
    elif(tries_list[-1] < 4):
        for i in range(0, len(teleList)-1):
            if(tries_list[i] > tries_list[i+1]):
                return teleList[i+1]

def incrementUserTries(teleID):
    users = getUsers()
    teleID = str(teleID)
    user = users[teleID]
    currentTries = user.get("tries_today")
    users[teleID]["tries_today"] = currentTries + 1
    setUsers(users)

def resetUserTries():
    users = getUsers()
    for user in users:
        users[user]["tries_today"] = 0
    setUsers(users)
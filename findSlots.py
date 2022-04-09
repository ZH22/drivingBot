class slot:
    def __init__(self, date, day, slotList):
        self.date = date
        self.day = day
        self.slots = slotList

# Get slots and date from page html string
def parsePage(pageString):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(pageString, 'html.parser')
    allSlots = []

    # Only run if no slots error didnt show
    if (hasSlots(soup)):
        slotTable = soup.find(id="myform").table.tbody.table
        table_body = slotTable.find("tbody")
        rows = table_body.find_all("tr")[2:]

        for row in rows:
            rowCols = row.find_all("td")

            # Get Date
            rowDateAndDay = rowCols[0].contents
            rowDate = rowDateAndDay[0]
            rowDay = rowDateAndDay[2]
            
            slotCols = rowCols[2:]
            rowFreeSlotsList = findSlots(slotCols)

            allSlots.append(slot(rowDate, rowDay, rowFreeSlotsList))
    else:
        print("no slots found")    
    return allSlots

def parseTPDS(pageString):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(pageString, 'html.parser')
    allSlots = []

    if (hasSlots(soup)):
        slotTable = soup.find("form").table.tbody.table
        table_body = slotTable.find("tbody")
        rows = table_body.find_all("tr")[2:]

        for row in rows:
            rowCols = row.find_all("td")

            # Get Date
            rowDateAndDay = rowCols[0].contents
            rowDate = rowDateAndDay[0]
            rowDay = rowDateAndDay[2]
            
            slotCols = rowCols[2:]
            rowFreeSlotsList = findSlots(slotCols)

            allSlots.append(slot(rowDate, rowDay, rowFreeSlotsList))
    else:
        print("no slots found")    
    return allSlots


# HELPER FUNCTIONS ===============================================
def hasSlots(soup):
    errList = soup.find_all("td", {"class": "errtbltitle"})
    if len(errList) == 0:
        return True
    return False

def findSlots(slotcols):
    slotNum = 0
    freeSlotList = []

    # Go through slots and return list of free slot Num
    for slot in slotcols:
        slotNum += 1
        slotContent = slot.contents
        
        if(len(slotContent) > 0):
            freeSlotList.append(slotNum)
    return freeSlotList
# =================================================================
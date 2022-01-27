class slot:
    def __init__(self, date, day, slotList):
        self.date = date
        self.day = day
        self.slots = slotList

# Get slots and date from page html string
def parsePage(pageString):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(pageString, 'html.parser')

    slotTable = soup.find(id="myform").table.tbody.table
    table_body = slotTable.find("tbody")
    rows = table_body.find_all("tr")[2:]

    # row= rows[0]
    allSlots = []

    for row in rows:
        rowCols = row.find_all("td")

        # Get Date
        rowDateAndDay = rowCols[0].contents
        rowDate = rowDateAndDay[0]
        rowDay = rowDateAndDay[2]
        
        slotCols = rowCols[2:]
        rowFreeSlotsList = findSlots(slotCols)

        allSlots.append(slot(rowDate, rowDay, rowFreeSlotsList))
    
    return allSlots

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
    
if __name__=="__main__":
    with open('./temp/temp.html', 'r') as file:
        allSlots = parsePage(file.read())
    
    for x in allSlots:
        print(f"{x.date} {x.slots}")
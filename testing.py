
def parsePage(pageString):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(pageString, 'html.parser')

    slotTable = soup.find(id="myform").table.tbody.table
    table_body = slotTable.find("tbody")
    rows = table_body.find_all("tr")[2:]


    
if __name__=="__main__":
    with open('./temp/temp.html', 'r') as file:
        parsePage(file.read())
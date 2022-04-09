from autoBrowse import getTPDS
from db_helper import checkModNum

notHitLimit = True
count = 0

while(notHitLimit):
    TPDS_errorCode = getTPDS(checkModNum)
    if(TPDS_errorCode == 0):
        notHitLimit = False
        print("ENDED")
        break
    
    count+=1

print(f"Number of tries: {count}")
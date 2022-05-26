from datetime import datetime
import time

now = datetime.now()
dtString = now.strftime('%H:%M:%S')
time.sleep(1)
now1 = datetime.now()
dtString1 = now1.strftime('%H:%M:%S')
a=int(dtString[6:9])
b=int(dtString1[6:9])
print(a-b)
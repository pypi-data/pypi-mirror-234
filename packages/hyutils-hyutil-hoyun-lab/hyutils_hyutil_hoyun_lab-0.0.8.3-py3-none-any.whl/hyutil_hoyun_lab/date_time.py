import datetime

"""
방법1
from datetime import datetime
dt = datetime.now()
dt.microsecond
방법2
from datetime import datetime
dt = datetime.now()
print dt.microsecond/1000 + dt.second*1000

밀리 초 단위로 현재 UTC 시간을 얻는 가장 간단한 방법
# timeutil.py
import datetime
def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)
    
# sample.py
import timeutil
timeutil.get_epochtime_ms()


import datetime
t = datetime.datetime(2023, 9, 7, 7, 32, 45)
s = t.strftime('%Y-%m-%d %H:%M:%S')
print(s)

"""
def get_epochtime_ms():
    # dt = datetime.now()
    # print(f'dt:{dt}')
    return round(datatime.datetime.utcnow().timestamp() * 1000)

def get_datetime_string():
    current = datetime.datetime.now()
    s = current.strftime('%Y%m%d_%H%M%S')
    return s
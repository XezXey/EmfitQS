import requests
import re
import pandas as pd
import time
import _thread
import matplotlib.pyplot as plt

exit_flag = 0
emfit_qs_value = {}

def input_thread():
    global exit_flag 
    exit_flag = int(input("Press 1 to terminate : "))
    
exit_flag = _thread.start_new_thread(input_thread, ( ))

while True:
    emfit_qs_value.setdefault('timestamp_from_machine', [])
    r = requests.get("http://10.204.161.78/dvmstatus.htm")
    emfit_qs_value['timestamp_from_machine'].append(str(time.time()))
    pattern = re.compile(r"[(A-Z_)]{1,}[(=0-9.)]{1,}\w+")
    m = re.findall(pattern, str(r.content))
    for each_value in m:
        label, value = each_value.split('=')
        emfit_qs_value.setdefault(label, [])
        emfit_qs_value[label].append(value)
    time.sleep(1)
    if exit_flag == 1:
        break

print("Writing data...", end='') 
emfit_df = pd.DataFrame.from_dict(emfit_qs_value)
emfit_df.to_csv("emfit_data.csv")
print("Done!")
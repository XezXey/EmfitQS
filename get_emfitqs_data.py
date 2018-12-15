import requests
import re
import datetime
import pandas as pd
import time
import _thread
import matplotlib.pyplot as plt
import os
import sys


exit_flag = 0
emfit_qs_value = {}
path = './dataset_emfitqs/'

def input_thread():
    global exit_flag 
    exit_flag = int(input("Press 1 to terminate : "))
    
exit_flag = _thread.start_new_thread(input_thread, ( ))
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
path = path + sys.argv[1] + '_' + start_time + '/'

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

# Trying to make directory if it's not exist
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: #Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

print("Writing data...", end='')


filename = sys.argv[1] + '_' + start_time + "_emfit_data.csv"
emfit_df = pd.DataFrame.from_dict(emfit_qs_value)
emfit_df.to_csv(path + filename)
print("Done!")

import requests
import re
import datetime
import pandas as pd
import time
import _thread
import matplotlib.pyplot as plt
import os
import sys


emfit_qs_value = {} # Storing emfitqs data
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
path = './dataset_emfitqs/'

path = path + sys.argv[1] + '/'
# Trying to make directory if it's not exist
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: #Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

def input_thread():
    global exit_flag 
    exit_flag = int(input("Press 1 to terminate : "))
    
#exit_flag = _thread.start_new_thread(input_thread, ( ))
filename = sys.argv[1] + '_' + start_time + "_emfit_data.csv"
header = "timestamp_from_machine,SER,TS,TS_R,PRES,HR,HR_DM,RR,RR_DM,ACT,ACT_DM,FW,END\n"
filestream = open(path + filename, "w+")
filestream.write(header)
write_data = ""
pattern = re.compile(r"[(A-Z_)]{1,}[(=0-9.)]{1,}\w+")
while True:
    emfit_qs_value.setdefault('timestamp_from_machine', [])
    try:
        r = requests.get("http://10.204.161.74/dvmstatus.htm")
        m = re.findall(pattern, str(r.content))
    except:
        print(sys.exc_info()[0])
        print('Timeout...Reconnecting...')
        continue
    emfit_qs_value['timestamp_from_machine'].append(str(time.time()))
    write_data = str(time.time()) + ','
    for each_value in m:
        label, value = each_value.split('=')
        write_data = write_data + value + ","
        emfit_qs_value.setdefault(label, [])
        emfit_qs_value[label].append(value)
    
    write_data = write_data[:-1] + "\n"
    print("Each data = " + write_data[:-1])
    filestream.write(write_data)
    write_data = ""
    time.sleep(1)

print("Writing data...", end='')


emfit_df = pd.DataFrame.from_dict(emfit_qs_value)
emfit_df.to_csv(path + "_df_" +filename)
print("Done!")

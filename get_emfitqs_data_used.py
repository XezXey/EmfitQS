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
start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
path = './dataset_emfitqs/'

path = path + sys.argv[1] + '_' + start_time + '/'
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
while True:
    emfit_qs_value.setdefault('timestamp_from_machine', [])
    r = requests.get("http://10.204.161.123/dvmstatus.htm")
    #print(r.content)
    emfit_qs_value['timestamp_from_machine'].append(str(time.time()))
    write_data = str(time.time()) + ','
    pattern = re.compile(r"[(A-Z_)]{1,}[(=0-9.)]{1,}\w+")
    m = re.findall(pattern, str(r.content))
    for each_value in m:
        label, value = each_value.split('=')
        write_data = write_data + value + ","
        emfit_qs_value.setdefault(label, [])
        emfit_qs_value[label].append(value)
        #print(write_data, end="")
    
    write_data = write_data[:-1] + "\n"
    print("Each data = " + write_data[:-1])
    filestream.write(write_data)
    write_data = ""
    time.sleep(1)
    if exit_flag == 1:
        break

print("Writing data...", end='')


emfit_df = pd.DataFrame.from_dict(emfit_qs_value)
emfit_df.to_csv(path + "_df_" +filename)
print("Done!")

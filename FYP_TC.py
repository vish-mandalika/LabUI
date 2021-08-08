#FYP

#PLC_USERNAME = 'plc_username'
#PLC_PASSWORD = 'plc_password'
#ROUTE_NAME = 'RouteToViswa'
#HOSTNAME = 'viswa'

import pyads
import pandas as pd
import numpy as np
import os
import time
from ctypes import sizeof
from datetime import datetime

SENDER_AMS = '192.168.0.1'
PLC_IP = '192.168.0.111.1.1'

# Communicating with the PLC over port 851.
#plc = pyads.Connection(PLC_IP, 851) 
#plc.open() # Opening the connection
#sin_vals = plc.read_by_name('MAIN.arr1', pyads.PLCTYPE_ARR_REAL(100))

df = pd.DataFrame()
rdata_col = np.array([1, 2, 3, 4, 5, 6])
tdata_col = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5])
df['Time(s)'] = tdata_col.tolist()
df['Amplitude(mm)'] = rdata_col.tolist()
path = 'C:/Users/viswa/FYPS12021/rawdata/'
now = datetime.now()
stamp = now.strftime("%d-%m-%Y__%H-%M-%S")
print(stamp)
df.to_csv(rf'{path}rawdata_{stamp}.csv',index= False, header=True)
#print(a)
   

#plc.close()


"""
# Reading value from the GVL file for variable 'someVar'
i = plc.read_by_name("GVL.someVar") 
print("someVar  = " + str(i))

print("\nNow changing i = 10:")
i = 10

# Writing to the someVar variable in the GVL file
plc.write_by_name("GVL.someVar", i)

# Reading updated value 
i = plc.read_by_name("GVL.someVar") 
print("\nUpdated someVar = " +str(i))
"""





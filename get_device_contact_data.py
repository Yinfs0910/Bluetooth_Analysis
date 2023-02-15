import os
import json
import matplotlib.pyplot as plt
import powerlaw
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import pickle
import time
from multiprocessing import Pool
import os
import seaborn as sns
from itertools import product

# Load setting.py
from setting import *

# Load bluetooth_class_device.py
from bluetooth_class_device import *

# Load summarize_device_classes.py
from summarize_device_classes import get_id_name_list,get_device_class

# Load make_contact_histogram.py
from make_contact_histogram import *



def get_device_contact_data(id_name_list):
  # List to save all the data
  device_contact_count = {}
  deviceName_count = 0

  for id_name in id_name_list:
    # List to save device and contact
    device_class_count_dict = {}
    hwAddrHash_count_dict = {}
    # Bluetooth file paths
    BLUETOOTH_LOG_PATH = 'phase-2' + '/' + id_name + '/bluetooth.log'
    print('* Starting to read bluetooth data file:', BLUETOOTH_LOG_PATH)

    # Reading the file
    try:
      infile = open(BLUETOOTH_LOG_PATH, 'r', errors='ignore')
    except FileNotFoundError:
      print(BLUETOOTH_LOG_PATH, 'does not exist, cannnot open, skip..')
      continue

    # for each record
    for line in infile:
      # extract hwAddressHash, deviceClass, and majorDeviceClass
      record_dict = json.loads(line)
      timestamp = int(str(record_dict['timestamp'])[:10])
      hwAddrHash = record_dict['data'][0]['bluetooth']['hwAddrHash']
      deviceClass = str(record_dict['data'][0]['bluetooth']['deviceClass'])
      majorDeviceClass = str(record_dict['data'][0]['bluetooth']['majorDeviceClass'])
      rssi = int(record_dict['data'][0]['bluetooth']['strength'])

      # Checking whether timestamp is between START_UNIXTIME and END_UNIXTIME
      if timestamp >= START_UNIXTIME and timestamp < END_UNIXTIME:
        pass
      else:
        continue

      # Checking RSSI settings
      if RSSI_ENABLE == True and rssi >= RSSI_THRESHOLD:
        pass
      elif RSSI_ENABLE == False:
        pass
      else:
        continue

      # Checking MATCH_LIST_ENABLE flag
      if MATCH_LIST_ENABLE == False:



        if DEVICECLASS_LIST_ENABLE == True and deviceClass in DEVICECLASS_TABLE.keys():

          if DEVICECLASS_TABLE[deviceClass] in DEVICECLASS_LIST:
            # Counting contact frequencies
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
              # Counting encoutered devices
              if deviceClass not in device_class_count_dict:
                device_class_count_dict[deviceClass] = 1
              else:
                device_class_count_dict[deviceClass] += 1
            else:
              # Counting contact frequencies
              hwAddrHash_count_dict[hwAddrHash] += 1

        if MAJORDEVICECLASS_LIST_ENABLE == True and str(majorDeviceClass) in DEVICECLASS_TABLE.keys():
          if MAJORDEVICECLASS_TABLE[majorDeviceClass] in DEVICECLASS_LIST:
            # Counting contact frequencies
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
              # Counting encoutered devices
              if majorDeviceClass not in device_class_count_dict:
                device_class_count_dict[deviceClass] = 1
              else:
                device_class_count_dict[deviceClass] += 1
            else:
              # Counting contact frequencies
              hwAddrHash_count_dict[hwAddrHash] += 1
      else:

        if 'deviceName' in record_dict['data'][0]['bluetooth']:
          # Checking deviceName matches MATCH_LIST
          deviceName = record_dict['data'][0]['bluetooth']['deviceName']

          if check_match_list(deviceName):
            deviceName_count += 1
            # Counting contact frequencies
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1
            continue

        if DEVICECLASS_LIST_ENABLE == True and deviceClass in DEVICECLASS_TABLE.keys():

          if DEVICECLASS_TABLE[deviceClass] in DEVICECLASS_LIST:
            # Counting contact frequencies
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
              # Counting encoutered devices
              if deviceClass not in device_class_count_dict:
                device_class_count_dict[deviceClass] = 1
              else:
                device_class_count_dict[deviceClass] += 1
            else:
              # Counting contact frequencies
              hwAddrHash_count_dict[hwAddrHash] += 1

        if MAJORDEVICECLASS_LIST_ENABLE == True and str(majorDeviceClass) in DEVICECLASS_TABLE.keys():
          if MAJORDEVICECLASS_TABLE[majorDeviceClass] in MAJORDEVICECLASS_LIST:

            if MAJORDEVICECLASS_TABLE[majorDeviceClass] in DEVICECLASS_LIST:
              # Counting contact frequencies
              if hwAddrHash not in hwAddrHash_count_dict:
                hwAddrHash_count_dict[hwAddrHash] = 1
                # Counting encoutered devices
                if majorDeviceClass not in device_class_count_dict:
                  device_class_count_dict[deviceClass] = 1
                else:
                  device_class_count_dict[deviceClass] += 1
              else:
                # Counting contact frequencies
                hwAddrHash_count_dict[hwAddrHash] += 1

    # Saving the encountered devices and contact frequency each id
    device_contact_count[sum(device_class_count_dict.values())] = sum(hwAddrHash_count_dict.values())
    # close file
    infile.close()


  return device_contact_count


def multiprocess_worker1(id_name):
  print('\nID_NAME:', id_name)
  # Reading bluetooth data file and counting contact frequency
  id_name_mod_list = [id_name]
  frequency_count_dict = get_device_contact_data(id_name_mod_list)
  return frequency_count_dict




if __name__ == '__main__':
  # Reading the ID list
  file_dir = "phase-2"
  id_list = os.listdir(file_dir)
  id_list.pop(-1)

  # Reading bluetooth data file, counting encountered device and contact frequency
  with ProcessPoolExecutor(max_workers=60) as ppe:
    frequency_count_dict_list_tmp = [ppe.submit(multiprocess_worker1, id_name) for id_name in id_list]
    frequency_count_dict_list = [obj.result() for obj in frequency_count_dict_list_tmp]

  # Saving the file
  with open('contact_data' + '.pkl', 'wb') as f:
    pickle.dump(frequency_count_dict_list, f, pickle.HIGHEST_PROTOCOL)





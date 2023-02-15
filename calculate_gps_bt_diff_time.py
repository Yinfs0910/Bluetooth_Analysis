#!/usr/bin/env python3
#
# usage: calculate_gps_bt_diff_time.py 
#
import os
import sys
import json
import matplotlib.pyplot as plt

from settings import *
from summarize_device_classes import get_id_name_list


if __name__ == '__main__':
  # create a directory to save figures
  save_data_dir_path = './time_difference'
  os.makedirs(save_data_dir_path, exist_ok=True)


  id_name_list = get_id_name_list()
  id_name_list.remove('last_status')
  #print(id_name_list)

  for id_name in id_name_list:
    # Bluetooth file paths
    BLUETOOTH_LOG_PATH = './'+MAIN_DIRNAME+'/'+PHASE+'/'+id_name+'/bluetooth.log'
    print('* Starting to read bluetooth data file:', BLUETOOTH_LOG_PATH)

    # Reading the file 
    try: 
      infile = open(BLUETOOTH_LOG_PATH, 'r')
    except FileNotFoundError:
      print(BLUETOOTH_LOG_PATH, 'does not exist, cannnot open, skip..')
      continue

    bluetooth_timestamps_list = []

    # for each record
    for line in infile:
      # extract hwAddressHash, deviceClass, and majorDeviceClass
      record_dict = json.loads(line)
      timestamp = int(str(record_dict['timestamp'])[:10])

      # Checking whether timestamp is between START_UNIXTIME and END_UNIXTIME
      if timestamp >= START_UNIXTIME and timestamp < END_UNIXTIME:
        bluetooth_timestamps_list.append( timestamp )
      else:
        continue

    infile.close()


    # GPS file paths
    GPS_LOG_PATH = './'+MAIN_DIRNAME+'/'+PHASE+'/'+id_name+'/gps.log'
    print('* Starting to read GPS data file:', GPS_LOG_PATH)

    # Reading the file 
    try: 
      infile = open(GPS_LOG_PATH, 'r')
    except FileNotFoundError:
      print(GPS_LOG_PATH, 'does not exist, cannnot open, skip..')
      continue

    gps_timestamps_list = []

    # for each record
    for line in infile:
      # extract hwAddressHash, deviceClass, and majorDeviceClass
      record_dict = json.loads(line)
      timestamp = int(str(record_dict['timestamp'])[:10])

      # Checking whether timestamp is between START_UNIXTIME and END_UNIXTIME
      if timestamp >= START_UNIXTIME and timestamp < END_UNIXTIME:
        gps_timestamps_list.append( timestamp )
      else:
        continue

    infile.close()


    # check time difference
    bt_minus_gps_time_diffs_list = []
    if len(bluetooth_timestamps_list) > 1 and len(gps_timestamps_list) > 1:
      print('bluetooth:', bluetooth_timestamps_list[:10])
      print('gps:', gps_timestamps_list[:10])
      gps_index_now = 0
      for i in range(len(bluetooth_timestamps_list)):
        while gps_timestamps_list[ gps_index_now ] < bluetooth_timestamps_list[i] and gps_index_now < len(gps_timestamps_list)-1:
          gps_index_now += 1
        #if gps_timestamps_list[ gps_index_now ] - bluetooth_timestamps_list[i] < 0:
        #  print(gps_timestamps_list[ gps_index_now ] - bluetooth_timestamps_list[i], gps_index_now, len(gps_timestamps_list))
        if gps_index_now != len(gps_timestamps_list)-1:
          bt_minus_gps_time_diffs_list.append( gps_timestamps_list[ gps_index_now ] - bluetooth_timestamps_list[i] )
        #sys.exit(0)
        #if i >= 10:
        #  break
      #print(bt_minus_gps_time_diffs_list)

      plt.hist(bt_minus_gps_time_diffs_list, bins=50, log=True)
      plt.savefig(save_data_dir_path+'/time_diff-'+id_name+'.png')
      plt.clf()



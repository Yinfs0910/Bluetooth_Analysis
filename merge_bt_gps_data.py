#!/usr/bin/env python3
#
# usage: python3 merge_bt_gps_data.py 
#
import os
import sys
import json
import matplotlib.pyplot as plt

from settings import *
from summarize_device_classes import get_id_name_list
from regional_mesh_codes import RegionalMeshCode

if __name__ == '__main__':
  # create a directory to save figures
  save_data_dir_path = './bt_gps_merged/phase-2'
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

    bt_timestamps_list = []
    bt_hwAddrHashes_list = []
    bt_deviceClasses_list = []
    bt_majorDeviceClasses_list = []
    bt_rssis_list = []

    # for each record
    for line in infile:
      # extract hwAddressHash, deviceClass, and majorDeviceClass
      record_dict = json.loads(line)
      timestamp = int(str(record_dict['timestamp'])[:10])
      hwAddrHash = str(record_dict['data'][0]['bluetooth']['hwAddrHash'])
      deviceClass = str(record_dict['data'][0]['bluetooth']['deviceClass'])
      majorDeviceClass = str(record_dict['data'][0]['bluetooth']['majorDeviceClass'])
      rssi = int(record_dict['data'][0]['bluetooth']['strength'])

      # Checking whether timestamp is between START_UNIXTIME and END_UNIXTIME
      if timestamp >= START_UNIXTIME and timestamp < END_UNIXTIME:
        bt_timestamps_list.append( timestamp )
        bt_hwAddrHashes_list.append( hwAddrHash )
        bt_deviceClasses_list.append( deviceClass )
        bt_majorDeviceClasses_list.append( majorDeviceClass )
        bt_rssis_list.append( rssi )
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
    gps_latitudes_list = []
    gps_longitudes_list = []
    gps_accuracies_list = []

    # for each record
    for line in infile:
      # extract hwAddressHash, deviceClass, and majorDeviceClass
      record_dict = json.loads(line)
      timestamp = int(str(record_dict['timestamp'])[:10])
      latitude = float(record_dict['data'][0]['gps']['latitude'])
      longitude = float(record_dict['data'][0]['gps']['longitude'])
      accuracy = float(record_dict['data'][0]['gps']['accuracy'])
      #print(timestamp, latitude, longitude, accuracy)
      #sys.exit(0)

      # Checking whether timestamp is between START_UNIXTIME and END_UNIXTIME
      if timestamp >= START_UNIXTIME and timestamp < END_UNIXTIME:
        gps_timestamps_list.append( timestamp )
        gps_latitudes_list.append( latitude )
        gps_longitudes_list.append( longitude )
        gps_accuracies_list.append( accuracy )
      else:
        continue

    infile.close()
    #sys.exit(0)

    outfilename = save_data_dir_path + '/'+id_name+'.csv'
    outfile = open(outfilename, 'w')

    # check time difference
    if len(bt_timestamps_list) > 1 and len(gps_timestamps_list) > 1:
      #print('bluetooth:', bt_timestamps_list)
      #print('gps:', gps_timestamps_list)
      gps_index_now = 0
      for i in range(len(bt_timestamps_list)):

        while gps_timestamps_list[ gps_index_now ] < bt_timestamps_list[i] and gps_index_now < len(gps_timestamps_list)-1:
          gps_index_now += 1

        if gps_index_now != len(gps_timestamps_list)-1:
          lon = gps_longitudes_list[ gps_index_now ]
          lat = gps_latitudes_list[ gps_index_now ]
          rmc = RegionalMeshCode((lon, lat))

          line_to_write = str(bt_timestamps_list[i])+','+str(bt_hwAddrHashes_list[i])+','+str(bt_deviceClasses_list[i])+','+str(bt_majorDeviceClasses_list[i])+','+str(bt_rssis_list[i])+','+str(gps_timestamps_list[ gps_index_now ])+','+str(gps_latitudes_list[ gps_index_now ])+','+str(gps_longitudes_list[ gps_index_now ])+','+str(gps_accuracies_list[ gps_index_now ])+','+str(rmc.grid1st())+','+str(rmc.grid2nd())+','+str(rmc.grid3rd())+','+str(rmc.grid4th())+','+str(rmc.grid5th())+','+str(rmc.grid6th())+'\n'
          outfile.write(line_to_write)

    outfile.close()
    #sys.exit(0)

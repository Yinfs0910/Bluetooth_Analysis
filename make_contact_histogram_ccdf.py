#!/usr/bin/env python3
# coding: utf-8

#######################################################
# usage: First install modules using requirements.txt #
#        $ sudo pip3 install -r requirements.txt      #
#                                                     #
#        Edit setting.py first as you like,           # 
#        then run the following command               #
#        $ python3 make_contact_histogram.py          #
#######################################################
import os
import json
import matplotlib.pyplot as plt
import powerlaw

from concurrent.futures import ProcessPoolExecutor

# Load settings.py 
from settings import *

# Load bluetooth_class_device.py
from bluetooth_class_device import *

# Load summarize_device_classes.py
from summarize_device_classes import get_id_name_list


# Functions
def read_bluetooth_data(id_name_list):

  # List to save contact frequency
  hwAddrHash_count_dict = {}
  deviceClass_count = 0
  majorDeviceClass_count = 0
  deviceName_count = 0

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

        ## Counting contact frequencies
        #if hwAddrHash not in hwAddrHash_count_dict:
        #  hwAddrHash_count_dict[hwAddrHash] = 1
        #else:
        #  hwAddrHash_count_dict[hwAddrHash] += 1

        if DEVICECLASS_LIST_ENABLE == True and deviceClass in DEVICECLASS_TABLE.keys():

          if DEVICECLASS_TABLE[deviceClass] in DEVICECLASS_LIST:
            # Counting contact frequencies
            deviceClass_count += 1
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1
            continue

        if MAJORDEVICECLASS_LIST_ENABLE == True and str(majorDeviceClass) in MAJORDEVICECLASS_TABLE.keys():
          if MAJORDEVICECLASS_TABLE[majorDeviceClass] in MAJORDEVICECLASS_LIST:
            # Counting contact frequencies
            majorDeviceClass_count += 1
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1

      else:

        if 'deviceName' in record_dict['data'][0]['bluetooth']:
          # Checking deviceName matches MATCH_LIST
          deviceName = record_dict['data'][0]['bluetooth']['deviceName']

          if check_match_list(deviceName):
            # Counting contact frequencies
            deviceName_count += 1
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1
            continue

        if DEVICECLASS_LIST_ENABLE == True and deviceClass in DEVICECLASS_TABLE.keys():

          if DEVICECLASS_TABLE[deviceClass] in DEVICECLASS_LIST:
            # Counting contact frequencies
            deviceClass_count += 1
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1
            continue

        if MAJORDEVICECLASS_LIST_ENABLE == True and str(majorDeviceClass) in DEVICECLASS_TABLE.keys():
          if MAJORDEVICECLASS_TABLE[majorDeviceClass] in MAJORDEVICECLASS_LIST:
            # Counting contact frequencies
            majorDeviceClass_count += 1
            if hwAddrHash not in hwAddrHash_count_dict:
              hwAddrHash_count_dict[hwAddrHash] = 1
            else:
              hwAddrHash_count_dict[hwAddrHash] += 1
    # close file
    infile.close()

  print('*** Count summary of '+str(id_name_list)+':', deviceName_count, deviceClass_count, majorDeviceClass_count, '***')
  return hwAddrHash_count_dict


def check_match_list(deviceName):
  matched_flag = False

  for device in MATCH_LIST:
    if device.lower() in deviceName.lower():
      matched_flag = True
      break

  return matched_flag


def make_histogram(count_dict, nbins, outfilename='histogram_ALL.png'):
  # Caluculating the histogram
  contact_frequency_list = list(count_dict.values())
  if len(contact_frequency_list) > 0:
    n, bins, patches = plt.hist(contact_frequency_list, bins=nbins)
    plt.clf()
    bins_mod = []
    for i in range(len(bins)-1):
      bins_mod.append( (bins[i] + bins[i+1])/2 )
    n_mod = [ float(n[-1]) / len(contact_frequency_list) ]
    for i in range(1, len(n)):
      to_append = n_mod[0] + float(n[-(i+1)]) / len(contact_frequency_list)
      n_mod = [ to_append ] + n_mod
   
    # Drawing with double logarithmic plot
    #plt.loglog(bins_mod, n, marker="o", linestyle="-")
    #plt.loglog(bins_mod, n, marker="o", linestyle="")
    plt.loglog(bins_mod, n_mod, marker="o", linestyle="")
    plt.xlabel('# of contacts')
    plt.ylabel('Frequency')
    # Path to save the histogram
    HISTOGRAM_IMAGE_FILENAME = './'+HISTOGRAM_DIRNAME+'/'+outfilename
    plt.savefig(HISTOGRAM_IMAGE_FILENAME)
    plt.clf()


def calculate_powerlaw_exponent(count_dict, idname):
  contact_frequency_list = list(count_dict.values())

  fit = powerlaw.Fit(contact_frequency_list)

  fitness_tuple = fit.distribution_compare('power_law', 'exponential')

  if fitness_tuple[0] > fitness_tuple[1]:
    dominant_distribution =  'power_law'
  else:
    dominant_distribution =  'exponential'

  print('#'*80)
  print('id name:', idname)
  print('Alpha:', fit.power_law.alpha)
  print('Sigma:', fit.power_law.sigma)
  print('Fitness (power_law vs. exponential):', fitness_tuple)
  print('-->', dominant_distribution, 'is dominant!')
  print('#'*80)


# For multi-processing
def multiprocess_worker1(id_name):
  print('\nID_NAME:', id_name)
  # Reading bluetooth data file and counting contact frequency
  id_name_mod_list = [id_name]
  frequency_count_dict = read_bluetooth_data(id_name_mod_list)

  # Drawing histograms of each participant
  make_histogram(frequency_count_dict, nbins=HISTOGRAM_BINS, outfilename='histogram_'+id_name+'.png')

  # Calculating the power-law exponent
  calculate_powerlaw_exponent(frequency_count_dict, id_name)

  return frequency_count_dict


def make_histogram_all(frequency_count_dict_list, id_name_list):
  # Counting contact frequency
  print('\nID_NAME: ALL')
  frequency_count_dict = {}
  for dict_tmp in frequency_count_dict_list:
    for k, v in dict_tmp.items():
      if k not in frequency_count_dict:
        frequency_count_dict[k] = v
      else:
        frequency_count_dict[k] += v

  # Drawing the histogram of all participants
  make_histogram(frequency_count_dict, nbins=HISTOGRAM_BINS)

  # Calculating the power-law exponent
  calculate_powerlaw_exponent(frequency_count_dict, id_name_list)

  return frequency_count_dict



### Main program ###
if __name__ == '__main__':
  print('### Starting to create the contact histogram ###')
  # Create a directory named histograms
  histogram_directory_path = './'+HISTOGRAM_DIRNAME
  os.makedirs(histogram_directory_path, exist_ok=True)

  if DRAW_ALL_HISTOGRAMS_ENABLE == False:
    # Reading bluetooth data file and counting contact frequency
    frequency_count_dict = read_bluetooth_data(ID_NAME_LIST)

    # Drawing the histogram of contact frequency
    make_histogram(frequency_count_dict, nbins=HISTOGRAM_BINS)

    # Calculating the power-law exponent
    calculate_powerlaw_exponent(frequency_count_dict, ID_NAME_LIST)

  else:
    # get all id names from /MAIN_DIRNAME/PHASE/
    id_name_list = get_id_name_list()
    id_name_list.remove("last_status")
   
    # multi-processing
    # https://qiita.com/maru_maruo/items/78da1545ce84014abca9
    frequency_count_dict_list = []
    with ProcessPoolExecutor(max_workers=30) as ppe:
      frequency_count_dict_list_tmp = [ ppe.submit(multiprocess_worker1, id_name) for id_name in id_name_list]
      frequency_count_dict_list = [ obj.result()  for obj in frequency_count_dict_list_tmp ]
      #print(frequency_count_dict_list)

    make_histogram_all(frequency_count_dict_list, id_name_list)
  
  print('### Finished creating the contact histogram ###')


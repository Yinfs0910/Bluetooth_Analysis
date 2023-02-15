#!/usr/bin/env python3
# coding: utf-8
################################################
#                                              #
# usage: $ python3 summarize_device_classes.py #
#                                              #
################################################
import subprocess
import sys
import json

# Load settings.py
from settings import MAIN_DIRNAME, PHASE
# Load bluetooth_class_device.py
from bluetooth_class_device import DEVICECLASS_TABLE, MAJORDEVICECLASS_TABLE



# functions
def get_id_name_list():
  id_name_path = './'+MAIN_DIRNAME+'/'+PHASE+'/'

  try:
    res = subprocess.run(['ls', id_name_path], stdout=subprocess.PIPE)
  except:
    print("ls does not work, exit..")
    sys.exit(1)

  return res.stdout.decode('utf-8').split('\n')[:-1]


def get_device_class(id_name_list):
  device_class_dict = {}
  major_device_class_dict = {}

  for id_name in id_name_list:
    bluetooth_log_path = './'+MAIN_DIRNAME+'/'+PHASE+'/'+id_name+'/bluetooth.log'

    try:
      infile = open(bluetooth_log_path, 'r')
    except FileNotFoundError:
      print(bluetooth_log_path, 'does not exist, cannot open, skip..')
      continue

    for line in infile:
      json_dict = json.loads(line)

      device_class = json_dict['data'][0]['bluetooth']['deviceClass']
      if str(device_class) not in device_class_dict:
        device_class_dict[str(device_class)] = 1
      else:
        device_class_dict[str(device_class)] += 1

      major_device_class = json_dict['data'][0]['bluetooth']['majorDeviceClass']
      if str(major_device_class) not in major_device_class_dict:
        major_device_class_dict[str(major_device_class)] = 1
      else:
        major_device_class_dict[str(major_device_class)] += 1
    # file close()
    infile.close()

  # sort by value
  sorted_device_class_dict = dict(sorted(device_class_dict.items(), key=lambda x:x[1], reverse=True))
  sorted_major_device_class_dict = dict(sorted(major_device_class_dict.items(), key=lambda x:x[1], reverse=True))

  return sorted_device_class_dict, sorted_major_device_class_dict



### main program ###
if __name__ == '__main__':
  print('### Starting to summarize deviceClass and majorDeviceClass ###')
  print('')

  # get all id names from /MAIN_DIRNAME/PHASE/
  id_name_list = get_id_name_list()
  #print(id_name_list)

  # get frequencies of deviceClass and majorDeviceClass
  device_class_dict, major_device_class_dict = get_device_class(id_name_list)

  # show device_class_dict
  print('### deviceClass ###')
  print('DEVICE_CLASS_ID(DEVICE_CLASS) --> COUNT')
  print('---')
  for k, v in device_class_dict.items():
    if k in DEVICECLASS_TABLE:
      print(k+'('+DEVICECLASS_TABLE[k]+')--> '+str(v))
    else:
      print(k+'(???)--> '+str(v))
  print('')

  # show major_device_class_dict
  print('### majorDeviceClass ###')
  print('DEVICE_CLASS_ID(DEVICE_CLASS) --> COUNT')
  print('---')
  for k, v in major_device_class_dict.items():
    if k in MAJORDEVICECLASS_TABLE:
      print(k+'('+MAJORDEVICECLASS_TABLE[k]+')--> '+str(v))
    else:
      print(k+'(???)--> '+str(v))
 
  print('### Finished summarizing deviceClass and majorDeviceClass ###')


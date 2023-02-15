#!/usr/bin/env python3
# coding: utf-8
#
# usage: $ python3 convert_gpslog_json2csv.py
import sys
import json

outfilename = './gps.csv'

with open(outfilename, 'w') as outfile:
  outfile.write('id,timestamp,latitude,longitude,accuracy\n')
  infilename = './gps.log'
  
  with open(infilename, 'r') as infile:
    for line in infile:
      dict_data = json.loads(line)
      #print(dict_data)
      output_line = str(dict_data['id'])+','+str(dict_data['timestamp'])+','+str(dict_data['data'][0]['gps']['latitude'])+','+str(dict_data['data'][0]['gps']['longitude'])+','+str(dict_data['data'][0]['gps']['accuracy'])+'\n'
      #print(output_line)
      outfile.write(output_line)


#
# usage: $ python3 make_contact_histogram_by_area.py
# 
import sys



from settings import *

CCDF_FLAG = True

if CCDF_FLAG == True:
  from make_contact_histogram_ccdf import *
else:
  from make_contact_histogram import *


infilename1 = './DATA/AREA_CODE.csv'
infilename2 = './DATA/ID_AREA.csv'


### Main program ###
if __name__ == '__main__':
  area_code_dict = {}
  area_id_count_dict = {}
  user_ids_by_area_list = []
  
  
  with open(infilename1, 'r') as infile1:
    for line in infile1:
      data_list = line.replace('\n', '').split(',')
      area_code_dict[ int(data_list[0]) ] = data_list[1]
  #print(area_code_dict, len(area_code_dict))
  
  for _ in range(len(area_code_dict)):
    user_ids_by_area_list.append([])
  #print(user_ids_by_area_list)
  
  
  with open(infilename2, 'r') as infile2:
    for line in infile2:
      data_list = line.replace('\n', '').split(',')
      user_id = data_list[0]
      area_id = int(data_list[1])
      user_ids_by_area_list[ area_id-1 ].append( user_id )
      if area_id not in area_id_count_dict:
        area_id_count_dict[ area_id ] = 1
      else:
        area_id_count_dict[ area_id ] += 1


  #print(area_id_count_dict)
  #print(user_ids_by_area_list)
  for k, v in sorted(area_id_count_dict.items(), key=lambda x:x[1], reverse=True):
  #  print(area_code_dict[k], v, user_ids_by_area_list[k-1], len(user_ids_by_area_list[k-1]))
    print(area_code_dict[k], v, user_ids_by_area_list[k-1])

    area_name_ja = area_code_dict[k]
    id_name_list = user_ids_by_area_list[k-1]

    # Reading bluetooth data file and counting contact frequency
    frequency_count_dict = read_bluetooth_data(id_name_list)

    # Drawing the histogram of contact frequency
    if CCDF_FLAG == True:
      make_histogram(frequency_count_dict, nbins=HISTOGRAM_BINS, outfilename='histogram_ccdf_'+area_name_ja+'.png')
    else:
      make_histogram(frequency_count_dict, nbins=HISTOGRAM_BINS, outfilename='histogram_'+area_name_ja+'.png')

    # Calculating the power-law exponent
    calculate_powerlaw_exponent(frequency_count_dict, id_name_list)



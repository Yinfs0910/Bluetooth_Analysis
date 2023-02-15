#
# usage: $ python3 count_userids_by_area.py
#
import sys

infilename1 = './DATA/AREA_CODE.csv'
infilename2 = './DATA/ID_AREA.csv'

area_code_dict = {}
area_id_count_dict = {}

with open(infilename1, 'r') as infile1:
  for line in infile1:
    data_list = line.replace('\n', '').split(',')
    area_code_dict[ int(data_list[0]) ] = data_list[1]
#print(area_code_dict)

with open(infilename2, 'r') as infile2:
  for line in infile2:
    data_list = line.replace('\n', '').split(',')
    area_id = int(data_list[1])
    if area_id not in area_id_count_dict:
      area_id_count_dict[ area_id ] = 1
    else:
      area_id_count_dict[ area_id ] += 1

#print(area_id_count_dict)
print('AREA_NAME,USER_ID_COUNT')
for k, v in sorted(area_id_count_dict.items(), key=lambda x:x[1], reverse=True):
  print(str(area_code_dict[k])+','+str(v))




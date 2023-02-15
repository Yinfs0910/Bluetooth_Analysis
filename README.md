# contact_analysis

## Install modules 
```
$ git clone https://github.com/naoyafujiwara/contact_analysis
$ sudo pip3 install -r requirements.txt

```


## Locate bluetooth and gps data in the current directory
- Path to Bluetooth log: ./MAIN_DIRNAME/PHASE/ID_NAME/bluetooth.log
- Path to GPS log: ./MAIN_DIRNAME/PHASE/ID_NAME/gps.log


## Edit settings.py first as you like
- MAIN_DIRNAME : Top directory name to save bluetooth and gps logs
- PHASE : Phase name in experiments
- ID_NAME_LIST : List of ID names [ID1, ID2, ...] (Disabled if DRAW_ALL_HISTOGRAMS_ENABLE flag is True)

- START_UNIXTIME : Unixtime to start data analysis
- END_UNIXTIME : Unixtime to end data analysis

- RSSI_ENABLE : True or False (Binary value) to enable or disable RSSI_THRESHOLD filter
- RSSI_THRESHOLD : Threshold to accept data (set to -63dBm in COCOA)

- HISTOGRAM_DIRNAME : Directory name to save contact histograms
- HISTOGRAM_BINS : # of bins in the contact histogram
- DRAW_ALL_HISTOGRAMS_ENABLE : True or False (Binary value) to enable or disable drawing all histograms

- MATCH_LIST_ENABLE : True or False (Binary value) to enable or disable MATCH_LIST filter
- MATCH_LIST : The contents of the filter

- DEVICECLASS_LIST_ENABLE : True or False (Binary value) to enable or disable DEVICECLASS_LIST filter
- DEVICECLASS_LIST : The contents of the filter

- MAJORDEVICECLASS_LIST_ENABLE : True or False (Binary value) to enable or disable MAJORDEVICECLASS_LIST filter
- MAJORDEVICECLASS_LIST : The contents of the filter


## Run the following command
```
$ python3 make_contact_histogram.py

```

## OUTPUT

- Standard output

```
$ python3 make_contact_histogram.py 
### Starting to create the contact histogram ###

ID_NAME: a01234
* Starting to read bluetooth data file: ./decrypted_data/phase1/a01234/bluetooth.log
Count summary: 0 1429 7
Calculating best minimal value for power law fit
################################################################################
Alpha: 3.070463817099154
Sigma: 0.3718662792056028
Fitness (power_law vs. exponential): (49.47320644181123, 0.0005538625819431783)
--> power_law is dominant!
################################################################################

ID_NAME: b56789
* Starting to read bluetooth data file: ./decrypted_data/phase1/b56789/bluetooth.log
Count summary: 0 2408 0
Calculating best minimal value for power law fit
################################################################################
Alpha: 1.8715671625039811
Sigma: 0.2250376736986115
Fitness (power_law vs. exponential): (28.41240809085128, 2.9587008603286445e-05)
--> power_law is dominant!
################################################################################

ID_NAME: ALL
* Starting to read bluetooth data file: ./decrypted_data/phase1/a01234/bluetooth.log
* Starting to read bluetooth data file: ./decrypted_data/phase1/b56789/bluetooth.log
Count summary: 0 3837 7
Calculating best minimal value for power law fit
################################################################################
Alpha: 2.4197598360190966
Sigma: 0.18329020668387114
Fitness (power_law vs. exponential): (119.25772141924594, 0.0018682779454588956)
--> power_law is dominant!
################################################################################
### Finished creating the contact histogram ###


```

- Another outputs: PNG files of contact histograms are created in the directory named HISTOGRAM_DIRNAME. 





# Summarize device classes

## Run the following command
```
$ python3 summarize_device_classes.py 

```


## OUTPUT

- Standard output

```
$ python3 summarize_device_classes.py 
### Starting to summarize deviceClass and majorDeviceClass ###

### deviceClass ###
DEVICE_CLASS_ID(DEVICE_CLASS) --> COUNT
---
7936(???)--> 27556
1084(AUDIO_VIDEO_VIDEO_DISPLAY_AND_LOUDSPEAKER)--> 3788
524(PHONE_SMART)--> 3504
268(COMPUTER_LAPTOP)--> 1020
260(COMPUTER_DESKTOP)--> 224
276(COMPUTER_PALM_SIZE_PC_PDA)--> 178
1060(AUDIO_VIDEO_SET_TOP_BOX)--> 137
1028(AUDIO_VIDEO_WEARABLE_HEADSET)--> 108
284(???)--> 78
1032(AUDIO_VIDEO_HANDSFREE)--> 57
1664(???)--> 37
1044(AUDIO_VIDEO_LOUDSPEAKER)--> 24
1048(AUDIO_VIDEO_HEADPHONES)--> 20
1796(WEARABLE_WRIST_WATCH)--> 13
272(COMPUTER_HANDHELD_PC_PDA)--> 10
520(PHONE_CORDLESS)--> 7
256(COMPUTER_UNCATEGORIZED)--> 7
1056(AUDIO_VIDEO_CAR_AUDIO)--> 4
2328(HEALTH_PULSE_RATE)--> 2
516(PHONE_CELLULAR)--> 2
2336(???)--> 2
1280(???)--> 2
1344(???)--> 1
1284(???)--> 1
1052(AUDIO_VIDEO_PORTABLE_AUDIO)--> 1
1408(???)--> 1
280(COMPUTER_WEARABLE)--> 1
1064(AUDIO_VIDEO_HIFI_AUDIO)--> 1

### majorDeviceClass ###
DEVICE_CLASS_ID(DEVICE_CLASS) --> COUNT
---
7936(UNCATEGORIZED)--> 27556
1024(AUDIO_VIDEO)--> 4140
512(PHONE)--> 3513
256(COMPUTER)--> 1518
1536(IMAGING)--> 37
1792(WEARABLE)--> 13
1280(PERIPHERAL)--> 5
2304(HEALTH)--> 4
### Finished summarizing deviceClass and majorDeviceClass ###

```


# Convert json-style gps.log to csv file

## Run the following command
```
$ mv (path to gps.log)
$ python3 convert_gpslog_json2csv.py

```


## OUTPUT

- No standard output. 

- A file named "gps.csv" is generated in the current directory. 



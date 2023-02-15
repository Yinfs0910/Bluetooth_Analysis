# Directory names
#MAIN_DIRNAME = '../../contact_phase2_test/contact_investigation_decode/output/'
MAIN_DIRNAME = '../output/'
PHASE = 'phase-2'
#PHASE = 'phase-1'
ID_NAME_LIST = []

# Analysis period (unixtime)
# Unixtime converter https://tool.konisimple.net/date/unixtime
#START_UNIXTIME = 1633046400 # 2021-10-01 00:00:00 JST
#START_UNIXTIME = 1635692400 # 2021-11-01 00:00:00
START_UNIXTIME = 1645455600 # 2022-02-22 00:00:00 JST
END_UNIXTIME   = 1647270000 # 2022-03-15 00:00:00 JST
#END_UNIXTIME   = 1647874800 # 2022-03-22 00:00:00 JST

# RSSI related (If RSSI >= RSSI_THRESHOLD, then accepted)
RSSI_ENABLE = True
RSSI_THRESHOLD = -63 # [dBm] <-- COCOA's threshold

# Regarding histogram
HISTOGRAM_DIRNAME = 'histograms'
HISTOGRAM_BINS = 1000
DRAW_ALL_HISTOGRAMS_ENABLE = True

# Regarding the match list
MATCH_LIST_ENABLE = False
MATCH_LIST = ['AQUOS', 'Xperia', 'sh', 'shv', 'shg', 'sense', 'Galaxy', 'LG', 'HUAWEI', 'arrows', 'Disney', 'OPPO', 'Pixel', 'TORQUE', 'ZTE', 'HTC', 'GRATINA', 'isai', 'Android', 'DIGNO', 'Nexus', 'Libero', 'MONO', 'BASIO', 'Qua', 'URBANO', 'iPhone', 'MacBook', 'iMac', 'LE', 'Fire', 'Nokia', 'Kindle', 'Pioneer', '小米', 'Apple', 'Bose', 'J:COM', 'Echo', 'iPad', 'TOUGHBOOK', 'V30+', 'V20 PRO', 'Mi 10', 'MARVERA', 'Redmi', 'Earphon', 'AUKEY', 'Anker', 'AirPods', 'Powerbeats', 'ANC', 'AVIOT', 'Aviot', 'Beoplay', 'QuietComfort', 'Earbuds', 'Creative', 'LBT', 'TWS0', 'GLIDiC', 'JVC', 'Jabra', 'Kenwood', 'Klipsch', 'MXH', 'NUARL', 'Audio', 'Onkyo', 'Owltech', 'SE04', 'Pioneer', 'SE-C', 'MOMENTUM', 'Shure', 'Soundpeats', 'TaoTronics', 'EAH-', 'Yamaha', 'TW-', 'technica', 'FLW TWS', 'SONY', 'JBL', 'Panasonic', 'RZ-', 'SoundCore', 'Speaker', 'SC-', 'Marshal', 'ELECOM', 'SANWA', 'JPR', 'JAPAN', 'GARMIN', 'Fit', 'TANITA', 'OMRON', 'Xiaomi', 'OPPO', 'Apple', 'SUUNTO', 'CASIO', 'SEIKO', 'SOMA', 'Withings', 'POLAR', 'watch', 'pencil', 'headset', 'versa', '-r', '-l', 'ath', 'lte']

# Regarding deviceClass
DEVICECLASS_LIST_ENABLE = True
DEVICECLASS_LIST = [
  'AUDIO_VIDEO_HEADPHONES',
  'AUDIO_VIDEO_PORTABLE_AUDIO',
  'AUDIO_VIDEO_WEARABLE_HEADSET',
  'COMPUTER_HANDHELD_PC_PDA',
  'COMPUTER_PALM_SIZE_PC_PDA',
  'COMPUTER_WEARABLE',
  'PHONE_CELLULAR',
  'PHONE_SMART',
  'WEARABLE_GLASSES',
  'WEARABLE_HELMET',
  'WEARABLE_JACKET',
  'WEARABLE_PAGER',
  'WEARABLE_UNCATEGORIZED',
  'WEARABLE_WRIST_WATCH'
]

# Regarding majorDeviceClass
MAJORDEVICECLASS_LIST_ENABLE = False
MAJORDEVICECLASS_LIST = [
  'PHONE',
  'WEARABLE'
]


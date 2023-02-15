# Reference of regional mesh (地域メッシュ) codes:
# https://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf
# https://qiita.com/yuusei/items/549402a80efd7e7192ef
# https://qiita.com/kota9/items/3cd8eb8f3df6d00e232b
# https://netfuku-yaro.com/2021/02/07/post-1046/
import math

class RegionalMeshCode:
  def __init__(self, coordinates):
    self.lon = coordinates[0]
    self.lat = coordinates[1]

  def grid1st(self): # 1次メッシュ(4桁) 分割なし
    return math.floor(self.lat*1.5)*100 + math.floor(self.lon-100)

  def grid2nd(self): # 2次メッシュ(6桁) 8分割
   return (self.grid1st()*100 
           + math.floor((self.lat*12)%8)*10 + math.floor((self.lon-100)*8)%8)

  def grid3rd(self): # 3次メッシュ(8桁) 8分割x10分割=80分割
    return (self.grid2nd()*100 # 2次メッシュ
            + math.floor((self.lat*120)%10)*10 + math.floor((self.lon-100)*80)%10)

  def grid4th(self): # 4次メッシュ(9桁) 8分割x10分割x2分割=160分割
    return (self.grid3rd()*10 # 3次メッシュ
            + (math.floor(self.lat*240)%2)*2 + math.floor((self.lon-100)*160)%2 + 1)

  def grid5th(self): # 5次メッシュ(10桁) 8分割x10分割x2分割x2分割=320分割
    return (self.grid4th()*10 # 4次メッシュ
            + (math.floor(self.lat*480)%2)*2 + math.floor((self.lon-100)*320)%2 + 1)

  def grid6th(self): # 6次メッシュ(10桁) 8分割x10分割x2分割x2分割x2分割=640分割
    return (self.grid5th()*10 # 5次メッシュ
            + (math.floor(self.lat*960)%2)*2 + math.floor((self.lon-100)*640)%2 + 1)

  def all(self):
    return [self.grid1st(), self.grid2nd(), self.grid3rd(), self.grid4th(), 
            self.grid5th(), self.grid6th()]


if __name__ == "__main__":

  # 東京都庁
  lon = 139.691774; lat = 35.689450
  rmc = RegionalMeshCode((lon, lat))

  print('1次地域メッシュ： ', rmc.grid1st())
  print('2次地域メッシュ： ', rmc.grid2nd())
  print('3次地域メッシュ： ', rmc.grid3rd())
  print('4次地域メッシュ： ', rmc.grid4th())
  print('5次地域メッシュ： ', rmc.grid5th())
  print('6次地域メッシュ： ', rmc.grid6th())
  print('All regional mesh codes:', rmc.all())


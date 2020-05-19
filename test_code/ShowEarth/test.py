import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib as mpl
import numpy as np
from pyecharts import Map
import math
from scipy.optimize import curve_fit
from pyecharts import Geo
data=pd.read_csv("virus.csv")
province_set={'湖北':11177,'广东':725,'浙江':724,'河南':566,'湖南':521,'安徽':408,\
          '江西':391,'重庆':312,'江苏':271,'山东':259,'四川':254,'北京':212,\
          '上海':203,'福建':179,'陕西':128,'广西':127,'黑龙江':121,'云南':114,\
          '河北':113,'辽宁':73,'海南':71,'山西':66,'天津':56,'甘肃':51,'贵州':46,\
          '内蒙古':34,'宁夏':31,'吉林':31,'新疆':24,'香港':15,'青海':13,'台湾':10,\
          '澳门':8,'西藏':1}
city_set={'青岛':46,'济南':42,'武汉':13603,'孝感':2313,'黄冈':2041,'深圳':351,'广州':298,\
          '珠海':82,'温州':438,'杭州':162,'宁波':141,'信阳':192,'南阳市':128,'郑州':120,\
          '长沙':196,'哈尔滨':100,'绥化':44,'上海':281,'福州':59,'厦门':25,'s石家庄':24,\
          '沧州':28,'邯郸':26,'唐山':23,'保定':18,'西安':88,'汉中':21,'南宁':32,'桂林':29,\
          '兰州':32,'长春':32,'吉林':5,'鄂尔多斯':11,'包头':10,'银川':29,'乌鲁木齐':19,\
          '香港':26,'西宁':15,'澳门':10,'合肥':128,'阜阳':113,'蚌埠':99,'南昌':168,'九江':97,\
          '赣州':64,'南京':65,'苏州':72,'徐州':52,'无锡':34,'重庆':426,'北京':315,'成都':109,\
          '南充':31,'天津':88,'昆明':41,'三亚':37,'海口':24,'晋中':30,'太原':12,'沈阳':25,\
          '大连':14,'盘锦':11,'毕节':21,'贵阳':18,'拉萨':1}
contry_set={"United States":13,"Japan":203,"Singapore":47,"Thailand":32,"Korea":28,"Malaysia":18,\
            "Germany":16,"Vietnam":15,"Australia":15,"France":11,"United Kingdom":8,"Canada":7,\
            "Philippines":3,"India":3,"Italy":3,"Russia":2,"Spain":2,"Nepal":1,\
            "Cambodia":1,'Finland':1,'Sweden':1,'Belgium':1}
contry=list(contry_set.keys())
valueC=list(contry_set.values())
city=list(city_set.keys())
city_v=list(city_set.values())
province=list(province_set.keys())
value=list(province_set.values())
starttime=datetime.datetime(2020,1,23)  #数据起始时间
endtime=datetime.datetime(2020,2,8)   #数据终止时间
interval=datetime.timedelta(days=1)  #时间间隔
dates=mpl.dates.drange(starttime,endtime,interval)
def fun(x,a,u,sig):
    return a*np.exp(-(x-u)**2/(2*sig**2))/(sig*math.sqrt(2*math.pi))  #定义高斯函数
x=np.arange(1,17,1)
y=np.array(data['numbers'])
ymean=np.mean(y)
y_mean=np.zeros((1,16))
for i in range(16):
    y_mean[:,i]=ymean
popt,pcov=curve_fit(fun,x,y)
a=popt[0]
u=popt[1]
sig=popt[2]
yvals=fun(x,a,u,sig)
R=1-np.sum((y-yvals)**2)/np.sum((y-y_mean[0])**2)   #拟合优度
print("高斯拟合的拟合优度是：",'%.4f'%R)   #拟合优度是0.9993(精确到小数点后四位)
print("预计峰值时期的累计确诊人数为：",int(round(fun(u,a,u,sig))))
print("预计峰值时间为1月23日起后"+str(int(round(u)))+"天左右")
fig=plt.figure()
ax1=fig.add_subplot(121)
ax1.plot_date(dates,data['numbers'],'-*',label='Cumulative number of confirmed')
for x,y in zip(dates,data['numbers']):
    plt.text(x,y,y)
ax1.plot_date(dates,yvals,'-*',label='Gaussian Fitting')
ax1.grid()
ax2=fig.add_subplot(122)
ax2.plot_date(dates,yvals,'-*',label='Gaussian Fitting')
for x,y in zip(dates,yvals):
    plt.text(x,int(y),int(round(y)))
ax2.grid()
fig.autofmt_xdate()
fig=plt.figure()
ax3=fig.add_subplot(111)
ax3.plot_date(dates,data['death'],'-*',label='Death Toll')
for x,y in zip(dates,data['death']):
    plt.text(x,y+8,y)
ax3.plot_date(dates,data['cure'],'-*',label='The Number Of Cure')
for x,y in zip(dates,data['cure']):
    plt.text(x,y-10,y)
ax3.grid()
fig.autofmt_xdate()
ax1.legend()
ax2.legend()
ax3.legend()
plt.show()
map = Map("疫情地图",'疫情地图', width=1200, height=500)
map.add("累计确诊人数", province, value, visual_range=[0,1000], maptype='china', is_visualmap=True,\
        visual_text_color='#333',is_map_symbol_show=True)
map.show_config()
map.render(path="疫情地图.html")
geo = Geo("全国疫情热力图", "全国疫情热力图",title_color="#fff",width=1000,height=600,\
          background_color='#404a59')
geo.add("累计确诊人数", city, city_v, visual_range=[1,100], maptype='china',type='heatmap',\
        visual_text_color="#fff",symbol_size=15, is_visualmap=True)
geo.render(path="全国疫情热力图.html")
mapW = Map("世界疫情地图",'世界疫情地图', width=1200, height=500)
mapW.add("累计确诊人数", contry, valueC, visual_range=[0,50], maptype='world', is_visualmap=True,\
        visual_text_color='#333',is_map_symbol_show=True)
mapW.show_config()
mapW.render(path="世界疫情地图.html")
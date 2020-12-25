#! /usr/bin/python3
#-*-coding:UTF-8-*-
# 青岛公交查询
# Author: 2997@YBZN

import requests,time
import configparser

#33路  隆德路②--南京路宁夏路①
rid = '33'
#departure_station =  '隆德路②'
#stop_station = '南京路宁夏路①'
departure_station = '北岭'
stop_station = '山东路南宁路'

#获取需要的线路公交站点信息
def get_bus_info(rid,departure_station,stop_station):
    url = 'http://bus.qingdaonews.com/m/detail.php?rid=' + rid + '&isjson=1'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 QIHU 360SE'
    }
    response=requests.get(url, headers=headers)
    response.encoding='utf-8'

    #Unicode转中文
    list_convert = (str(response.text).replace('u\'','\'')).replace('null', '\65e0')
    #转成列表
    station_info = eval(list_convert.encode('utf-8').decode("unicode-escape"))

    if station_info['stations']:
        rid = station_info['rid']
        segment_id = station_info['stations'][0]['segment_id']
        main_station = station_info['stations'][0]['station_name']
        all_station_num = len(station_info['stations'])
        
        if departure_station == main_station:
            for i in range(0,all_station_num-1):
                if stop_station == station_info['stations'][i]['station_name']:
                    station_id = station_info['stations'][i]['station_id']
                    break
            get_bus_detail(departure_station,stop_station,rid,segment_id,station_id)                
        else: 
            for i in range(0,all_station_num-1):
                if ('MO' == station_info['stations'][i]['station_direct']) and (stop_station == station_info['stations'][i]['station_name']):
                    station_id = station_info['stations'][i]['station_id']
                    break
            get_bus_detail(departure_station,stop_station,rid,segment_id,station_id)
    else:
        print(rid + '路公交暂无信息')

#获取需要的线路公交到站信息
def get_bus_detail(departure_station,stop_station,rid,segment_id,station_id):
    bus_details = ''
    url = 'http://bus.qingdaonews.com/m/detail_ajax.php?rid=' + rid + '&smid=' + segment_id + '&id=' + station_id + '&from=m'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 QIHU 360SE'
    }
    response=requests.get(url, headers=headers)
    response.encoding='utf-8'
    #Unicode转中文
    list_convert = str(response.text).replace('u\'','\'')
    #转成列表
    bus_detail = eval(list_convert.encode('utf-8').decode("unicode-escape"))
    print('公交查询', rid + '路', stop_station + '站')
    print('始发站',departure_station, '\n')
    if 'error' in bus_detail:
        print(bus_detail['error'])
    else:
        for item in bus_detail:
            for key,values in item.items():
                if key == 'car_num':
                    k1 = '车辆编号'
                    v1 = values
                elif key == 'current_station_name':
                    k2 = '当前站点'
                    v2 = values
                elif key == 'time_to_there':
                    k3 = '到站时间'
                    v3 = values
                elif key == 'time_to_there2':
                    k4 = '到站时间'
                    v4 = values
                elif key == 'station_count_remain':
                    k5 = '离 ' + stop_station + ' 还有'
                    v5 = values + ' 站'
                elif key == 'last_bus':
                    k6 = '末班车'
                elif key == 'stationseq':
                    k7 = '站点顺序'    
                #if (k != '末班车') and (k != '站点顺序'):
                    #print(k,v,' ',end='')
                    #bus_info += k + ' ' + v + ' '
            #bus_info += k1 + ' ' + v1 + ' ' + k2 + ' ' + v2 + ' ' +k3 + ' ' + v3 + ' ' +k4 + ' ' + v4 + ' ' + k5 + ' ' + v5 + ' '
            #bus_info += '\n'
            bus_details += rid + '路 ' + v1 + ' ' + v3 + '到达' + ' ' + v2 + ' ' + k5 + ' ' + v5 + ' ' 
            bus_details += '\n'
            #print()
    print(bus_details)

    #发送到群晖Chat
    #Synology_Chat(bus_details)

#到站信息发送到Synology_Chat,需要在Chat-整合 里传入的Webhook创建一个。
def Synology_Chat(bus_details):
    #curl -X POST  --data-urlencode 'payload={"text": "This is a test"}'  "http://192.168.10.254:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22a%22"
    chat_url = "http://192.168.10.254:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22a%22"
    payload = 'payload={"text": "' + bus_info + '"}'
    payload = payload.encode("utf-8").decode("latin1")
    r = requests.post(chat_url, payload).text

if __name__ == '__main__':
    get_bus_info(rid, departure_station, stop_station) 
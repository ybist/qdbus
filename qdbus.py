#! /usr/bin/python3
#-*-coding:UTF-8-*-
# 青岛公交查询
# Author: 2997

import requests,time

#33路  隆德路②--南京路宁夏路①
bus_num1 = '33'
#begin_station1 =  '隆德路②'
#wait_station1 = '南京路宁夏路①'
begin_station1 = '北岭'
wait_station1 = '山东路南宁路'
'''
#301路 高邮湖路  四川路滋阳路② - 万里江茶园
bus_num1 = '301'
#begin_station1 =  "四川路滋阳路②"
begin_station1 = '万里江茶园'
wait_station1 = '高邮湖路'

#223路 高邮湖路  东平路-刘家下庄
bus_num2 = '223'
#begin_station2 =  "刘家下庄"
begin_station2 = '东平路②'
wait_station2 = '高邮湖路'
'''
#获取需要的线路公交站点信息
def get_bus_info(bus_num,begin_station,wait_station):
    url = 'http://bus.qingdaonews.com/m/detail.php?rid=' + bus_num + '&isjson=1'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 QIHU 360SE'
    }
    response=requests.get(url, headers=headers)
    response.encoding='utf-8'
    time.sleep(2)
    #Unicode转中文
    list_right = (str(response.text).replace('u\'','\'')).replace('null', '\65e0')
    #转成列表
    station_info = eval(list_right.encode('utf-8').decode("unicode-escape"))
    
    if station_info['stations']:
        rid = station_info['rid']
        segment_id = station_info['stations'][0]['segment_id']
        main_station = station_info['stations'][0]['station_name']
        all_station_num = len(station_info['stations'])
        
        if begin_station == main_station:
            for i in range(0,all_station_num-1):
                if wait_station == station_info['stations'][i]['station_name']:
                    station_id = station_info['stations'][i]['station_id']
                    break
            get_bus_detail(begin_station,wait_station,rid,segment_id,station_id)                
        else: 
            for i in range(0,all_station_num-1):
                if ('MO' == station_info['stations'][i]['station_direct']) and (wait_station == station_info['stations'][i]['station_name']):
                    station_id = station_info['stations'][i]['station_id']
                    break
            get_bus_detail(begin_station,wait_station,rid,segment_id,station_id)
        #print(station_info)
        ''' 
        print('rid',rid)
        print('segment_id',segment_id)
        print('始发站', begin_station)
        print('等待站', wait_station)
        print('等待站ID', station_id)
        print('rid',rid)
        print('总共',all_station_num,'站')
        '''       
    else:
        print(bus_num + '路公交暂无信息')

#获取需要的线路公交到站信息
def get_bus_detail(begin_station,wait_station,rid,segment_id,station_id):
    bus_info = ''
    url = 'http://bus.qingdaonews.com/m/detail_ajax.php?rid=' + rid + '&smid=' + segment_id + '&id=' + station_id + '&from=m'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 QIHU 360SE'
    }
    response=requests.get(url, headers=headers)
    response.encoding='utf-8'
    time.sleep(2)
    #Unicode转中文
    list_right = str(response.text).replace('u\'','\'')
    #转成列表
    bus_detail = eval(list_right.encode('utf-8').decode("unicode-escape"))
  
    print('公交查询', rid + '路', wait_station + '站')
    print('始发站',begin_station, '\n')
    if 'error' in bus_detail:
        print(bus_detail['error'])
    else:
        for item in bus_detail:
            for k,v in item.items():
                if k == 'car_num':
                    k = '车辆编号'
                elif k == 'current_station_name':
                    k = '当前站点'
                elif k== 'time_to_there':
                    k = '到站时间'
                elif k== 'time_to_there2':
                    k = '到站时间'
                elif k== 'station_count_remain':
                    k = '离' + wait_station
                    v = v + ' 站'
                elif k== 'last_bus':
                    k = '末班车'
                elif k== 'stationseq':
                    k = '站点顺序'    
                if (k != '末班车') and (k != '站点顺序'):
                    #print(k,v,' ',end='')
                    bus_info += k + ' ' + v + ' '
            bus_info += '\n'
            #print()
    print(bus_info)

    #发送到群晖Chat
    Synology_Chat(bus_info)

#到站信息发送到Synology_Chat,需要在Chat-整合 里传入的Webhook创建一个。
def Synology_Chat(bus_info):
    #curl -X POST  --data-urlencode 'payload={"text": "This is a test"}'  "http://192.168.10.254:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22a%22"
    chat_url = "http://192.168.10.254:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=incoming&version=2&token=%22a%22"
    #payload = 'payload={"text": "This is a test"}'
    #payload = 'payload={"text": "这是一个测试"}'
    payload = 'payload={"text": "' + bus_info + '"}'
    payload = payload.encode("utf-8").decode("latin1")
    r = requests.post(chat_url, payload).text

if __name__ == '__main__':
    get_bus_info(bus_num1, begin_station1, wait_station1)
    #get_bus_info(bus_num2, begin_station2, wait_station2) 
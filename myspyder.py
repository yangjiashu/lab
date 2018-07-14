# coding:utf-8
from selenium import webdriver
import csv
import json
import sys
import time
import pandas as pd
import random
from selenium.webdriver.common.action_chains import ActionChains
from imp import reload
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
reload(sys)

yuanzu1 = (
    "BJS", "SHA", "CAN", "SZX", "CTU", "HGH", "WUH", "SIA", "CKG", "TAO", "CSX", "NKG", "XMN", "KMG", "DLC", "TSN",
    "CGO",
    "SYX", "TNA", "FOC")
yuanzu = (
    "SHA", "CAN", "SZX", "CTU", "HGH", "WUH", "SIA", "CKG", "TAO", "CSX", "NKG", "XMN", "KMG", "DLC", "TSN", "CGO",
    "SYX",
    "TNA", "FOC", "URC", "HAK", "HRB", "KWE", "SHE", "NNG", "LHW", "TYN", "CGQ", "WNZ", "HET", "KHN", "NGB", "HFE",
    "SJW",
    "LJG", "KWL", "INC", "ZUH", "WUX", "YNT", "XNN", "JHG", "SWA", "JJN", "LXA", "MIG")
cityCode = {'CKG': '重庆', 'LIA': '梁平', 'NAO': '南充', 'MIG': '绵阳', 'SIA': '西安', 'GHN': '广汉', 'NNG': '南宁', 'HSN': '丹山',
            'KHV': '伯力', 'LYA': '洛阳', 'KHN': '南昌', 'TAO': '青岛', 'HKG': '香港', 'TPE': '台北', 'HAK': '海口', 'CHG': '朝阳',
            'JIL': '吉林', 'KNC': '吉安', 'LHW': '兰州', 'WNZ': '温州', 'JIU': '九江', 'TYN': '太原', 'WUX': '无锡', 'LXA': '拉萨',
            'WUH': '武汉', 'UYN': '榆林', 'TSN': '天津', 'NGB': '宁波', 'YBP': '宜宾', 'AKA': '安康', 'MFM': '澳门', 'SZX': '深圳',
            'JUZ': '衢州', 'SHS': '沙市', 'ENH': '恩施', 'LJG': '丽江', 'SHA': '上海', 'CSX': '长沙', 'FOC': '福州', 'ENY': '延安',
            'DLX': '大连', 'DDG': '丹东', 'CZX': '常州', 'SYX': '三亚', 'TEN': '铜仁', 'LZH': '柳州', 'INC': '银川', 'KMG': '昆明',
            'CTU': '成都', 'LUZ': '庐山', 'XUZ': '徐州', 'PEK': '北京', 'HNY': '衡阳', 'ZUH': '珠海', 'HFE': '合肥', 'XNN': '西宁',
            'CGO': '郑州', 'XFN': '襄樊', 'CGD': '常德', 'PVG': '浦东', 'CGQ': '长春', 'SEL': '汉城', 'XMN': '厦门', 'NNY': '南阳',
            'YIH': '宜昌', 'HEK': '黑河', 'LYI': '临沂', 'JJN': '晋江', 'NTG': '南通', 'BAV': '包头', 'CIF': '赤峰', 'YNJ': '延吉',
            'SWA': '汕头', 'HZG': '汉中', 'HYN': '黄岩', 'ZHA': '湛江', 'SHE': '沈阳', 'XIC': '西昌', 'CAN': '广州', 'CIU': '长治',
            'YNT': '烟台', 'KOW': '赣州', 'TXN': '黄山', 'KWE': '贵阳', 'KWL': '桂林', 'DAT': '大同', 'AQG': '安庆', 'GYS': '广元',
            'DAX': '达县', 'TNA': '济南', 'HGH': '杭州', 'WXN': '万县', 'NKG': '南京', 'BHY': '北海'}
addDays = 8
checkIfR = 0
BigMonth = [1, 3, 5, 7, 8, 10]
SmallMonth = [4, 6, 9, 11]
CITY1 = ""
CITY2 = ""
DOUBLECITY = ""
def getPresentTime():
    year = int(time.strftime('%Y', time.localtime(time.time())))
    month = int(time.strftime('%m', time.localtime(time.time())))
    day = int(time.strftime('%d', time.localtime(time.time())))
    monthStr = ''
    dayStr = ''

    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                checkIfR = 1
            else:
                checkIfR = 0
        else:
            checkIfR = 1
    else:
        checkIfR = 0

    day = day + addDays

    if month == 2 and checkIfR == 1 and day > 29:
        month = 3
        day = day - 29

    if month == 2 and checkIfR == 0 and day > 28:
        month = 3
        day = day - 28

    if month in SmallMonth and day > 30:
        month = month + 1
        day = day - 30

    if month in BigMonth and day > 31:
        month = month + 1
        day = day - 31

    if month == 12 and day > 31:
        month = 1
        day = day - 31

    if month < 10:
        monthStr = '0' + str(month)
    else:
        monthStr = str(month)

    if day < 10:
        dayStr = '0' + str(day)
    else:
        dayStr = str(day)

    return str(year) + '-' + monthStr + '-' + dayStr


def search_xiecheng(browser,url,fout):
    #initialize
    try:
        browser.get(url)
        wait = WebDriverWait(browser,5)
        #print('successful!')
    except Exception as e:
        print(e)
    
    time.sleep(1)
#    try:
#        string = wait.until(EC.presence_of_element_located((By.ID,'J_flight_num')))
#        num = int(re.findall('\d+',string)[0]) + 1
#        print(string)
#        print(string2)
#    except:
    try:
        string = browser.find_element_by_css_selector('.flight-num').text
       # string = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'flight-num'))).text
        num = int(re.findall('\d+',string)[0]) + 1
    except:
        return
            
    for i in range(0, 5):
        js = "var q=document.documentElement.scrollTop=10000"
        browser.execute_script(js)
        time.sleep(0.2)
    
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.search_box_tag:first-child')))
    except:
        pass
    
    print(str(num) + '条航班信息')
#    iterate to get data
    for i in range(1,num):
#        try:
#            wait.until(EC.presence_of_all_elements_located((By.ID,'J_flightlist2')))
#        except:
#            
    #        try:
    #            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search_box_tag:nth-child(' + str(i) + ')')))
    #        except:
    #            pass
        
        field=['company','number','model','leaveairport','leavetime','arriveairport','arrivetime',\
               'way','staycity','staytime','share','price','discount']
        data = {} #store the data we need
        
        #company
        try:
            company1 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:first-child span strong').text
            company2 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:last-child span strong').text
            company = company1 + ' ' + company2
            data['company'] = company
        except:
            try:
                company1 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:first-child strong').text
                company2 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:last-child strong').text
                company = company1 + ' ' + company2
                data['company'] = company
            except:
                try:
                    data['company'] = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo .J_flight_no span strong').text
                    data['way'] = '直达'
                except:
                    try:
                        data['company'] = browser.find_element_by_css_selector(
                                '.search_box_tag:nth-child(' + str(i) + ') .logo .J_flight_no strong').text
                        data['way'] = 1
                    except:
                        data['company'] = 'unknown'
                        data['way'] = 'unknown'
                    pass
                pass
            pass
        pass
        if i < num / 5:
            time.sleep(0.1)
        #number
        try:
            number1 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:first-child span span').text
            number2 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:last-child span span').text
            number = number1 + ' ' + number2
            data['number'] = number
        except:
            try:
                number1 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:first-child span').text
                number2 = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo-item:last-child span').text
                number = number1 + ' ' + number2
                data['number'] = number
            except:
                try:
                    data['number'] = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) + ') .logo .J_flight_no span span').text
                except:
                    try:
                        data['number'] = browser.find_element_by_css_selector(
                                '.search_box_tag:nth-child(' + str(i) + ') .logo .J_flight_no span').text
                    except:
                        data['number'] = 'unknown'
                        pass
                    pass
                pass
            pass
        pass

        #way
        try:
            way = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) +') .transfer').text
            data['way'] = 3
            data['staycity'] = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) +') .stay-city span').text
            data['staytime'] = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) +') .stay-time').text
        except:
            try:
                way = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) +') .stopover').text
                data['way'] = 2
                data['staycity'] = browser.find_element_by_css_selector(
                        '.search_box_tag:nth-child(' + str(i) +') .stopover .low_text').text
                data['staytime'] = 'unknown'
            except:
                data['staycity'] = 'unknown'
                data['staytime'] = 'unknown'
                
        #share
        try:
            share = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) +') .shared_flight').text
            data['share'] = share
        except:
            data['share'] = 'noshare'
            pass
        

        #model
        try:
            model = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .logo .low_text span').text
            data['model'] = model
        except:
            try:
                model = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .logo .special_text').text
                data['model'] = model
            except:
                pass
            
        if i < num / 5:
            time.sleep(0.1) 
        #leavetime
        try:
            leavetime = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .right .time').text
            data['leavetime'] = leavetime
        except Exception as e:
            data['leavetime'] = 'unknown'
        
        #leaveairport
        try:
            leaveairport = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .right > div:nth-child(2)').text
            data['leaveairport'] = leaveairport
        except Exception as e:
            data['leaveairport'] = 'unknown'
        
        #arrivetime
        try:
            arrivetime = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .left .time').text
            data['arrivetime'] = arrivetime
        except Exception as e:
            data['arrivetime'] = 'unknown'
            
        #arriveairport
        try:
            arriveairport = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .left > div:nth-child(2)').text
            data['arriveairport'] = arriveairport
        except Exception as e:
            data['arriveairport'] = 'unknown'
       
        #price
        try:
            price = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .price .base_price02').text
            data['price'] = price
        except Exception as e:
            data['price'] = 'unknown'
            
        #discount
        try:
            discount = browser.find_element_by_css_selector(
                    '.search_box_tag:nth-child(' + str(i) + ') .price .low_text').text
            data['discount'] = discount
        except Exception as e:
            data['discount'] = 'unknown'
            
        #output
        writer = csv.DictWriter(fout,fieldnames=field)
        if not (data['company']=='unknown' and data['price'] == 'unknown' and data['leavetime']=='unknown'):
            writer.writerow(data)
if __name__ == '__main__':                  
    #initial
    chrome_options = webdriver.ChromeOptions()                                          
    chrome_options.add_argument('--proxy-server=http://183.32.88.182:808')
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get('https://accounts.ctrip.com/member/login.aspx?')
    time.sleep(1)
    try:
        browser.find_element_by_css_selector('#txtUserName').send_keys('18474699744')
    except:
        try:
            browser.find_element_by_css_selector('#nloginname').send_keys('18474699744')
        except:
            pass

    try:
        browser.find_element_by_css_selector('#npwd').send_keys('aa123456')
    except:
        try:
            browser.find_element_by_css_selector('#npwd').send_keys('aa123456')
        except:
            pass

    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.ID,'nsubmit'))).click()

    #get target date
    targetDateStr = getPresentTime()
    
    #decide position
    f_couple_city = open('./couple_city_sample.txt','r')
    Usetime = targetDateStr + time.strftime('-%Y%m%d-%Hh', time.localtime(time.time()))
    count = 1
    with open(Usetime+'.csv','w',encoding='utf-8') as fout:
        for line in f_couple_city.readlines():
            line = line.strip().split(',')
            print(str(line) +'  ' + str(count))
            count += 1
            start = line[0]
            end = line[1]
            url = 'http://flights.ctrip.com/booking/{start}-{end}-day-1.html?DDate1={date}'.format(\
                                                start=start,end=end,date=targetDateStr)
            #print(targetDateStr)
            search_xiecheng(browser,url,fout)
            #print('successful!')
    f_couple_city.close()
    browser.close()
    
    
    
    
    
    
    
    
    
    
    
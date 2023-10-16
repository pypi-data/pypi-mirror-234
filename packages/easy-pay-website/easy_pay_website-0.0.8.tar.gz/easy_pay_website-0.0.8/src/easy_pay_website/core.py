import requests
import re
import os
import time
from bs4 import BeautifulSoup
import ddddocr
import datetime
import pytz

def login(url : str  , username : str , password : str ,quary_key : str | int, query_value : str | int ) -> None:
    
    session = requests.session()
    timestamp = int(time.time())

    try:
        # code that may raise an error
        response = session.get(url+"/manage.php?"+quary_key+"="+query_value)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
        return False
    else:
        # logger.info(f"login response: {response.text}")
        cookiesAfter = response.cookies
        c = cookiesAfter.get_dict()
        cookiesPHPSESSID = c["PHPSESSID"]
        print(f"1 . get PHPSESSID: {cookiesPHPSESSID}")

    cookiesLogin = {
            'QINGZHIFU_PATH': 'qingzhifu',
            'PHPSESSID': cookiesPHPSESSID
        }


    try:
        # code that may raise an error
        # logger.info(f"2 . get number , url :{URL}/manage.php?{KEY}={VALUE}")
        response = session.get(url+"/manage.php?"+quary_key+"="+query_value, cookies=cookiesLogin)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
        return False
    else:
        # logger.info(f"login response: {response.text}")
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', {'method': 'post'})
        action_value = form['action']
        match = re.search(r'/(\d+)\.html$', action_value)

        if match:
            number = match.group(1)
            print(f"3 . login number: {number}")
        else:
            print("Number not found")
    
    urlVerify = url + "/Manage/Index/verify.html"
    
    
    try:
        # code that may raise an error
        print(f"4 . capcha url: {urlVerify}")
        response = session.get(urlVerify, cookies=cookiesLogin)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
        return False
    else:
        # code to execute if there is no error
        with open(f"captcha_{str(timestamp)}.png", "wb") as file:
            # Write the image data to the file
            file.write(response.content)

        # cookiesAfter = response.cookies
        # c = cookiesAfter.get_dict()
        # cookiesPHPSESSID = c["PHPSESSID"]

        # # read captcha
        ocr = ddddocr.DdddOcr()
        with open(f"captcha_{str(timestamp)}.png", 'rb') as f:
            image = f.read()
        
        # delete the f"captcha_{str(timestamp)}.png"
        if os.path.exists(f"captcha_{str(timestamp)}.png"):
            os.remove(f"captcha_{str(timestamp)}.png")
        code = ocr.classification(image)
        print(f"5 . capcha code: {code}")
        print(f"login code: {code}")
        
        if len(code) != 4:
            print(f"5 . capcha code error: {code}")
            return False
        
        data = {
            "username": username,
            "password": password,
            "yzm": code
        }

        urlLogin = url + "/Manage/Index/login/" + number + ".html"
        

        try:
            # code that may raise an error
            print(f"6 . login url: {urlLogin} , data: {data}")
            responseLogin = session.post(urlLogin, data=data, cookies=cookiesLogin)
        except Exception as e:
            # code to handle the error
            print(f"An error occurred: {e.args}")
            return False
        else:
            # check responseLogin.cookies exist or not , if not , return
            if responseLogin.cookies:
                print(f"6 . login response: True , cookies : {responseLogin.cookies}")
                cookiesR = responseLogin.cookies
                d = cookiesR.get_dict()
                fx_admin_user_CODE = d["fx_admin_user_CODE"]
                with open('fx_admin_user_CODE.txt', 'w') as file:
                                # Write some text to the file
                                file.write(fx_admin_user_CODE)
                with open('PHPSESSID.txt', 'w') as file:
                                # Write some text to the file
                                file.write(cookiesPHPSESSID)
                
                return {
                    "fx_admin_user_CODE": fx_admin_user_CODE,
                    "PHPSESSID": cookiesPHPSESSID
                }
            

            else:
                print(f"6 . login response: False")
                return False
            
def check_login_status(url : str):
    # start
    # check if fx_admin_user_CODE.txt exist or not 
    
    if os.path.exists('fx_admin_user_CODE.txt'):
        with open('fx_admin_user_CODE.txt', 'r') as file:
            fx_admin_user_CODE = file.read()
    else:
        print(f"login status: False")
        return False
    
    if os.path.exists('PHPSESSID.txt'):
        with open('PHPSESSID.txt', 'r') as file:
            cookiesPHPSESSID = file.read()
    else:
        print(f"login status: False")
        return False
    
    url = url + "/manage/main/index.html"
    cookies={
            "JSESSIONID": cookiesPHPSESSID,
            'QINGZHIFU_PATH': 'qingzhifu',
            'fx_admin_user_UNAME': 'admin',
            'menudd': '0',
            'fx_admin_user_UID': '1',
            'fx_admin_user_CODE': fx_admin_user_CODE
        }
    
    session = requests.session()

    try:
        # code that may raise an error
        response = session.get(url, cookies=cookies)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
        return False
    else:
        # if response.headers lens 12 returm true else return false
        if len(response.headers) == 12:
            print(f"login status: True")
            return True
        else:
            print(f"login status: False")
            return False


def get_trading_volume(url : str , userId : str, which_day : str):
    
    if which_day == "today":
        time_value = get_today_00_00_millisecond()
        date_string = str(get_today_date())
    
    elif which_day == "yesterday":
        time_value = get_yesterday_00_00_millisecond()
        date_string = str(get_yesterday_date())
    else:
        return False
    

    session = requests.session()
    with open('fx_admin_user_CODE.txt', 'r') as file:
        fx_admin_user_CODE = file.read()
    with open('PHPSESSID.txt', 'r') as file:
        cookiesPHPSESSID = file.read()

    cookies={
            "JSESSIONID": cookiesPHPSESSID,
            'QINGZHIFU_PATH': 'qingzhifu',
            'fx_admin_user_UNAME': 'admin',
            'menudd': '0',
            'fx_admin_user_UID': '1',
            'fx_admin_user_CODE': fx_admin_user_CODE
        }
    try:
        # code that may raise an error
        response = session.get(url+"/manage/dingdan/dingdancheck.html?userid=" + userId + "&pzid=&jkstyle=&time=" + str(time_value)+"&money=&mypagenum", cookies=cookies)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
        return False
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('div', {'class': 'row tagtopdiv'})
        # fild all h4 tag
        h4_tags = form.find_all('h4')
        # print h4_tags value one by one , and append to the new list
        h4_values = []
        for h4_tag in h4_tags:
            h4_values.append(h4_tag.text)
        for i in range(len(h4_values)):
            h4_values[i] = h4_values[i].strip()
        h4_values[0] = h4_values[0][1:-2]
        h4_values[2] = h4_values[2][:-2]
        h4_values[6] = h4_values[6][1:-2]

        # find last order
        last_soup = soup.find('tbody')
        # print(f"last order: {last_soup}")
        # find all td
        last_soup_td_tags = last_soup.find_all('td')
        # print(f"last order td: {last_soup_td_tags}")
        # find frist tr fourest td
        try:
            print(last_soup_td_tags[3].text)
        except Exception as e:
            todays_last_order_no = None
        else:
            todays_last_order_no = last_soup_td_tags[3].text


        if float(h4_values[6].split()[0]) == 0:
            data_object = {
                h4_values[1]: float(h4_values[0].split()[0]),  
                h4_values[3]: int(h4_values[2].split()[0]),  
                h4_values[7]: float(h4_values[6].split()[0])  ,
                "last_order" : todays_last_order_no,
                "rate" : 0,
            }
        else:
            data_object = {
                h4_values[1]: float(h4_values[0].split()[0]),  
                h4_values[3]: int(h4_values[2].split()[0]),  
                h4_values[7]: float(h4_values[6].split()[0])  ,
                "last_order" : todays_last_order_no,
                "rate" : round(( 1 - float(h4_values[0].split()[0]) / float(h4_values[6].split()[0]) ) * 100 , 2 ),
            }
        # print(data_object)
        # return data_object

        if data_object['last_order'] == None:
            # data_object['balance'] = 0
            try:
                # code that may raise an error
                response = session.get(url+"/manage/user/index.html?userid="+userId, cookies=cookies)
            except Exception as e:
                # code to handle the error
                print(f"An error occurred: {e.args}")
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                balance_soup = soup.find('tbody')
                balance_soup_td_tags = balance_soup.find_all('td')
                try:
                    print(balance_soup_td_tags[6].text)
                except Exception as e:
                    current_balance = None
                else:
                    current_balance = balance_soup_td_tags[6].text
                
                    # handle string delete after 【
                    
                    index = current_balance.find("【")
                    if index != -1:
                            current_balance = float(current_balance[:index])
                    else:
                            current_balance = float(current_balance)
                    
                data_object['balance'] = current_balance
        else:
            try:
                # code that may raise an error
                response = session.get(url+"/manage/pay/moneylog.html?ordersn="+data_object['last_order'], cookies=cookies)
            except Exception as e:
                # code to handle the error
                print(f"An error occurred: {e.args}")
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                balance_soup = soup.find('tbody')
                balance_soup_td_tags = balance_soup.find_all('td')
                try:
                    print(balance_soup_td_tags[5].text)
                except Exception as e:
                    current_balance = None
                else:
                    # current_balance = float(balance_soup_td_tags[5].text)
                    if userId == balance_soup_td_tags[2].text:
                        current_balance = float(balance_soup_td_tags[5].text)
                    elif userId == balance_soup_td_tags[10].text:
                        current_balance = float(balance_soup_td_tags[13].text)
                    else:
                        current_balance = None
                data_object['balance'] = current_balance
        
        print(data_object)
    try:
        print(date_string)
        # code that may raise an error
        response = session.get(url+"/manage/pay/moneylog.html?userid="+userId+"&start="+date_string+" 00:00:00&end="+date_string+" 23:59:59&style=2", cookies=cookies)
    except Exception as e:
        # code to handle the error
        print(f"An error occurred: {e.args}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        withdraw_soup = soup.find('tbody')
        withdraw_soup_tr_tags = withdraw_soup.find_all('tr')
        print(f"withdraw_soup_tr_tags: {withdraw_soup_tr_tags}")
        print(f"len of withdraw_soup_tr_tags: {len(withdraw_soup_tr_tags)}")
        if len(withdraw_soup_tr_tags[0].text) == 6:
            data_object['withdraw'] = None
        else:
            # data_object['withdraw'] = float(withdraw_soup_tr_tags[0].text)
            # data_object['withdraw'] = 1
            withdraw_data = []
            for i in range(len(withdraw_soup_tr_tags)):
                # find all td
                withdraw_soup_td_tags = withdraw_soup_tr_tags[i].find_all('td')
                # use dictionary to store data
                withdraw_data.append({
                    'date': withdraw_soup_td_tags[7].text,
                    'amount': float(withdraw_soup_td_tags[4].text),
                })

            data_object['withdraw'] = withdraw_data
        
        print(data_object)
        return data_object

def get_today_date():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    today_date = now.date()
    return today_date

def get_yesterday_date():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    yesterday_date = (now - datetime.timedelta(days=1)).date()
    return yesterday_date

def get_now_time():
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    current_time = now.strftime("%H:%M")
    print(f"current_time: {current_time}")
    return current_time

def get_today_00_00_millisecond():
    timestamp = int(time.time()) 
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    latest_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_utc1600 = int(latest_time.timestamp() )
    if timestamp < today_utc1600:
        today_00_00_millisecond = today_utc1600 - 24 * 60 * 60 
    else:
        today_00_00_millisecond = today_utc1600
    return today_00_00_millisecond

def get_yesterday_00_00_millisecond():
    timestamp = int(time.time()) - 24 * 60 * 60
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    latest_time = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_utc1600 = int(latest_time.timestamp() )
    if timestamp < yesterday_utc1600:
        yesterday_00_00_millisecond = yesterday_utc1600 - 24 * 60 * 60 
    else:
        yesterday_00_00_millisecond = yesterday_utc1600
    # print(f"yesterday_00_00_millisecond: {yesterday_00_00_millisecond}")
    return yesterday_00_00_millisecond


import datetime
import io
import json
import os
import sys
import time
from time import sleep
import requests
from bs4 import BeautifulSoup
import lxml
import hashlib
from urllib.parse import urlencode
import mysql.connector
from mysql.connector import Error

# 需要一个当天日期
# 需要一个当天前10天日期
# 上海市10mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E4%25B8%258A%25E6%25B5%25B7%3A15640&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}

# 上海市20mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E4%25B8%258A%25E6%25B5%25B7%3A15640&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}

# 广州市10mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%25B9%25BF%25E5%25B7%259E%3A15589&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}

# 广州市20mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%25B9%25BF%25E5%25B7%259E%3A15589&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}

# 南京市10mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%258D%2597%25E4%25BA%25AC%3A15411&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}

# 南京市20mm造船板价格
# catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%258D%2597%25E4%25BA%25AC%3A15411&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}

def connect_to_database(host_name, user_name, port, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            port=port,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")



if __name__ == '__main__':
    APPKEY = '47EE3F12CF0C443F8FD51EFDA73AC815'
    APPSEC = '3BA6477330684B19AA6AF4485497B5F2'
    PATH = '/zs/newprice/getBaiduChartMultiCity.ms'

    TODAY = datetime.date.today()
    START_DAY = TODAY - datetime.timedelta(days=5000)
    TODAY_str = str(TODAY)
    START_DAT_str = str(START_DAY)

    # print(START_DAT_str)
    # print(TODAY_str)
    print('正在获取 {} 当天数据...'.format(TODAY_str))
    now_time = int(time.time() * 1000)
    JSON_FILE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'mysteel-{}-{}.json'.format(TODAY_str, now_time))
    # print(now_time)
    new_path = 'path' + PATH + 'timestamp' + str(now_time) + 'version1.0.0' + APPSEC
    m = hashlib.md5()
    m.update(new_path.encode(encoding='utf-8'))
    # print(m.hexdigest())
    SIGN = m.hexdigest().upper()
    # print(SIGN)


    headers = {
        'Appkey': APPKEY,
        'Sign': SIGN,
        'Timestamp': str(now_time),
        'Version': '1.0.0'
    }

    url = 'https://index.mysteel.com/zs/newprice/getBaiduChartMultiCity.ms?'

    params_dict = {
        '上海市10mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E4%25B8%258A%25E6%25B5%25B7%3A15640&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}'.format(
            START_DAT_str, TODAY_str, now_time),
        # '上海市20mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E4%25B8%258A%25E6%25B5%25B7%3A15640&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}'.format(
        #     START_DAT_str, TODAY_str, now_time),
        # '广州市10mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%25B9%25BF%25E5%25B7%259E%3A15589&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}'.format(
        #     START_DAT_str, TODAY_str, now_time),
        # '广州市20mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%25B9%25BF%25E5%25B7%259E%3A15589&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}'.format(
        #     START_DAT_str, TODAY_str, now_time),
        # '南京市10mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%258D%2597%25E4%25BA%25AC%3A15411&spec=10mm_%3A__10mm&startTime={}&endTime={}&callback=json&v={}'.format(
        #     START_DAT_str, TODAY_str, now_time),
        # '南京市20mm造船板价格': 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E5%258D%2597%25E4%25BA%25AC%3A15411&spec=20mm_%3A__20mm&startTime={}&endTime={}&callback=json&v={}'.format(
        #     START_DAT_str, TODAY_str, now_time),
    }

    param_to_sql_key_dict = {
        '上海市10mm造船板价格': 'SH_SHIP_PLATE_10MM',
        '上海市20mm造船板价格': 'SH_SHIP_PLATE_20MM',
        '广州市10mm造船板价格': 'GZ_SHIP_PLATE_10MM',
        '广州市20mm造船板价格': 'GZ_SHIP_PLATE_20MM',
        '南京市10mm造船板价格': 'NJ_SHIP_PLATE_10MM',
        '南京市20mm造船板价格': 'NJ_SHIP_PLATE_20MM',
    }

    result_dict = {}

    connection = connect_to_database(
        host_name='sh-cynosdbmysql-grp-pvsmsm7y.sql.tencentcdb.com',
        user_name='root',
        port=23620,
        user_password='Cyl@31415',
        db_name='Time_Series'
    )

    for params_dict_item in params_dict.keys():
        result_key = params_dict_item
        result_params = params_dict[params_dict_item]

        # params = 'catalog=%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF_%3A_%25E9%2580%25A0%25E8%2588%25B9%25E6%259D%25BF&city=%25E4%25B8%258A%25E6%25B5%25B7%3A15640&spec=10mm_%3A__10mm&startTime=2023-11-20&endTime=2023-11-30&callback=json&v={}'.format(now_time)
        response = requests.get(url=url + result_params, headers=headers)
        # print(response.text)
        content_json = response.json()
        data_price_map = content_json['data'][0]['dateValueMap']
        # print(data_price_map)
        column = param_to_sql_key_dict[result_key]
        for dv in data_price_map:
            d = dv['date']
            v = dv['value']
            sql_query = f"""
                                INSERT INTO daily_data (date, {column})
                                VALUES ('{d}', {v})
                                ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                                """
            print(sql_query)
            execute_query(connection, sql_query)



    # with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f_first:
    #     json.dump({'mysteel': result_dict}, f_first, ensure_ascii=False, indent=2)

    print('爬取完成...')

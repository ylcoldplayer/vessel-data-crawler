import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import pandas as pd
import warnings


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)
    return wrapper


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


def datetime_to_string(datetime_value):
    return datetime_value.strftime('%Y-%m-%d')


def execute_query(connection, sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()

    column_names = [column[0] for column in cursor.description]

    return column_names, result


sheet_to_table_name_map = {
    '上海10mm船板价格': '上海市10mm造船板价格',
    '上海20mm船板价格': '上海市20mm造船板价格',
    '广州10mm船板价格': '广州市10mm造船板价格',
    '广州20mm船板价格': '广州市20mm造船板价格',
    '南京20mm船板价格': '南京市20mm造船板价格',
    '南京10mm船板价格': '南京市10mm造船板价格',
    '1M SOFR': 'CME_TERM_SOFR_1_MON',
    '3M Term SOFR': 'CME_TERM_SOFR_3_MON',
    '6M Term SOFR': 'CME_TERM_SOFR_6_MON',
    '12M Term SOFR': 'CME_TERM_SOFR_1_Y',
    'bci': 'bci',
    'bpi': 'bpi',
    'bsi': 'bsi',
    'BDI\n波罗的海干散货运价指数': 'BDI_波罗的海干散货运价指数',
    'bhsi': 'bhsi',
    'BDTI\n波罗的海原油运价指数': 'BDTI_波罗的海原油运价指数',
    'BCTI\n波罗的海成品油运价指数': 'BCTI_波罗的海成品油运价指数',
    'blpg': 'blpg',
    'blng': 'blng',
    'CCFI\n中国出口集装箱运价指数': 'CCFI_中国出口集装箱运价指数',
    'SCFI上海出口集装箱运价指数': 'SCFI上海出口集装箱运价指数',
    '中国沿海散货船舶日租金指数(CDI)': 'CDI_中国沿海散货船舶日租金指数',
    '中国进口原油运价指数': '中国进口原油运价指数',
    '新华-泛亚内贸集装箱船运价指数': '新华_泛亚内贸集装箱船运价指数',
    'USDIND\n美元指数': 'USDIND_美元指数',
    'USDCNH\n美元/人民币离岸价格': 'USDCHN_美元人民币离岸价格',
    'Gold Price(LME) -USD\n黄金价格 -美元': 'Gold_Price_LME_USD',
    ' Oil Price (WTI) -USD\n原油价格 -美元': 'Oil_Price_WTI_USD',
    ' Gold to Oil Ratio\n金油比': 'Gold_To_Oil_Ratio',
    'IFO 380cst Bunker Prices (3.5% Sulphur), Singapore $/Tonne': 'IFO_380cst_Bunker_Prices',
    'VLSFO Bunker Prices (0.5% Sulphur), Singapore $/Tonne': 'VLSFO_Bunker_Prices',
    'Spread between high and low sulphur': 'Spread_between_high_and_low_sulphur',
    'MEOH': 'MEOH',
    'MEoH-VLSFOe': 'MEoH_VLSFOe',
    'MEoH-MGOe': 'MEoH_MGOe',
    '路透CRB商品指数': '路透CRB商品指数',
    '南华商品指数': '南华商品指数',
    'Iron Ore 62% Fe, CFR China': 'iron_ore',
    '隔夜Shibor': '隔夜Shibor',
    '1M SHIBOR': '1M_SHIBOR',
    '3M SHIBOR': '3M_SHIBOR',
    '6M SHIBOR': '6M_SHIBOR',
    '12个月shibor': '1Y_SHIBOR',
    'LPR1Y': 'LPR1Y',
    'LPR5Y': 'LPR5Y',
    '中国1年期国债': '中国1年期国债',
    '中国10年期国债/': '中国10年期国债',
    '美国1年期国债/': '美国1年期国债',
    '美国10年期国债': '美国10年期国债',
    'CEA -RMB/t\n中国碳排放配额价格-元/吨': 'CEA_RMB',
    'TJCE-RMB/t天津碳排放配额价格': 'TJCE_RMB',
    'EUA -EUR/t\n欧洲碳排放配额价格-欧元/吨': 'EUA_EUR',
    'KranShare-全球碳ETF（KRBN）': 'KRBN',
    '东方财富航运港口指数': '东方财富航运港口指数',
    'Dow Jones U.S. Marine Transportation Index': 'DJ_US_MARINE_TRANS_INDEX',
    'MSCI world transportation index': 'MSCI_world_transportation_index',
    'Euribor 1month': 'Euribor_1m',
    'Euribor 3m': 'Euribor_3m',
    'Euribor 6m': 'Euribor_6m',
    'Euribor 12m': 'Euribor_1y',
    'SCFIS欧线主连 ECM': 'SCFIS欧线主连_ECM',
    'SCFIS欧线次主连 ECS': 'SCFIS欧线次主连_ECS',
    '1Y SOFR swap rate ': '1Y_SOFR_swap_rate',
    '2Y SOFR swap rate ': '2Y_SOFR_swap_rate',
    '3Y  SOFR swap rate ': '3Y_SOFR_swap_rate',
    '5Y  SOFR swap rate ': '5Y_SOFR_swap_rate',
    '7Y  SOFR swap rate ': '7Y_SOFR_swap_rate',
    '10Y  SOFR swap rate ': '10Y_SOFR_swap_rate',
    '15Y  SOFR swap rate ': '15Y_SOFR_swap_rate',
    '30Y  SOFR swap rate ': '30Y_SOFR_swap_rate'
}


@suppress_warnings
def read_excel_file_update_values(column_and_value_dict, old_file='data-2024-01-16.xlsx', today='2024-01-20'):
    # today = datetime_to_string(datetime.today())
    # yesterday = datetime_to_string(datetime.today() - timedelta(days=2))

    new_file = today + '.xlsx'

    df = pd.read_excel(old_file, engine='openpyxl', sheet_name='日报', index_col=None).drop('Unnamed: 0', axis=1)
    print("old file: " + old_file)
    print(df)
    if today not in df.columns:
        df.insert(1, today, None)
    print(df)

    for k, v in sheet_to_table_name_map.items():
        value = column_and_value_dict[v]
        if value is not None:
            print(k)
            df.loc[df['metric'] == k, today] = value

    file_name = "data-" + new_file
    sheet_1 = pd.read_excel(old_file, sheet_name='Sheet1', engine='openpyxl')
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='日报')
        sheet_1.to_excel(writer, sheet_name='Sheet1')
    # df.to_excel(new_file, engine='openpyxl')


def consolidate_two_sheets():
    pass

if __name__ == '__main__':
    # df = pd.read_excel('../data/data-2024-01-16.xlsx',skiprows=2, sheet_name='日报')
    # df.rename(columns={'Unnamed: 0': 'metric'}, inplace=True)
    #
    # df.to_excel('2024-01-16.xlsx', engine='openpyxl', index=False)
    #
    # print(df)



    # sheet_1 = pd.read_excel('../data/市场数据跟踪 二次调整颜色(1).xlsx', sheet_name='Sheet1', engine='openpyxl')
    # print(sheet_1)
    # df = pd.read_excel('2024-01-16.xlsx', engine='openpyxl')
    # # df.drop(df.columns[0], axis=1, inplace=True)
    # file_name = "data-2024-01-16.xlsx"
    # with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    #     df.to_excel(writer, sheet_name='日报')
    #     sheet_1.to_excel(writer, sheet_name='Sheet1')






    today = datetime_to_string(datetime.today())
    now = datetime.today()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    connection = connect_to_database(
        host_name='sh-cynosdbmysql-grp-pvsmsm7y.sql.tencentcdb.com',
        user_name='root',
        port=23620,
        user_password='Cyl@31415',
        db_name='Time_Series'
    )

    sql_query = f"select * from Time_Series.daily_data where date = '{today}' limit 10"

    print(sql_query)
    result = execute_query(connection, sql_query)

    column_names = result[0]
    values = result[1][0]

    k_v_dict = {}
    n = len(column_names)
    for i in range(n):
        k_v_dict[column_names[i]] = values[i]
    yesterday = datetime_to_string(datetime.today() - timedelta(days=1))
    old_file = 'data-' + yesterday + '.xlsx'
    # read_excel_file_update_values(k_v_dict, old_file=old_file, today=today)

    read_excel_file_update_values(k_v_dict)

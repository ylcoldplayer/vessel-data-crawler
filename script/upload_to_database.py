import mysql.connector
from mysql.connector import Error
from cme_util import get_cme_data
from script.config import Ship_BUNKER_dict, all_configs
from script.previous_data_util import read_shanghai_10mm, read_row_data
from script.scrape_ccfi import get_ccfi_data
from script.scrape_cdi import get_cdi_data
from script.scrape_cn_yield import get_cn_yield_data
from script.scrape_crb import get_crb_data
from script.scrape_ctfi import get_ctfi_data
from script.scrape_ecm import get_ecm_data
from script.scrape_ecs import get_ecs_data
from script.scrape_euribor import get_euribor_data
from script.scrape_gold_price import get_gold_price_data
from script.scrape_ifo import get_ifo_380_data
from script.scrape_iron_ore import get_iron_ore_data
from script.scrape_krbn import get_krbn_data
from script.scrape_lpr import get_lpr_data
from script.scrape_msci import get_msci_data
from script.scrape_nanhua import get_nanhua_data
from script.scrape_scfi import get_scfi_data
from script.scrape_shibors import get_shibor_data
from script.scrape_shipandbunker_web import get_data_from_config_dict
from script.scrape_us_yield import get_us_yield_data
from script.scrape_usd_cny import get_usd_cny_data
from script.scrape_usd_index import get_usd_index_data
from script.scrape_usd_jpy import get_usd_jpy_data
from script.scrape_vlsfo import get_vlsfo_data
from script.scrape_wti_oil import get_wti_oil_data
from script.script_sofr import get_sofr_data
from script.script_sofr_on import get_sofr_on_data
from script.steel_util import get_steel_data
from datetime import datetime


import functools
import time


def retry(attempts=3, delay=1):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            nonlocal attempts
            attempts_left = attempts
            while attempts_left > 1:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Function {func.__name__} failed with {e}, retrying...")
                    time.sleep(delay)  # wait for some time before retrying
                    attempts_left -= 1
            return func(*args, **kwargs)  # last attempt without catching exceptions
        return wrapper_retry
    return decorator_retry


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


@retry(attempts=3, delay=2)
def upload_cme_data():
    cme_data = get_cme_data()
    print(cme_data)
    date_str = cme_data[0]['timestamp'].split('T')[0]
    price_1_month = cme_data[0]['price']
    price_3_month = cme_data[1]['price']
    price_6_month = cme_data[2]['price']
    price_1_year = cme_data[3]['price']

    sql_insert_query = f"INSERT INTO Time_Series.daily_data (date, CME_TERM_SOFR_1_MON, CME_TERM_SOFR_3_MON, " \
                       f"CME_TERM_SOFR_6_MON, CME_TERM_SOFR_1_Y) VALUES ('{date_str}', {price_1_month}, " \
                       f" {price_3_month}, {price_6_month}, {price_1_year});"
    execute_query(connection, sql_insert_query)
    print(sql_insert_query)

@retry(attempts=3, delay=2)
def upload_steel_data():
    json_data = get_steel_data()
    print(json_data)

    # Preparing the SQL query
    today = datetime_to_string(datetime.today())
    columns = ', '.join(json_data.keys())
    values = ', '.join(['%s'] * len(json_data))
    update_parts = ', '.join([f"{k} = VALUES({k})" for k in json_data.keys()])
    print("update_parts: " + update_parts)
    sql_query = f"""
    INSERT INTO daily_data (date, {columns})
    VALUES ('{today}', {values})
    ON DUPLICATE KEY UPDATE {update_parts};
    """
    print(sql_query)
    execute_query(connection, sql_query % tuple(json_data.values()))


@retry(attempts=3, delay=2)
def upload_msci_data():
    msci_data = get_msci_data()
    date_from_scrape = msci_data['this_date']
    data_this_period = msci_data['this_period']
    sql_query = f"""
        INSERT INTO daily_data (date, MSCI_world_transportation_index)
        VALUES ('{date_from_scrape}', {data_this_period})
        ON DUPLICATE KEY UPDATE MSCI_world_transportation_index = VALUES(MSCI_world_transportation_index);
        """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ccfi_data():
    ccfi_data = get_ccfi_data()
    date_from_scrape = ccfi_data['this_date']
    data_this_period = ccfi_data['this_period']
    sql_query = f"""
        INSERT INTO daily_data (date, CCFI)
        VALUES ('{date_from_scrape}', {data_this_period})
        ON DUPLICATE KEY UPDATE CCFI = VALUES(CCFI);
        """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_scfi_data():
    ccfi_data = get_scfi_data()
    date_from_scrape = ccfi_data['this_date']
    data_this_period = ccfi_data['this_period']
    sql_query = f"""
            INSERT INTO daily_data (date, SCFI)
            VALUES ('{date_from_scrape}', {data_this_period})
            ON DUPLICATE KEY UPDATE SCFI = VALUES(SCFI);
            """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_cdi_data():
    cdi_data = get_cdi_data()
    date_from_scrape = cdi_data['this_date']
    data_this_period = cdi_data['this_period']
    sql_query = f"""
                INSERT INTO daily_data (date, CDI)
                VALUES ('{date_from_scrape}', {data_this_period})
                ON DUPLICATE KEY UPDATE CDI = VALUES(CDI);
                """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_usd_index_data():
    usd_index_data = get_usd_index_data()
    date_from_scrape = usd_index_data['this_date']
    data_this_period = usd_index_data['this_period']
    sql_query = f"""
                    INSERT INTO daily_data (date, USD_INDEX)
                    VALUES ('{date_from_scrape}', {data_this_period})
                    ON DUPLICATE KEY UPDATE USD_INDEX = VALUES(USD_INDEX);
                    """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_usd_cny_data():
    usd_cny_data = get_usd_cny_data()
    date_from_scrape = usd_cny_data['this_date']
    data_this_period = usd_cny_data['this_period']
    sql_query = f"""
                        INSERT INTO daily_data (date, USDCHN)
                        VALUES ('{date_from_scrape}', {data_this_period})
                        ON DUPLICATE KEY UPDATE USDCHN = VALUES(USDCHN);
                        """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_usd_jpy_data():
    usd_jpy_data = get_usd_jpy_data()
    date_from_scrape = usd_jpy_data['this_date']
    data_this_period = usd_jpy_data['this_period']
    sql_query = f"""
                           INSERT INTO daily_data (date, USDJPY)
                           VALUES ('{date_from_scrape}', {data_this_period})
                           ON DUPLICATE KEY UPDATE USDJPY = VALUES(USDJPY);
                           """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_gold_price_data():
    gold_price_data = get_gold_price_data()
    date_from_scrape = gold_price_data['this_date']
    data_this_period = gold_price_data['this_period']
    sql_query = f"""
                            INSERT INTO daily_data (date, Gold_Price_LME_USD)
                            VALUES ('{date_from_scrape}', {data_this_period})
                            ON DUPLICATE KEY UPDATE Gold_Price_LME_USD = VALUES(Gold_Price_LME_USD);
                            """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ecm_data():
    ecm_data = get_ecm_data()
    date_from_scrape = ecm_data['this_date']
    data_this_period = ecm_data['this_period']
    sql_query = f"""
                            INSERT INTO daily_data (date, SCFIS_EUR_ECM)
                            VALUES ('{date_from_scrape}', {data_this_period})
                            ON DUPLICATE KEY UPDATE SCFIS_EUR_ECM = VALUES(SCFIS_EUR_ECM);
                            """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ecs_data():
    ecs_data = get_ecs_data()
    date_from_scrape = ecs_data['this_date']
    data_this_period = ecs_data['this_period']
    sql_query = f"""
                            INSERT INTO daily_data (date, SCFIS_EUR_ECS)
                            VALUES ('{date_from_scrape}', {data_this_period})
                            ON DUPLICATE KEY UPDATE SCFIS_EUR_ECS = VALUES(SCFIS_EUR_ECS);
                            """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_crb_data():
    crb_data = get_crb_data()
    date_from_scrape = crb_data['this_date']
    data_this_period = crb_data['this_period']
    sql_query = f"""
                                INSERT INTO daily_data (date, CRB_COMMODITY_INDEX)
                                VALUES ('{date_from_scrape}', {data_this_period})
                                ON DUPLICATE KEY UPDATE CRB_COMMODITY_INDEX = VALUES(CRB_COMMODITY_INDEX);
                                """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_nanhua_data():
    nanhua_data = get_nanhua_data()
    date_from_scrape = nanhua_data['this_date']
    data_this_period = nanhua_data['this_period']
    sql_query = f"""
                                    INSERT INTO daily_data (date, NH_COMMODITY_INDEX)
                                    VALUES ('{date_from_scrape}', {data_this_period})
                                    ON DUPLICATE KEY UPDATE NH_COMMODITY_INDEX = VALUES(NH_COMMODITY_INDEX);
                                    """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_iron_ore_data():
    iron_ore_data = get_iron_ore_data()
    date_from_scrape = iron_ore_data['this_date']
    data_this_period = iron_ore_data['this_period']
    sql_query = f"""
                                        INSERT INTO daily_data (date, iron_ore)
                                        VALUES ('{date_from_scrape}', {data_this_period})
                                        ON DUPLICATE KEY UPDATE iron_ore = VALUES(iron_ore);
                                        """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_wti_oil_data():
    wti_oil_data = get_wti_oil_data()
    date_from_scrape = wti_oil_data['this_date']
    data_this_period = wti_oil_data['this_period']
    sql_query = f"""
                                            INSERT INTO daily_data (date, Oil_Price_WTI_USD)
                                            VALUES ('{date_from_scrape}', {data_this_period})
                                            ON DUPLICATE KEY UPDATE Oil_Price_WTI_USD = VALUES(Oil_Price_WTI_USD);
                                            """
    print(sql_query)
    execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_shibors_data():
    date, shibor_dict = get_shibor_data()
    if date is None or shibor_dict is None:
        print("Error: no shibor data found...")
        return

    columns = ['SHIBOR_ON', 'SHIBOR_1M', 'SHIBOR_3M', 'SHIBOR_6M','SHIBOR_1Y']
    for column in columns:
        if column not in shibor_dict:
            print(column + " data not found...")
            continue
        shibor_value = float(shibor_dict[column])/100.0
        sql_query = f"""
                    INSERT INTO daily_data (date, {column})
                    VALUES ('{date}', {shibor_value})
                    ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                    """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_lpr_data():
    date, lpr_dict = get_lpr_data()
    if date is None or lpr_dict is None:
        print("Error: no lpr data found...")
        return

    columns = ['LPR1Y', 'LPR5Y']
    for column in columns:
        if column not in lpr_dict:
            print(column + " data not found...")
            continue
        lpr_value = float(lpr_dict[column]) / 100.0
        sql_query = f"""
                        INSERT INTO daily_data (date, {column})
                        VALUES ('{date}', {lpr_value})
                        ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                        """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_us_yield_data():
    term_dict = {
        '1 Year': 'US_1Y_BOND_YIELD',
        '2 Year': 'US_2Y_BOND_YIELD',
        '3 Year': 'US_3Y_BOND_YIELD',
        '5 Year': 'US_5Y_BOND_YIELD',
        '7 Year': 'US_7Y_BOND_YIELD',
        '10 Year': 'US_10Y_BOND_YIELD',
        '30 Year': 'US_30Y_BOND_YIELD'
    }
    sofr_data = get_us_yield_data()
    for term, rates in sofr_data.items():
        for date, rate in rates:
            column = term_dict[term]
            sql_query = f"""
                            INSERT INTO daily_data (date, {column})
                            VALUES ('{date}', {rate})
                            ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                            """
            print(sql_query)
            execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_sofr_on_data():
    term_dict = {
        'SOFR': 'SOFR',
        '30-Day Average SOFR': 'SOFR_30_DAYS_AVG',
        '90-Day Average SOFR': 'SOFR_90_DAYS_AVG',
    }
    sofr_on_data = get_sofr_on_data()
    print(sofr_on_data)
    for term, rates in sofr_on_data.items():
        for date, rate in rates:
            if term not in term_dict:
                continue
            column = term_dict[term]
            sql_query = f"""
                        INSERT INTO daily_data (date, {column})
                        VALUES ('{date}', {rate})
                        ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                        """
            print(sql_query)
            execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_sofr_data():
    term_dict = {
        '1 Year': '1Y_SOFR_swap_rate',
        '2 Year': '2Y_SOFR_swap_rate',
        '3 Year': '3Y_SOFR_swap_rate',
        '5 Year': '5Y_SOFR_swap_rate',
        '7 Year': '7Y_SOFR_swap_rate',
        '10 Year': '10Y_SOFR_swap_rate',
        '15 Year': '15Y_SOFR_swap_rate',
        '30 Year': '30Y_SOFR_swap_rate'
    }
    sofr_data = get_sofr_data()
    for term, rates in sofr_data.items():
        for date, rate in rates:
            column = term_dict[term]
            sql_query = f"""
                        INSERT INTO daily_data (date, {column})
                        VALUES ('{date}', {rate})
                        ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                        """
            print(sql_query)
            execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_euribor_data():
    term_dict = {
        'Euribor 1 week': 'Euribor_1w',
        'Euribor 1 month': 'Euribor_1m',
        'Euribor 3 months': 'Euribor_3m',
        'Euribor 6 months': 'Euribor_6m',
        'Euribor 12 months': 'Euribor_1y',

    }
    date, term_rate_dict = get_euribor_data()
    for term, rate in term_rate_dict.items():
        column = term_dict[term]
        sql_query = f"""
                    INSERT INTO daily_data (date, {column})
                    VALUES ('{date}', {rate})
                    ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                    """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ifo_data():
    ifo_data = get_ifo_380_data()
    for date, price in ifo_data.items():
        sql_query = f"""
                            INSERT INTO daily_data (date, IFO_380cst_Bunker_Prices)
                            VALUES ('{date}', {price})
                            ON DUPLICATE KEY UPDATE IFO_380cst_Bunker_Prices = VALUES(IFO_380cst_Bunker_Prices);
                            """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_vlsfo_data():
    vlsfo_data = get_vlsfo_data()
    for date, price in vlsfo_data.items():
        sql_query = f"""
                            INSERT INTO daily_data (date, VLSFO_Bunker_Prices)
                            VALUES ('{date}', {price})
                            ON DUPLICATE KEY UPDATE VLSFO_Bunker_Prices = VALUES(VLSFO_Bunker_Prices);
                            """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ship_bunker_data(origin_data, name_column_dict, config):
    column = name_column_dict[config['name']]
    for date, price in origin_data.items():
        sql_query = f"""
                                INSERT INTO daily_data (date, {column})
                                VALUES ('{date}', {price})
                                ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                                """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_krbn_data():
    data_dict = get_krbn_data()
    for date, price in data_dict.items():
        sql_query = f"""
                       INSERT INTO daily_data (date, KRBN)
                       VALUES ('{date}', {price})
                       ON DUPLICATE KEY UPDATE KRBN = VALUES(KRBN);
                       """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_ctfi_data():
    data_dict = get_ctfi_data()
    date = data_dict['last_date']

    for k, v in data_dict.items():
        if k == 'last_date':
            continue
        sql_query = f"""
                               INSERT INTO daily_data (date, {k})
                               VALUES ('{date}', {v})
                               ON DUPLICATE KEY UPDATE {k} = VALUES({k});
                               """
        print(sql_query)
        execute_query(connection, sql_query)


@retry(attempts=3, delay=2)
def upload_cn_yield_data():
    term_to_column_dict = {
        '3月': 'CN_3M_BOND_YIELD',
        '6月': 'CN_6M_BOND_YIELD',
        '1年': 'CN_1Y_BOND_YIELD',
        '3年': 'CN_3Y_BOND_YIELD',
        '5年': 'CN_5Y_BOND_YIELD',
        '7年': 'CN_7Y_BOND_YIELD',
        '10年': 'CN_10Y_BOND_YIELD',
        '30年': 'CN_30Y_BOND_YIELD'
    }
    date, data_dict = get_cn_yield_data()
    for term, dp in data_dict.items():
        column = term_to_column_dict[term]
        sql_query = f"""
                       INSERT INTO daily_data (date, {column})
                       VALUES ('{date}', {dp})
                       ON DUPLICATE KEY UPDATE {column} = VALUES({column});
                        """
        print(sql_query)
        execute_query(connection, sql_query)


def datetime_to_string(datetime_value):
    return datetime_value.strftime('%Y-%m-%d')


def back_fill_steel_shanghai_10mm():
    df = read_shanghai_10mm()
    for col in df.columns[1:]:
        today = datetime_to_string(df[col][0])
        print(today)
        sh_10mm_price = df[col][1]
        print(df[col][0])
        print(df[col][1])
        sql_query = f"""
            INSERT INTO daily_data (date, 上海市10mm造船板价格)
            VALUES ('{today}', {sh_10mm_price})
            ON DUPLICATE KEY UPDATE 上海市10mm造船板价格 = VALUES(上海市10mm造船板价格);
            """
        print(sql_query)
        execute_query(connection, sql_query)


sheet_to_table_name_map = {
    '广州10mm船板价格': '广州市10mm造船板价格',
    '南京10mm船板价格': '南京市10mm造船板价格',
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
    '新华-泛亚内贸集装箱船运价指数': '新华_泛亚内贸集装箱船运价指数', #https://www.epanasia.com/freightIndex/
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


def back_fill_row_data(row_name_in_sheet='广州10mm船板价格'):
    df = read_row_data(row_name_in_sheet)
    row_name = sheet_to_table_name_map[row_name_in_sheet]
    for col in df.columns[1:]:
        today = datetime_to_string(df[col][0])
        print(today)
        row_data = df[col][1]
        print(df[col][0])
        print(df[col][1])
        sql_query = f"""
            INSERT INTO daily_data (date, {row_name})
            VALUES ('{today}', {row_data})
            ON DUPLICATE KEY UPDATE {row_name} = VALUES({row_name});
            """
        print(sql_query)
        execute_query(connection, sql_query)


if __name__ == '__main__':

    # mysql.connector.connect(
    #     host="sh-cdb-aale09ms.sql.tencentcdb.com",
    #     port=26059,
    #     user="root",
    #     password="xemjyn-kanqoq-gImho4"
    # )

    # connection = connect_to_database(
    #     host_name='sh-cynosdbmysql-grp-pvsmsm7y.sql.tencentcdb.com',
    #     user_name='root',
    #     port=23620,
    #     user_password='Cyl@31415',
    #     db_name='Time_Series'
    # )

    connection = connect_to_database(
        host_name='sh-cdb-aale09ms.sql.tencentcdb.com',
        user_name='root',
        port=26059,
        user_password='Sail@001',
        db_name='Time_Series'
    )

    # upload_steel_data()

    upload_msci_data()

    upload_euribor_data()

    upload_lpr_data()

    upload_shibors_data()

    # upload_iron_ore_data()

    # upload_nanhua_data()

    upload_crb_data()


    upload_vlsfo_data()
    upload_ifo_data()

    upload_ecs_data()
    upload_ecm_data()

    upload_usd_index_data()

    upload_sofr_data()
    upload_sofr_on_data()
    upload_us_yield_data()

    upload_cdi_data()

    upload_scfi_data()

    upload_ccfi_data()

    upload_ctfi_data()

    upload_gold_price_data()


    for config in all_configs:
        origin_data = get_data_from_config_dict(config)
        upload_ship_bunker_data(origin_data=origin_data, name_column_dict=Ship_BUNKER_dict, config=config)

    upload_krbn_data()

    upload_cn_yield_data()

    #
    upload_wti_oil_data()
    #
    upload_cme_data()

    upload_usd_cny_data()
    upload_usd_jpy_data()







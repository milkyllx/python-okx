import time
import pymysql
from datetime import datetime
from okx.MarketData import MarketAPI
from config import SPOT_SYMBOLS

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "juxue654321A!",
    "database": "crypto_follow",
    "charset": "utf8"
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def save_kline_data(instId, timeframe, kline_data):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for k in kline_data:
                timestamp = int(k[0])
                open_price = float(k[1])
                high_price = float(k[2])
                low_price = float(k[3])
                close_price = float(k[4])
                volume = float(k[5])
                sql_check = "SELECT COUNT(1) FROM spot_kline WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
                cursor.execute(sql_check, (instId, timeframe, timestamp))
                exists = cursor.fetchone()[0]

                if exists:
                    sql_update = """
                    UPDATE spot_kline SET open=%s, high=%s, low=%s, close=%s, volume=%s, update_time=CURRENT_TIMESTAMP
                    WHERE inst_id=%s AND timeframe=%s AND timestamp=%s
                    """
                    cursor.execute(sql_update, (open_price, high_price, low_price, close_price, volume, instId, timeframe, timestamp))
                else:
                    sql_insert = """
                    INSERT INTO spot_kline (inst_id, timeframe, timestamp, open, high, low, close, volume, update_time, data_src)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
                    """
                    cursor.execute(sql_insert, (instId, timeframe, timestamp, open_price, high_price, low_price, close_price, volume,'OKX'))
            conn.commit()
    finally:
        conn.close()


def fetch_latest_klines(market_api, instId, timeframe, limit=2):
    data = market_api.get_candlesticks(instId=instId, bar=timeframe, limit=str(limit))
    if data and 'data' in data:
        return data['data']
    return []


def calculate_and_save_sma200(instId, timeframe='1D'):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_select = """
            SELECT timestamp, close FROM spot_kline
            WHERE inst_id=%s AND timeframe=%s
            ORDER BY timestamp DESC
            LIMIT 200
            """
            cursor.execute(sql_select, (instId, timeframe))
            rows = cursor.fetchall()

            if len(rows) < 200:
                print(f"{instId} {timeframe} 数据不足200条，无法计算SMA200")
                return

            closes = [row[1] for row in reversed(rows)]
            timestamps = [row[0] for row in reversed(rows)]

            sma200 = sum(closes) / 200
            latest_timestamp = timestamps[-1]

            sql_check = "SELECT COUNT(1) FROM spot_kline WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
            cursor.execute(sql_check, (instId, timeframe, latest_timestamp))
            exists = cursor.fetchone()[0]

            if exists:
                sql_update = "UPDATE spot_kline SET sma200=%s WHERE inst_id=%s AND timeframe=%s AND timestamp=%s"
                cursor.execute(sql_update, (sma200, instId, timeframe, latest_timestamp))
            else:
                sql_insert = "INSERT INTO spot_kline (inst_id, timeframe, timestamp, sma200) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insert, (instId, timeframe, latest_timestamp, sma200))

            conn.commit()
    finally:
        conn.close()


def scheduled_update():
    api = MarketAPI()
    while True:
        for symbol in SPOT_SYMBOLS:
            try:
                klines = fetch_latest_klines(api, symbol, '1D')
                save_kline_data(symbol, '1D', klines)
                calculate_and_save_sma200(symbol, '1D')
            except Exception as e:
                print(f"处理日线数据时出错: {e}")
            
            try:
                week_klines = fetch_latest_klines(api, symbol, '1W')
                save_kline_data(symbol, '1W', week_klines)
                calculate_and_save_sma200(symbol, '1W')
            except Exception as e:
                print(f"处理周线数据时出错: {e}")

        print(f"{datetime.now()} - 定时数据更新完成")
        time.sleep(15)


if __name__ == '__main__':
    scheduled_update()
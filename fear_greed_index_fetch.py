import requests
import pymysql
import time
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'juxue654321A!',
    'database': 'crypto_follow',
    'charset': 'utf8'
}

# 创建数据库连接
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# 获取恐惧与贪婪指数数据
def fetch_fng_data():
    url = 'https://api.alternative.me/fng/'
    params = {'limit': 1, 'format': 'json'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            return data['data']  # 返回多条数据列表
    return None

# 保存数据到数据库，避免重复
def save_fng_to_db(fng_data_list):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for fng_data in fng_data_list:
                # 检查timestamp是否已存在
                sql_check = "SELECT COUNT(1) FROM index_fear_greed WHERE timestamp=%s"
                cursor.execute(sql_check, (fng_data['timestamp'],))
                exists = cursor.fetchone()[0]
                if exists:
                    print(f"数据已存在，timestamp={fng_data['timestamp']}")
                    continue
                # 插入数据
                sql_insert = "INSERT INTO index_fear_greed (value, value_classification, timestamp) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (fng_data['value'], fng_data['value_classification'],fng_data['timestamp']))
            conn.commit()
    finally:
        conn.close()       

if __name__ == '__main__':
    while True:
        fng_data_list = fetch_fng_data()
        if fng_data_list:
            save_fng_to_db(fng_data_list)
        else:
            print("获取数据失败")
        time.sleep(3600)
import schedule
import threading
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
from config import DB_CONFIG


# 初始化全局浏览器实例
def init_driver():
    service = Service("D:\\devtool\\chromedriver\\chromedriver.exe")  # 替换为你的 ChromeDriver 路径
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式，后台运行
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")  # 解决 Linux 环境下权限问题
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# 数据库保存函数
def save_data_to_db(date, ahr999_index, btc_price, cost_200d):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 检查当天数据是否存在
            sql_check = "SELECT COUNT(1) FROM index_ahr999 WHERE date = %s"
            cursor.execute(sql_check, (date,))
            exists = cursor.fetchone()[0]
            if exists:
                return  # 数据已存在，不插入
            # 插入数据
            sql_insert = """
                INSERT INTO index_ahr999 (date, ahr999_index, btc_price, cost_200d)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (date, ahr999_index, btc_price, cost_200d))
            connection.commit()
    except Exception as e:
        print(f"数据库操作失败: {e}")
    finally:
        connection.close()


# 获取 AHR999 数据并保存到数据库
def fetch_and_save(driver):
    try:
        # 打开目标网页
        driver.get("https://www.coinglass.com/zh/pro/i/ahr999")

        # 等待页面加载完成
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.ant-table-tbody"))
        )

        # 获取页面内容
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")

        # 提取表格行数据
        rows = soup.select("tbody.ant-table-tbody > tr.ant-table-row.ant-table-row-level-0")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                # 获取时间、ahr999囤币指数、BTC价格、200日定投成本
                date = cells[0].div.text.strip()
                ahr999_index = cells[1].div.text.strip()
                btc_price = cells[2].div.text.strip().replace('$', '').replace(',', '')  # 去除美元符号和千分位逗号
                cost_200d = cells[3].div.text.strip().replace(',', '')

                # 转换数据类型
                try:
                    ahr999_index = float(ahr999_index)
                    btc_price = float(btc_price)
                    cost_200d = float(cost_200d)
                except ValueError:
                    print("数据格式异常，跳过")
                    continue

                # 保存到数据库
                save_data_to_db(date, ahr999_index, btc_price, cost_200d)
                print(f"数据保存成功: 时间={date}, AHR999囤币指数={ahr999_index}, BTC价格={btc_price}, 200日定投成本={cost_200d}")
                break  # 只保存当天最新一条数据
    except Exception as e:
        print(f"获取数据失败: {e}")


# 定时任务线程启动函数
def run_schedule():
    while True:
        schedule.run_pending()
        sleep(1)


# 主函数
if __name__ == "__main__":
    # 初始化浏览器
    driver = init_driver()

    # 安排每小时整点执行一次任务
    schedule.every().hour.at(":00").do(fetch_and_save, driver)

    # 启动定时任务线程
    threading.Thread(target=run_schedule, daemon=True).start()

    try:
        # 主程序保持运行
        while True:
            sleep(60)
    except KeyboardInterrupt:
        print("程序退出中...")
    finally:
        # 关闭浏览器
        driver.quit()

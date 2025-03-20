from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
from datetime import datetime
import schedule
import time

URL_VAM = "http://172.31.76.171"

DB_CONFIG = {
    "host": "localhost",  
    "user": "root",
    "password": "rootpassword",
    "database": "mydatabase",
    "port": 3306  
}


def insert_data(vam_data):
    try:
        now = datetime.now()
        path_time_stamp = now.strftime("%d/%m/%y %H:%M:%S")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO VAM_DATA 
            ()
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            str(path_time_stamp),
            float(vam_data[0]),
            float(vam_data[1]),
            float(vam_data[2])
            )
        cursor.execute(insert_query, values)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database Insert Error: {e}")
    finally:
        cursor.close()
        conn.close()
        print("DB connection closed.")

def fetch_data_with_selenium():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        service = Service('/opt/homebrew/bin/chromedriver')  
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(URL_VAM)
        data_divs = driver.find_elements(By.CLASS_NAME, "dVal")
        data_values = [float(div.text) for div in data_divs] 

        driver.quit()
        insert_data(data_values)


        driver.quit()
    except Exception as e:
        print(f"Exception in fetch_data_with_selenium: {e}")

fetch_data_with_selenium()
schedule.every(1).minutes.do(fetch_data_with_selenium)

if __name__ == "__main__":
    print("Starting HTTP polling + MQTT service...")
    while True:
        schedule.run_pending()
        time.sleep(1)
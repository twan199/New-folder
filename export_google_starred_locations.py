from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
import glob
import os.path

listofcsv = (glob.glob("*.csv"))
if os.path.isfile("export/completed.txt"):
    with open('export/completed.txt', 'r') as f:
        completed = f.read().splitlines()
else:
    completed = []

# df_end = pd.DataFrame()
for i in listofcsv:
    if i not in completed:
        df = pd.read_csv(i)
        # df_end = pd.concat([df_end, df], ignore_index=True, sort=False)
        df_end = df
        listofplaces = []
        driver = webdriver.Firefox()
        time.sleep(5)
        print(i)
        for index, row in df_end.iterrows():
            print(row)
            link = row["URL"]
            driver.get(link)
            time.sleep(2)
            try:
                driver.find_element(
                    By.XPATH, "//.[@aria-label='Alles afwijzen']").click()
            except:
                pass
            time.sleep(6)
            # driver.close()
            a = driver.current_url.split("@")[1].split(",")
            listofplaces.append([row["Titel"], a[0], a[1]])
        df = pd.DataFrame(listofplaces, columns=['Name', 'lat', 'long'])
        df.to_csv(f'export/export_{i}',
                  index=False, encoding='utf-8')
        completed.append(i)
        with open('export/completed.txt', 'w') as f:
            for line in completed:
                f.write(f"{line}\n")

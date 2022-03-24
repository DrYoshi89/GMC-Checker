from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from PIL import Image
import os
import time
import json
import pandas as pd
import image
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import easygui

os.environ['PATH'] += r'C:\Users\Dani\Downloads\python main\test 2'
driver = webdriver.Chrome()
driver.get("https://www.gmc-uk.org/registration-and-licensing/the-medical-register")

#grabbing the file from folder
dataframe = pd.read_csv(r"C:\Users\Dani\Downloads\python main\GMC Checker\ahlsdhajsdfh.csv")
print(dataframe)

all_data = []
i = 0
for i in dataframe.index:
    entry = dataframe.iloc[i]
    
    #gmc input
    gmc_input = driver.find_element_by_id('searchForDr')
    gmc_input.send_keys(str(entry['GMC Ref No']))

    #click search
    click_input = driver.find_element_by_id('searchButton')
    driver.execute_script("arguments[0].click();", click_input)

    GP_status = driver.find_element_by_xpath('//*[@id="main"]/div/div/section[2]/div[1]/div[2]/div/div[1]')

    Specialist_status = driver.find_element_by_xpath('//*[@id="main"]/div/div/section[2]/div[2]/div[2]/div/div[1]')

    #finding status covid, gp and specialist register
    try:
        status = driver.find_element_by_class_name('c-dr-details__status_sanctions')
        all_data.append([str(entry['GMC Ref No']), status.text, GP_status.text, Specialist_status.text])
    except Exception:
        pass
        all_data.append([str(entry['GMC Ref No']), "NULL", GP_status.text, Specialist_status.text])

    
    time.sleep(3)
    driver.back()
    time.sleep(3)
    driver.find_element_by_id('searchForDr').clear()

df = pd.DataFrame(all_data)
df.columns =['GMC', 'Covid Status', 'GP Register Status', 'Specialist Status']
df.to_csv(r"C:\Users\Dani\Downloads\python main\GMC Checker\final.csv",index=False)
print(df)


easygui.msgbox("Process has been completed!")
 


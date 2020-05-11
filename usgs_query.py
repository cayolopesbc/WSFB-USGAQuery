import requests
import pandas as pd
import lxml.html as lh
from html_table_extractor.extractor import Extractor


# -*- coding: utf-8 -*-
import time
from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox

######################
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
######################

import os

#soup = BeautifulSoup(url)

#Query build:

#1 - Columns to show
value_1 = "realdate" # Date(MM/DD/YYYY)
value_2 = "stat"    # Station Number

#VARS:
VARS_NAME = ['Depth',
'Discrete Chlorophyll',
'Chlorophyll a/a+PHA ratio',
'Fluorescence',
'Calculated Chlorophyll',
'Discrete Oxygen',
'Oxygen electrode output',
'Oxygen Saturation %',
'Calculated Oxygen',
'Discrete SPM',
'Optical Backscatter',
'Calculated SPM',
'Measured Extinction Coeff',
'Calculated Extinction Coeff',
'Salinity',
'Temperature',
'Sigma-t',
'Nitrite',
'Nitrate+Nitrite',
'Ammonium',
'Phosphate',
'Silicate'
]


value_1 = "-2" # Date(MM/DD/YYYY)
value_2 = "-1"    # Station Number


VARS = {
    "-2": "realdate",
    "-1": "stat",
    '1': 'depth',
    '2': 'dscrchl',
    '3': 'chlrat',
    '4': 'fluor',
    '5': 'calcchl',
    '6': 'dscroxy',
    '7': 'oxy',
    '8': 'oxysat',
    '9': 'calcoxy',
    '10': 'dscrspm',
    '11': 'obs',
    '12': 'calcspm',
    '13': 'dscrexco',
    '14': 'excoef',
    '15': 'salin',
    '16': 'temp',
    '17': 'sigt',
    '18': 'no2',
    '19': 'no32',
    '20': 'nh4',
    '21': 'po4',
    '22': 'si',
    }

for i in range(0,22):
    print('{} - {}'.format(str(i+1),VARS_NAME[i]))
print('Digite Quit para encerrar a escolha de variáveis')

choose = ''
query = [value_1,value_2]

while choose.upper() != 'QUIT':
    choose = input('Código da variável: ')
    if choose.upper() != 'QUIT':
        query.append(choose)


def download_download_usgs(outputfile):

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.dir", dir_out)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    fp.set_preference("browser.download.manager.showWhenStarting", False) 
    fp.set_preference("browser.download.useDownloadDir", True)
    fp.set_preference("browser.helperApps.alwaysAsk.force", False)
    fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
    fp.set_preference("browser.download.manager.closeWhenDone", True)
    fp.set_preference("browser.download.manager.showAlertOnComplete", False)
    fp.set_preference("browser.download.manager.useWindow", False)
    fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
    fp.set_preference("pdfjs.disabled", True)
    fp.set_preference("browser.link.open_newwindow.override.external", True)


    #C:\Program Files (x86)\Mozilla Firefox
    binary = FirefoxBinary("C://Program Files//Mozilla Firefox//firefox.exe")
    
    driver = webdriver.Firefox(firefox_profile=fp,firefox_binary=binary, executable_path='C://geckodriver')
    wait = WebDriverWait(driver, 10)
    driver.minimize_window()
    url = 'https://sfbay.wr.usgs.gov/access/wqdata/query/expert.html'
    driver.get(url)
    
    time.sleep(1)

    # 1 - Columns to Show
    for var in query:
        
        if int(var) <= 17:
            driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[1]/td[1]/font/input[@value='"+VARS[var] +"']").click()
        
        elif 17 < int(var) & int(var) <= 20:
            driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td[1]/font/input[@value='"+ VARS[var] +"']").click()
        else:
            driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td[2]/font/input[@value='"+ VARS[var] +"']").click()

    # 3 - Sort by:
    name1 = 'sort1'
    value_3 = 'fulldate'
    name2 = 'sort2'
    value_4 = 'stat'
    name3  = 'sort3'
    value_5 = 'depth'

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[4]/td[1]/select/option[2]").click()
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[5]/td[1]/select/option[3]").click()
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[6]/td[1]/select/option[5]").click()

    
    #4 - Table Format
    name4 = 'out'
    value = 'html' #comma
    name5 = 'param'
    name6 = 'maxrow' # 10, 50, 100, 500, 1000, "99999"

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[8]/th/table/tbody/tr/td/select/option[1]").click()
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[8]/th/table/tbody/tr/td/font/select/option[5]").click()

    #5 - Submit
    type7 = 'submit'
    name7 = "Query Database"
    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/th/table/tbody/tr/th[2]/span/form/table/tbody/tr/td/table/tbody/tr[8]/th/table/tbody/tr/th/input[2]").click()

    alert = driver.switch_to_alert()
    alert.accept()

    # Get Data:
    
    info = wait.until(ec.visibility_of_element_located(( By.XPATH,"/html/body/form[2]/table/tbody/tr/td[1]"))).text    
    noData = info.split('out of ')[1][:-10]
    countData = info.split('out of ')[0].split('to ')[1][:-1]
    
    subname = '10p'
    n = 1
    w = 1
    while countData != noData:
        table = driver.find_element_by_xpath('/html/body/table[3]')
        extractor = Extractor(table.get_attribute("outerHTML")).parse()
        extractor.write_to_csv(path='.')

        if float(countData) > float(noData)*0.1*n:
            n += 1
            subname = str(n)+'0p'

        out_file = subname + '_' + outputfile

        if os.path.exists(os.path.join(os.getcwd(),out_file)):
            df = pd.read_csv(os.path.join(os.getcwd(),out_file))
            data = pd.read_csv(os.path.join(os.getcwd(),'output.csv'), encoding = 'cp1252')
            df = pd.concat([df,data], ignore_index = True)
            df.to_csv(os.path.join(os.getcwd(),out_file))
        else:
            data = pd.read_csv(os.path.join(os.getcwd(),'output.csv'), encoding = 'cp1252')
            data.to_csv(os.path.join(os.getcwd(),out_file))

        info = wait.until(ec.visibility_of_element_located(( By.XPATH,"/html/body/form[2]/table/tbody/tr/td[1]"))).text 
        countData = info.split('out of ')[0].split('to ')[1][:-1]
        print(countData)
        print(w)
        w+=1
        try:
            driver.find_element_by_xpath("/html/body/form[2]/table/tbody/tr/td[1]/input").click()
        except:
            print("Programa encerrado. Checar se todos os dados foram baixados")
    return Data

        
df = download_usgs('outputData.csv')

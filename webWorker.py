
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import base64
from deep_translator import GoogleTranslator

manualTranslator = {}
f = open('manualTranslator.txt', 'r', encoding='utf-8')
for line in f.readlines():
    data = line.split('\t')
    manualTranslator[data[0]] = data[1].strip()
    manualTranslator[data[0]+":"] = data[1].strip()+":"
f.close()

translator = GoogleTranslator(source='en', target='es')
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options)
driver.get("https://army-forge.onepagerules.com/")
sleep(3)
driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-u4p24i']/button[1]").click()
f = open('ListLinks.txt','r')

firstLoop = True
for lin in f.readlines():
    fileName = lin.split("name=")[1][:-1]
    driver.get(lin)
    sleep(5)
    if firstLoop:
        driver.find_element(By.XPATH, "//div[@class='MuiStack-root no-print css-1mhrztx']/button[2]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//li[@class='MuiListItem-root MuiListItem-gutters MuiListItem-padding css-j4r5fq']/span[1]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-1xctuv5']/button[1]").click()
        firstLoop = False
    elems = driver.find_elements(By.XPATH, "//div[@class='MuiContainer-root css-2og7kz']//span")
    #elems += driver.find_elements(By.XPATH, "//div[@class='MuiContainer-root css-2og7kz']//td")
    for i in elems:
        try:
            orig = i.text
            if orig == None: continue
            if orig.strip() in list(manualTranslator.keys()):
                trans = orig.replace(orig.strip(), manualTranslator[orig.strip()])

            else:
                trans = orig.replace(orig.strip(), translator.translate(text =orig.strip()))
            driver.execute_script("arguments[0].innerText = '{}'".format(trans), i)
        except Exception as e:
            print(e)
            None

    pdf = driver.print_page()
    with open('{}.pdf'.format(fileName), 'wb') as file:
        file.write(base64.b64decode(pdf))

f.close()
driver.close()
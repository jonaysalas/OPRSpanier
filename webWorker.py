
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import base64
from deep_translator import MyMemoryTranslator

manualTranslator = {}
f = open('manualTranslator.txt', 'r', encoding='utf-8')
for line in f.readlines():
    data = line.split('\t')
    manualTranslator[data[0]] = data[1].strip()
    manualTranslator[data[0]+":"] = data[1].strip()+":"
f.close()

prevTranslator = {}
f = open('translatorHistoryv341.txt', 'r', encoding='utf-8')
for line in f.readlines():
    data = line.split('\t')
    if data[1].strip()[-2:] == "::": continue
    prevTranslator[data[0]] = data[1].strip()
f.close()

translator = MyMemoryTranslator(source='english', target='spanish')
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options)
driver.get("https://army-forge.onepagerules.com/")
sleep(3)
driver.find_element(By.XPATH, "//div[@class='MuiStack-root css-u4p24i']/button[1]").click()
f = open('ListLinks.txt','r')

for lin in f.readlines():
    try:
        fileName = lin.split("name=")[1][:-1]
        fileName = fileName.replace("%20", "_")
        driver.get(lin)
        sleep(5)
        elems = driver.find_elements(By.XPATH, "//div[@class='MuiContainer-root css-2og7kz']//span")
        #elems += driver.find_elements(By.XPATH, "//div[@class='MuiContainer-root css-2og7kz']//td")
        for i in elems:
            try:
                orig = i.text
                if orig == None: continue
                elif orig.strip()[-1] == '+': continue
                if orig.strip() in list(manualTranslator.keys()):
                    trans = orig.replace(orig.strip(), manualTranslator[orig.strip()])
                elif orig.strip() in list(prevTranslator.keys()):
                    trans = orig.replace(orig.strip(), prevTranslator[orig.strip()])
                else:
                    trans = orig.replace(orig.strip(), translator.translate(orig.strip()))
                    prevTranslator[orig.strip()] = trans

                driver.execute_script("arguments[0].innerText = '{}'".format(trans), i)
            except Exception as e:
                print(e)
                None

        sleep(5)
        pdf = driver.print_page()
        with open('{}.pdf'.format(fileName), 'wb') as file:
            file.write(base64.b64decode(pdf))
        
        print("The {} army list generated in pdf".format(fileName))
    except:
        continue

f.close()

f = open('translatorHistoryv341.txt', 'w', encoding='utf-8')
txt = ""
for key in list(prevTranslator.keys()):
    txt += "{}\t{}\n".format(key, prevTranslator[key])
f.write(txt[:-1]) #we remove the last '\n'
f.close()
driver.close()
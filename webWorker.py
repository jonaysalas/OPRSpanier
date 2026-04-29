
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions
from time import sleep
import base64
from deep_translator import MyMemoryTranslator

print("V1.1")
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
    if "\t\n" in line:
        continue
    print(line)
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
try:
    driver.find_element(By.XPATH, "//div[@class='MuiStack-root mui-u4p24i']/button[1]").click()
except:
    print("No needed to close the dialog")
f = open('ListLinks.txt','r')

for lin in f.readlines():
    try:
        fileName = lin.split("name=")[1][:-1]
        fileName = fileName.replace("%20", "_")
        driver.get(lin)
        sleep(5)
        elems = driver.find_elements(By.TAG_NAME, "span")
        #elems += driver.find_elements(By.XPATH, "//div[@class='MuiContainer-root css-2og7kz']//td")
        for i in elems:
            try:
                orig = i.text
                if orig == None: continue
                elif orig.strip()[-1] == '+': continue
                #If it is a name of the unit, only translate the name
                if '[' in orig and 'pts' in orig: #is a name
                    justName = orig.split('[')[0].strip()
                    if justName in list(manualTranslator.keys()):
                        trad = manualTranslator[justName]
                    elif orig.strip() in list(prevTranslator.keys()):
                        trad = prevTranslator[justName]
                    else:
                        trad = translator.translate(justName)
                        if len(trad) > 1:
                            prevTranslator[justName] = trad
                    trans = orig.replace(justName, trad)
                    
                else:
                    if orig.strip() in list(manualTranslator.keys()):
                        trans = orig.replace(orig.strip(), manualTranslator[orig.strip()])
                    elif orig.strip() in list(prevTranslator.keys()):
                        trans = orig.replace(orig.strip(), prevTranslator[orig.strip()])
                    else:
                        trans = orig.replace(orig.strip(), translator.translate(orig.strip()))
                        if len(trans) > 1:
                            prevTranslator[orig.strip()] = trans

                driver.execute_script("arguments[0].innerText = '{}'".format(trans), i)
            except Exception as e:
                print(e)
                None
        '''
        elems = driver.find_elements(By.XPATH, "//div[@class='MuiBox-root mui-1v95bqz']//span")
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
                if ":" in trans:
                    trans = trans.replace(":", ": ")
                driver.execute_script("arguments[0].innerText = '{}'".format(trans), i)
            except Exception as e:
                print(e)
                None
        '''
        sleep(5)
        print_options = PrintOptions()
        print_options.shrink_to_fit = True 
        print_options.page_height = 29.7  # Use page_width to assign width
        pdf = driver.print_page(print_options)
        with open('{}.pdf'.format(fileName), 'wb') as file:
            file.write(base64.b64decode(pdf))
        
        print("The {} army list generated in pdf".format(fileName))
    except Exception as e:
        print(e)
        continue
f.close()

f = open('translatorHistoryv341.txt', 'w', encoding='utf-8')
txt = ""
for key in list(prevTranslator.keys()):
    if prevTranslator[key].strip() != "":
        txt += "{}\t{}\n".format(key, prevTranslator[key])
f.write(txt[:-1]) #we remove the last '\n'
f.close()
driver.close()
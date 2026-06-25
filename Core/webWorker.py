
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.edge.options import Options as OptionsEdge
from selenium.webdriver.common.print_page_options import PrintOptions
from time import sleep
import base64
from deep_translator import MyMemoryTranslator
import os
from Core.GeneralMethods import LoadATranslatorDictionary, SaveATranslatorDictionary

class WebWorker:

    def __init__(self, prevTranslations, manualTranslations = None):
        self.availableBrowsers = ['firefox', 'chrome', 'edge']
        self.prevTranslationsLink = prevTranslations
        self.Translations = LoadATranslatorDictionary(prevTranslations)

        self.ManualTranslations = {}
        if manualTranslations != None:
            self.ManualTranslations = LoadATranslatorDictionary(manualTranslations)

        self.Translator = MyMemoryTranslator(source='english', target='spanish')
    
    def GetAvailableBrowsers(self):
        return self.availableBrowsers
    
    def CreateWebDriver(self, browser, browVisible=False):
        try:
            if browser.lower() in self.availableBrowsers:
                if browser.lower() == 'firefox':
                    options = OptionsFirefox()
                elif browser.lower() == "chrome":
                    options = OptionsChrome()
                elif browser.lower() == 'edge':
                    options = OptionsEdge()
                
                if browVisible == False:
                    options.add_argument('-headless')
                
                if browser.lower() == 'firefox':
                    self.driver = webdriver.Firefox(options)
                elif browser.lower() == "chrome":
                    self.driver = webdriver.Chrome(options)
                else:
                    self.driver = webdriver.Edge(options)
            
            return ""
        except Exception as e:
            return str(e)
    
    def DestroyWebDriver(self):
        self.driver.close()

    def PrepareTheBrowser(self):
        self.driver.get("https://army-forge.onepagerules.com/")
        sleep(3)
        try:
            self.driver.find_element(By.XPATH, "//div[@class='MuiStack-root mui-u4p24i']/button[1]").click()
        except:
            None #No need to close the dialog


    def avoidTranslation(self, word):
        #To save space in the translator, we will avoid translate things like ranges, 4+, AX...
        if "pts" in word: #is the point cost. Not translated
            return True
        
        if word[0] == 'A':
            if word[1:].isdigit(): #Its an attack attribute
                return True
        
        if word[-1] == '+': #Is an attribute, like the Quality
            if len(word) == 1: #is just the + characer
                return True
            elif word[:-1].isdigit(): #its an attribute like 4+
                return True

        if word[-1] == '"':
            if word[:-1].isdigit(): #its a range, like 12"
                return True

    def PrepareTheWordToTransalte(self,word):
        #Clean the message from (), : and others...
        cleaned = word
        if cleaned.find('(') != -1: #If it an ability with a number, we will ignore the number
            if cleaned[cleaned.find('(')+1:cleaned.find(')')].isdigit(): #is something like Blast(3) or Though(12)
                cleaned = cleaned[:cleaned.find('(')]
        elif cleaned.find(':') != -1: #Sometimes, a word ending in : is translated in a weird way
            cleaned = cleaned[:cleaned.find(':')]
        
        return cleaned

    def TranslateALink(self, link, pathToPdf):
        try:
            fileName = link.split("name=")[1][:-1]
            fileName = fileName.replace("%20", "_")

            self.driver.get(link)
            sleep(5)
            elems = self.driver.find_elements(By.TAG_NAME, "span")
            
            for i in elems:
                try:
                    orig = i.text
                    if orig == None: continue #Is empty, nothing to translate
                    elif orig.strip()[-1] == '+': continue #Is a attribute like "6 +" or "4 +"
                    
                    #If it is a name of the unit, only translate the name
                    if '[' in orig: #is a name of a unit
                        continue #Editing the text in the span causes to lose the style
                    elif self.avoidTranslation(orig):
                        continue
                    else: #Other cases
                        word = self.PrepareTheWordToTransalte(orig)
                        if word.strip() in list(self.ManualTranslations.keys()): #This phrase was translated manually
                            trans = orig.replace(word.strip(), self.ManualTranslations[word.strip()])
                        elif word.strip() in list(self.Translations.keys()): #This phrase was already translated
                            trans = orig.replace(word.strip(), self.Translations[word.strip()])
                        else: #Is the first time we translate this phrase
                            newWord = self.Translator.translate(word.strip())
                            trans = orig.replace(word.strip(), newWord)
                            if len(trans) > 1: #It was translated correctly, so save it for future times
                                self.Translations[word.strip()] = newWord
                    self.driver.execute_script("arguments[0].innerText = '{}'".format(trans), i) #Change the text
                except Exception as e:
                    print(e)
                    None
            
            print("_______________P____________")
            elems = self.driver.find_elements(By.TAG_NAME, "p")
            for i in elems:
                try:
                    orig = i.text
                    
                    if orig == None: continue #Is empty, nothing to translate
                    elif orig.strip()[-1] == '+': continue #Is a attribute like "6 +" or "4 +"
                    
                    #If it is a name of the unit, only translate the name
                    if '[' in orig: #is a name of a unit
                        justName = orig.split('[')[0].strip() #Get only the name
                        if justName in list(self.ManualTranslations.keys()): #This name was translated Manually
                            trad = self.ManualTranslations[justName]
                        elif justName in list(self.Translations.keys()): #This name was translated before
                            trad = self.Translations[justName]
                        else: #Is the first time we translate this name
                            trad = self.Translator.translate(justName)
                            if len(trad) > 1: #It was translated correctly, save it for future times
                                self.Translations[justName] = trad
                        trans = orig.replace(justName, trad)
                    else:
                        continue #the names had finished

                    self.driver.execute_script("arguments[0].innerText = '{}'".format(trans), i) #Change the text
                except Exception as e:
                    print(e)
                    None
            
            print("______________TD____________")
            elems = self.driver.find_elements(By.TAG_NAME, "td")
            for i in elems:
                try:
                    if i.find_elements(By.TAG_NAME, "span") != []:
                        #it has a span child, already translated
                        continue

                    orig = i.text
                    
                    if orig == None: continue #Is empty, nothing to translate
                    elif orig.strip()[-1] == '+': continue #Is a attribute like "6 +" or "4 +"
                    
                    if self.avoidTranslation(orig):
                        continue
                    
                    word = self.PrepareTheWordToTransalte(orig)
                    if word.strip() in list(self.ManualTranslations.keys()): #This phrase was translated manually
                        trans = orig.replace(word.strip(), self.ManualTranslations[word.strip()])
                    elif word.strip() in list(self.Translations.keys()): #This phrase was already translated
                        trans = orig.replace(word.strip(), self.Translations[word.strip()])
                    else: #Is the first time we translate this phrase
                        newWord = self.Translator.translate(word.strip())
                        trans = orig.replace(word.strip(), newWord)
                        if len(trans) > 1: #It was translated correctly, so save it for future times
                            self.Translations[word.strip()] = newWord

                    self.driver.execute_script("arguments[0].innerText = '{}'".format(trans), i) #Change the text
                except Exception as e:
                    print(e)
                    None

            sleep(5)
            print_options = PrintOptions()
            print_options.shrink_to_fit = False 
            print_options.page_height = 29.7  # Use page_width to assign width
            pdf = self.driver.print_page(print_options)
            with open(os.path.join(pathToPdf,'{}.pdf'.format(fileName)), 'wb') as file:
                file.write(base64.b64decode(pdf))
            
            return "" #Correctly Generated
        except Exception as e:
            return str(e)

    def CheckNewTranslations(self):
        oldTranslator = LoadATranslatorDictionary(self.prevTranslationsLink)

        newTranslations = {}
        for key in list(self.Translations.keys()):
            if key not in list(oldTranslator.keys()) and key not in list(self.ManualTranslations.keys()): #is a new translation
                newTranslations[key] = self.Translations[key]
            else: #is an old translation
                None
        
        del oldTranslator
        return newTranslations

    def SaveTranslations(self):
        SaveATranslatorDictionary(self.Translations, self.prevTranslationsLink)

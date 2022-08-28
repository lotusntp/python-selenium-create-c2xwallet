from outcome import acapture
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import inquirer
from inquirer.themes import GreenPassion
from data_sheet import SHEET
import json
import os , glob
from Google import Create_Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
from Firebase import FIREBASE
from Line import LINE
import matplotlib.pyplot as plt

firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": "",
  "databaseURL":""
}

email = "email@gmail.com"
password = "password"

firebase = FIREBASE(firebaseConfig)

line = LINE("")


root_dir = r"C:\Users\Administrator\Documents\python\Selenium\PJ01"
dest_dir = os.path.join(root_dir,"QR")

confirm = {
    inquirer.Confirm('confirmed',
                     message="Do you want to get data ?" ,
                     default=True),
    }

confirmAgain = {
    inquirer.Confirm('confiragain',
                     message="Do you should get data first ?" ,
                     default=True),
    }

questions = [
    inquirer.List('wallet',
                message="Do yon need wallet?",
                choices=['C2X', 'Wemix'],
            ),
    ]



chrome_options = ChromeOptions()
chrome_options.add_extension('c2x.crx')

driver = webdriver.Chrome('./chromedriver',options=chrome_options)

wait = WebDriverWait(driver, 5)

def open_jsonEr(text):
    try:
        return open(text)
    except ValueError as e:
        print(f'Not have file {e}')
        return None # or: raise

def parse(text):
    try:
        return json.load(text)
    except ValueError as e:
        print(f'invalid json: file {text} not data')
        return None # or: raise

def inputData():
    print()

def find_text_lable(element):
       word = driver.find_element(By.XPATH,element).text
       word = word.split()
       word = word[0]

       return word

def split_mnemonic(mnemonic,word_first,word_second):

        
    
        strMnemonicArr = mnemonic.split()
        i = 1
        keys = []
        mnemo = []
        for key in strMnemonicArr:
            str_key = ""
            if i == 1 or i == 21:
                str_key = str(i)+"st"
            elif i == 2 or i == 22:
                str_key = str(i)+"nd"
            elif i == 3 or i == 23:
                str_key = str(i)+"rd"
            else:
                str_key = str(i)+"th"
            
            mnemo.append(key)
            keys.append(str_key)
            i = i+1 

        mnemonic_dictionary = dict(zip(keys, mnemo))
        check_word_first = mnemonic_dictionary[word_first]
        check_word_second = mnemonic_dictionary[word_second]

        check = serach_word(check_word_first)
        if check == True:
            check_2 = serach_word_second(check_word_second)
            if check_2 == True:
                driver.find_element(By.XPATH,f'//button[text()="Submit"]').click()

def serach_word(check_word_first):
    check = False
    for x in range(1,7):
            check_button_one = driver.find_element(By.XPATH,f"//*[@id='station']/article/section/div/form/div[1]/section/button[{x}]").text
            if  check_button_one == check_word_first:
                    driver.find_element(By.XPATH,f"//*[@id='station']/article/section/div/form/div[1]/section/button[{x}]").click()
                    check = True
                    break
    
    return check
def serach_word_second(check_word_second):
    check = False
    for x in range(1,7):
            check_button_two = driver.find_element(By.XPATH,f"//*[@id='station']/article/section/div/form/div[2]/section/button[{x}]").text
            if  check_button_two == check_word_second:
                    driver.find_element(By.XPATH,f"//*[@id='station']/article/section/div/form/div[2]/section/button[{x}]").click()
                    check = True
                    break
    return check
            

def move_files(images,targetFolder):
    try:
        if images:
            for image in images:
                shutil.move(image,targetFolder)
    except:
        print('dont file')


if __name__ == '__main__':

    # firebase.create_user("email@gmail.com","password")

    
    SHEET(True)
    account_list = json.load(open('data.json'))
    newAcc = []
    newObj = []
    pig = 1
    for key in account_list:
        
        email = key['email'].partition('@')[0]
        driver.get("chrome-extension://ofeeamlegilfbjlgbephmdhchpblfigo/index.html#/auth/new")
        time.sleep(5)
        driver.find_element(By.NAME,"name").send_keys(email)
        driver.find_element(By.NAME,"password").send_keys("qwertyuiop")
        driver.find_element(By.NAME,"confirm").send_keys("qwertyuiop")
        driver.find_element(By.CLASS_NAME,"Copy_button__Hcrbf").click()
        driver.find_element(By.CLASS_NAME,"Checkbox_track__2gz9s").click()
        mnemonic = driver.find_element(By.NAME,"mnemonic")
        mnemonic_value = mnemonic.get_attribute('value')
        new_key_values_dict = {'email': key['email'], 'pass': key['pass'],'mnemonic': mnemonic_value}
        
        newObj.append(new_key_values_dict)
        newAcc.append(mnemonic_value)

        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@id='station']/article/section/div/form/button").click()
        time.sleep(2)
        text_lable_one = find_text_lable("//*[@id='station']/article/section/div/form/div[1]/header/label")
        text_lable_two = find_text_lable("//*[@id='station']/article/section/div/form/div[2]/header/label")
        split_mnemonic(mnemonic_value,text_lable_one,text_lable_two)
        time.sleep(3)
        driver.find_element(By.XPATH,f'//button[text()="Connect"]').click()
        time.sleep(3)
        driver.get('chrome-extension://ofeeamlegilfbjlgbephmdhchpblfigo/index.html#/auth/export')
        time.sleep(3)
        driver.find_element(By.NAME,"password").send_keys("qwertyuiop")
        driver.find_element(By.XPATH,f'//button[text()="Submit"]').click()
        time.sleep(3)
        driver.save_screenshot(f"{email}.png")
        time.sleep(3)

    with open('xyz.txt', "a") as fhandle:
        for line in newAcc:
            fhandle.write(f'{line}\n')
            
    images = glob.glob("**\*.png",recursive=True)
    move_files(images,dest_dir)

    with open("sample.json", "w") as outfile:
        json.dump(newObj, outfile)


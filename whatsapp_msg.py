from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # import webdriver manager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # to use command keys in test browser, like ENTER/SHIFT/ESC
from selenium.webdriver.support.wait import WebDriverWait # to wait for a certain condition to occur
from selenium.webdriver.support import expected_conditions as EC # to specify the condition
from time import sleep # to pause code execution
from datetime import datetime # to create current timestamp
import pandas as pd

# read excel as dataframe
message_df = pd.read_excel("export_result/message_list_result.xlsx")
# store phone numbers as list
phone_list = list(message_df["PhoneNumber"])

# initialize Google Chrome with a Selenium WebDriver object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# create 60s wait object
wait = WebDriverWait(driver, 100)

# open whatsapp web and scan QR code to log in
driver.get("https://web.whatsapp.com/")
sleep(30) # pause code execution as log in buffer time

## FUNCTION to write emoji in selenium
def paste_content(driver, element, content):
    driver.execute_script(
      f'''
const text = `{content}`;
const dataTransfer = new DataTransfer();
dataTransfer.setData('text', text);
const event = new ClipboardEvent('paste', {{
  clipboardData: dataTransfer,
  bubbles: true
}});
arguments[0].dispatchEvent(event)
''',
      element)

## FOR LOOP to iterate over numbers in phone list
for index, number in enumerate(phone_list):
    try:
        ### STEP: create variables to read gptText and imagePath
        # first greeting message
        hello_msg = "🧧Greetings from Isabella!"
        note_msg = "💻 Below text and image are created by OpenAI and sent automatically 💻"
        # ai greeting message
        ai_msg = message_df["gptText"][index]
        # ai image file path
        image_folder = "/Users/isabellashao/Desktop/Github/OpenAI-Whatsapp/"
        ai_image = image_folder + message_df["imagePath"][index]

        ## STEP: open chat link for each number
        chat_url = "https://web.whatsapp.com/send?phone="
        driver.get(chat_url + str(number))

        ## STEP: send hello text message
        # variable to hold the XPATH of textbox element
        input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p'
        # wait until textbox element is clickable
        input_box = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        # pass hello message
        paste_content(driver, input_box, hello_msg)
        sleep(5) # pause for buffer
        # line break
        input_box.send_keys(Keys.SHIFT, Keys.ENTER)
        # pass note message
        paste_content(driver, input_box, note_msg)
        # hit enter
        input_box.send_keys(Keys.ENTER)
        sleep(5) # pause for buffer
        
        ## STEP: send OpenAI message and image

        ### STEP: click attachment icon
        # variable to hold the XPATH of clip element
        clip_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span'
        # wait until clip element is clickable
        clip_icon = wait.until(EC.element_to_be_clickable((By.XPATH, clip_xpath)))
        # click on clip element
        clip_icon.click()
        
        ### STEP: upload image attachment
        # variable to hold the XPATH of image attachment element
        image_input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input'
        # wait until image attachment element is located
        image_attach = wait.until(EC.presence_of_element_located((By.XPATH, image_input_xpath)))
        # pass image file path as attachment input
        image_attach.send_keys(ai_image)
        
        ### STEP: add message & send
        # variable to hold the XPATH of image preview textbox element
        preview_input_xpath = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p'
        # wait until image preview textbox element is clickable
        preview_input_box = wait.until(EC.element_to_be_clickable((By.XPATH, preview_input_xpath)))
        # type message
        preview_input_box.send_keys(ai_msg)
        # hit enter
        preview_input_box.send_keys(Keys.ENTER)
        sleep(10) # pause for buffer

        ## STEP: mark message sent time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_df["msgSent"][index] = now
        print(index)
        print(now)
    
    except:
        pass

# write dataframe to file
message_df.to_excel("export_result/message_list_sent.xlsx")
from dotenv import load_dotenv # to create environment variable
import os # to access environment variable
import openai # OpenAI library
import pandas as pd # for data manipulation
import requests # to make HTTP request, ex. download url file
from datetime import datetime # to create current timestamp

# initialize environment variable
load_dotenv()
# call api
openai.api_key = os.getenv("OPENAI_API_KEY")

# read excel as dataframe
message_df = pd.read_excel("message_list.xlsx")
# store phone number as list
phone_list = list(message_df["PhoneNumber"])

## FUNCTION to create text prompt
def create_prompt(lang, tone, name):
    # create nested dictionary to hold a selection of custom tones by languages
    lang_tone = {
        "EN" : {
            "1" : "heart-warming and funny",
            "2" : "hopeful and light-hearted",
            "3" : "humorous and encouraging"
        },
        "CH" : {
            "1" : "真誠",
            "2" : "有趣",
            "3" : "幽默"
        }
    }
    # create text prompt by language
    if lang == "EN":
        text_prompt = f"Write a 20-word {lang_tone[lang][tone]} 2023 Rabbit Lunar New Year Greeting for {name}"
    elif lang == "CH":
        text_prompt = f"寫給{name}的十五字的{lang_tone[lang][tone]}的2023兔年新春賀詞"
    
    return text_prompt

## FUNCTION to create OpenAI text completion response
def text_completion(text_prompt, temp):
    # create an OpenAI text completion response with custom prompt and temp
    response = openai.Completion.create(model="text-davinci-003", prompt=text_prompt, temperature=temp, max_tokens=60)
    # list that holds result json
    response_result = response["choices"]

    # for loop to access json wrapped inside list
    for result in response_result:
        # access target element in json, clean string, store string in variable
        gpt_text = result["text"].replace('\n','').replace('"','')
      
    # store response descriptions in variables
    gpt_object = response["object"]
    completion_tokens = response["usage"]["completion_tokens"]
    prompt_tokens = response["usage"]["prompt_tokens"]
    total_tokens = response["usage"]["total_tokens"]
    
    return gpt_text, gpt_object, completion_tokens, prompt_tokens, total_tokens

## FUNCTION to create OpenAI image creation response
def image_creation(text_prompt, gpt_text):
    # create image prompt from the combination of text prompt and text completion result
    image_prompt = text_prompt + ": " + gpt_text
    # create an OpenAI image creation response with image prompt
    response = openai.Image.create(prompt=image_prompt, n=1, size="256x256")
    # store url in variable
    image_url = response["data"][0]["url"]

    return image_url

## FUNCTION to download image url
def download_image(number, image_url):
    # create path name for each image
    # save in a folder named [dalle_images] in current directory
    # save file name as [phone number.png]
    image_path = "dalle_images/" + str(number) + ".png"
    
    # call http request to get url image
    response = requests.get(image_url)
    
    # save http request to local folder
    if response.status_code:
        save_image = open(image_path, "wb") # open image path
        save_image.write(response.content) # write http request response to image path
        save_image.close()
    
    return image_path
## end of function

# FOR LOOP to create text prompt - gpt text - image link for each contact
for index, number in enumerate(phone_list):
    try:
        ## STEP: create text prompt for each contact based on custom inputs
        # prepare variables for creating text prompt
        lang = message_df["Language"][index]
        tone = str(message_df["Tone"][index])
        name = message_df["ContactName"][index]
        # call function
        text_prompt = create_prompt(lang, tone, name)
        # write response to column
        message_df["textPrompt"][index] = text_prompt

        ## STEP: call OpenAI API for text completion based on each text prompt
        # prepare variable for creating text completion response
        temp = message_df["Temperature"][index]
        # call function
        gpt_text, gpt_object, completion_tokens, prompt_tokens, total_tokens = text_completion(text_prompt, temp)
        # write responses to columns
        message_df["gptText"][index] = gpt_text
        message_df["gptObject"][index] = gpt_object
        message_df["completionUsage"][index] = completion_tokens
        message_df["promptUsage"][index] = prompt_tokens
        message_df["totalUsage"][index] = total_tokens

        ## STEP: call OpenAI API for image creation based on each text prompt + gpt text
        # call function
        image_url = image_creation(text_prompt, gpt_text)
        # write response to column
        message_df["imageLink"][index] = image_url

        ## STEP: download image url to local folder
        # call function
        image_path = download_image(number, image_url)
        # write response to column
        message_df["imagePath"][index] = image_path

        # print preview
        print(index)
        print(gpt_text)
        print(image_url)
        print(image_path)

    except:
        pass

# save file
message_df.to_excel("export_result/message_list_result.xlsx")
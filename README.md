# OpenAI-Text-and-Image-to-Automated-Whatsapp-Message
Program to generate unique festival greeting texts and images with OpenAI, and automate WhatsApp messaging with Selenium

Follow my Instagram for more creative programming content: https://instagram.com/issyshao9?igshid=YmMyMTA2M2Y=

## Project Flow
1. Export iCloud/Google contacts to excel
    1. Export contacts as vcard file
    2. Convert vcard file to excel https://labs.brotherli.ch/vcfconvert/

2. Excel: Data preparation
    1. Clean contact data
    2. Add columns to set input
        1. **Language** to use in creating text prompt and text message, input set based on the contact person’s language preference
        2. **Tone** to use in creating text prompt, set randomly
        3. **Temperature** to use in OpenAI text completion, set randomly
    3. Add columns for writing output
        1. textPrompt: description given to OpenAI to generate text completion
        2. gptText: text completion response from OpenAI
        3. gptObject: object response from OpenAI
        4. promptUsage: tokens used in prompt
        5. completionUsage: tokens used in completion
        6. totalUsage: total tokens used
        7. imageLink: url link in image creation response from OpenAI
        8. imagePath: local file path name
        9. msgSent: message sent time

3. Python Script: Get OpenAI response
    1. Create unique text prompt for each contact person.
    2. Send textPrompt and Temperature to OpenAI and request for text completion. Write responses [gptText, gptObject, promptUsage, completionUsage, totalUsage] to excel.
    3. Set image_prompt as textPrompt + gptText. Send image_prompt to OpenAI and request for image creation. Write response [imageLink] to excel.
    4. Download imageLink to local folder. File name as imagePath.

4. Python Script: Send Whatsapp messages using Selenium
    1. Initialise WhatsApp Web with Selenium. Manually scan QR code to log in.
    2. Open chat link.
    3. Locate textbox element in chat window. Pass message string. Hit enter to send
    4. Locate attachment element in chat window. Pass local file path.
    5. Locate textbox element in image preview window. Pass message string. Hit enter to send.

## Using OpenAI in unavailable region (ex. Hong Kong)
Youtube tutorial (Chinese): https://www.youtube.com/watch?v=aI5-aUWUBPQ

Tutorial blog post (Chinese): https://bigfang.vip/openai/

Virtual SMS Indonesian number ~US$2: https://sms-activate.org/cn/getNumber

Privado Free Vpn: https://privadovpn.com/

## Project Story
👩🏻‍💻 2023 mid-Jan, I started training to become a Python for Data Science instructor at Preface. One of the projects in the teaching module is to create a program that sends WhatsApp messages using Selenium. 

🧧 As Lunar New Year was approaching, I was inspired to take the exercise to real-life application. 

💻 I decided to spice things up by incorporating OpenAI’s GPT3 NLP model to generate customised greetings, and DALL-E to create corresponding festive images. 

💡 Frankly speaking, the program is not the most practical (and not cost-efficient🤓), but I had a lot of fun along the journey of creative brainstorming and problem solving in building a product.

😂 Given how terrible the DALL•E images are, this mini project has become more of a meme project. I died laughing seeing the sent images when Selenium was running the message automation.

## Project Output
Created 120 unique text greetings and 120 unique festive images. API requests costed US$2. Overall, in trial runs plus launch run, API requests costed US$5.

Sending 120 text + image WhatsApp messages using Selenium took 1 hour.

### Painpoint
1. DALL•E image link expires in 1 hour after creation. It must be downloaded immediately.
2. Selenium.driver.send.keys() does not support emojis. There is a function to work around the limitation with JavaScript.
(to be continued)
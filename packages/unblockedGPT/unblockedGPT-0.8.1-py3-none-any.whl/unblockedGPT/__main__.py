import os
from unblockedGPT.typeresponse import Typeinator
from unblockedGPT.auth import Database
import openai
import time
def run():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app_path = os.path.join(dir_path, 'app.py')
    os.system(f'streamlit run {app_path}')

def type():
    while True:
        print("Enter the text you want to type (end with a line saying 'END'):")
        text = ""
        end_flag = False
        while not end_flag:
            line = input("")
            if line == "END":
                end_flag = True
            else:
                text += line + "\n"
        print("Starting in 5 seconds...")
        time.sleep(5)
        typeinator = Typeinator()

        typeinator.type(text)
def typeGPT():
    while True:
        #print selected model
        print("")
        model_selection = input("Selected model (1)gpt3.5 or (2)gpt.4\nEnter 1 or 2:")
        if model_selection != "1" and model_selection != "2":
            print("Invalid selection")
            continue

        prompt = input("Enter the prompt to be typed:")
        openai_api_key = Database.get_instance().get_settings(0)
        openai.api_key = openai_api_key
        try:
            response = openai.ChatCompletion.create(
            model=model_selection,
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )
            chatbot_response = response['choices'][0]['message']['content'].strip()
        except:
            print("run chat and update API key")
            continue
        if chatbot_response != "":
            print(chatbot_response)
            
            if input("Type this? (y/n)") == "y":
                print("Starting in 5 seconds...")
                time.sleep(5)
                typeinator = Typeinator()
                typeinator.type(chatbot_response)
            else:
                print("Not typing")


if __name__ == '__main__':
    type()
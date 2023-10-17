import streamlit as st
import requests
import openai
from unblockedGPT.rephrase import rephrase_2
from unblockedGPT.auth import Database
from unblockedGPT.detection import ai_detection, ai_detection_2
from unblockedGPT.typeresponse import Typeinator
import time


# Decrypted API keys
auth = Database.get_instance()
OPENAI_API_KEY_DEFAULT = auth.get_settings(0)
STEALTHGPT_API_KEY_DEFAULT = auth.get_settings(4)
GPTZERO_API_KEY_DEFAULT = auth.get_settings(5)

# Placeholder for special password
SPECIAL_PASSWORD = 'klfasdjf94305$'



# Obtain API keys from the user (or use the defaults)
#openai_api_key = st.text_input("OpenAI Api Key", type="password")
#stealthgpt_api_key = st.text_input("Rephrasing Key", type="password")
#gptzero_api_key = st.text_input("Detection Key", type="password")
#orginality = st.text_input("Originality Key", type="password")
keys = [st.text_input(auth.key_lable(i), type="password") for i in auth.index]
if st.button('Save Keys'):
    for i in range(len(keys)):
        if keys[i] != '' and keys[i] != None:
            auth.set_settings(i, keys[i])
            keys[i] = ''
    st.write("Keys Saved")
        

# Check if user entered the special password for any key
#if openai_api_key == SPECIAL_PASSWORD:
openai_api_key = OPENAI_API_KEY_DEFAULT
#if stealthgpt_api_key == SPECIAL_PASSWORD:
stealthgpt_api_key = STEALTHGPT_API_KEY_DEFAULT
#if gptzero_api_key == SPECIAL_PASSWORD:
gptzero_api_key = GPTZERO_API_KEY_DEFAULT

# Initialize session_state if not already initialized
if 'position' not in st.session_state:
    st.session_state.position = -1  # Position of the current display in history

if 'rephrase_list' not in st.session_state:
    st.session_state.rephrase_list = []
    st.session_state.submitFlag = True
# Title
st.title('Totally Not ChatGPT')

# Model selection
model_selection = st.selectbox('Select the model:', ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4'])

if st.button('Clear Conversation'):
    st.session_state.position = -1
    st.session_state.conversation = []
    st.session_state.ai_detection_score = ["N/A", "N/A"]

# User input
user_input = st.text_area('You: ', height=200)
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Load conversation and rephrase_list based on the current position
if st.session_state.position == -1:
    st.session_state.conversation = []
    st.session_state.ai_detection_score = ["N/A", "N/A"]


# Submit button
if st.button('Submit'):
    st.session_state.submitFlag = True

if user_input and st.session_state.submitFlag:
    st.session_state.submitFlag = False
    if openai_api_key != False:
        openai.api_key = openai_api_key
        try: 
            response = openai.ChatCompletion.create(
            model=model_selection,
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]
        )
            chatbot_response = response['choices'][0]['message']['content'].strip()
            st.session_state.conversation.insert(0, {"user-input":user_input, "response": chatbot_response, "type": 1})
            st.session_state.ai_detection_score[0] = ai_detection( chatbot_response, auth)
            st.session_state.ai_detection_score[1] = ai_detection_2( chatbot_response, auth)
            st.session_state.position += 1
        except:
            st.write("Invalid API Key")
    else:
        st.write("Please enter an API Key")
        

        
# Rephrase button
if st.button('Rephrase Text'):
    if stealthgpt_api_key != False:
        headers = {'api-token': stealthgpt_api_key, 'Content-Type': 'application/json'}
        data = {'prompt': st.session_state.conversation[0]['response'], 'rephrase': True}
        response = requests.post('https://stealthgpt.ai/api/stealthify', headers=headers, json=data)
        if response.status_code == 200:
            rephrased_text = response.json()
            rephrased_text = rephrased_text['result']
            st.session_state.conversation.insert(0, {"user-input":'Rephrase Text 1', "response": rephrased_text, "type": 0})
            st.session_state.ai_detection_score[0] = ai_detection( rephrased_text, auth)
            st.session_state.ai_detection_score[1] = ai_detection_2( rephrased_text, auth)
        elif response.status_code == 401:
            st.session_state.conversation.insert(0, {"user-input":'Rephrase Text 1', "response": 'Invalid API Key', "type": 0})
            st.session_state.ai_detection_score[0] = "N/A"
            st.session_state.ai_detection_score[1] = "N/A"
        else:
            st.session_state.conversation.insert(0, {"user-input":'Rephrase Text 1', "response": 'Could not rephrase', "type": 0})
            st.session_state.ai_detection_score[0] = "N/A"
            st.session_state.ai_detection_score[1] = "N/A"
    else:
        st.write("Please enter stealth API Key")

# Rephrase button 2
if st.button('Rephrase Text 2'):
    response =  rephrase_2(st.session_state.conversation[0]['response'])
    st.session_state.conversation.insert(0, {"user-input":'Rephrase Text 2',"response":response['msg'], "type": 0})
    if response['status']:
        st.session_state.ai_detection_score[0] = ai_detection( response['msg'], auth)
        st.session_state.ai_detection_score[1] = ai_detection_2( response['msg'], auth)
    else:
        st.session_state.ai_detection_score[0] = "N/A"
        st.session_state.ai_detection_score[1] = "N/A"



# Type response
if st.button('Type Response'):
    #type the most recent, using keyboard inputs
    typeinator = Typeinator()
    time.sleep(5)
    typeinator.type(st.session_state.conversation[0]['response'])

st.write('Timed Typing')
minutes = st.number_input('Minutes to type response', min_value=0, max_value=1000, step=1)
if st.button('Timed Type Response') and minutes != 0:
    #type the most recent, using timed typing
    st.write('Typing in 5 seconds...')
    time.sleep(5)
    typeinator = Typeinator()
    typeinator.timeToType(st.session_state.conversation[0]['response'], minutes)
    minutes = 0


# Display conversation and rephrases
st.write(f'<div style="text-align: right; color: blue;">AI Detection Score: {st.session_state.ai_detection_score[0]}</div>', unsafe_allow_html=True )
st.write(f'<div style="text-align: right; color: blue;">AI Detection Score 2: {st.session_state.ai_detection_score[1]}</div>', unsafe_allow_html=True)
st.write("### Conversation:")
for turn in st.session_state.conversation:
    if turn["type"] == 1: 
        st.write(f'<div style="color: blue; background-color:{ "#E6EFFF" if turn["type"] == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>You:</b> {turn["user-input"]}</div>', unsafe_allow_html=True)
    st.write(f'<div style="color: black; background-color:{ "#DCDCDC " if turn["type"] == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>{"ChatGPT: " if turn["type"] == 1 else "Rephrase: "}</b> {turn["response"]}</div>', unsafe_allow_html=True)
    
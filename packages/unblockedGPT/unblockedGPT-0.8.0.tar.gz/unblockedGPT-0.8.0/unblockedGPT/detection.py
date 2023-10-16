from unblockedGPT.auth import Database
import requests
import json
from typing import Union
def ai_detection(chatbot_response: str, auth: Database) -> str:
    """
        This function detects the AI generated text using the GPTZero API.
    """
    gptzero_api_key = auth.get_settings(5)
    if gptzero_api_key == False:
        return "Please enter GPTZero API Key"
    gptzero_response = requests.post(
        "https://api.gptzero.me/v2/predict/text",
        headers={"x-api-key": gptzero_api_key},
        json={"document": chatbot_response}
    )
    if gptzero_response.status_code == 401:
        return "Invalid API Key"
    gptzero_response = gptzero_response.json()
    if 'error' in gptzero_response:
        return "N/A"
    if 'documents' in gptzero_response:
        return str(int(gptzero_response['documents'][0]['completely_generated_prob'] * 100))+'%'
    else:
        return "N/A"

def ai_detection_2(chatbot_response: str, auth: Database) -> str:
    """
        This function detects the AI generated text using the Originality API.
    """
    api_key = auth.get_settings(6)
    if api_key == False:
        return "Please enter originality API Key"
    url = "https://api.originality.ai/api/v1/scan/ai"
    headers = {
        "Accept": "application/json",
        "X-OAI-API-KEY": api_key
    }
    content = {
        "title": "test title",
        "content": chatbot_response,
    }
    response = requests.post(url, headers=headers, json=content)
    if response.status_code == 422:
        return "Invalid API Key"

    response_dict = json.loads(response.text)
    if 'error' in response_dict:
        return "N/A"
    else:
        return str(int(response_dict['blocks'][0]['result']['fake']))+"%"


if __name__ == "__main__":
    auth = Database.get_instance()
    print(ai_detection_2( "testing testing testing!", auth))


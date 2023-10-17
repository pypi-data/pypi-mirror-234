import requests
from unblockedGPT.auth import Database
# Define the base URL of your FastAPI-based API
base_url = "https://gpthero.dev/api/"

# Define the essay and API keys
#essay = "The man in space has always been a symbol of human curiosity, exploration, and innovation. Since Yuri Gagarin's historic journey aboard Vostok 1 in 1961, when he became the first human to venture into the cosmos, space exploration has captured the imagination of people worldwide. The allure of the unknown, the breathtaking views of our planet from orbit, and the quest to understand the mysteries of the universe have driven countless astronauts to embark on remarkable missions to space stations, the moon, and even distant planets. With each mission, we not only expand our scientific knowledge but also reaffirm our indomitable spirit of adventure and the boundless possibilities that await us beyond the Earth's atmosphere. The man in space continues to be a symbol of humanity's relentless pursuit of discovery and the remarkable achievements that come when we dare to reach for the stars."




# if you wan to pass auth_token then use this

# request_payload = {
#     "prompt": {
#         "essay": essay,
#         "openaiapikey": openai_api_key,
#         "prowritingaidapikey": prowritingaid_api_key,
#         "approach": "Creative",
#         "context": True,
#         "randomness": 5,
#         "tone": "newspaper",
#         "difficulty": "easy to understand, very common",
#         "additional_adjectives": "concise and precise, to the point",
#         "model": "GPT-3",
#     },
#     "user": {"auth_token": "string"},
# }


def rephrase_2(essay: str) -> dict:
    """
        This function rephrases the result using the 2nd rephasing API.
        returns a dictionary with status bool and msg str
    """
    # Define the request payload
    auth = Database.get_instance()
    openai_api_key = auth.get_settings(0)
    prowritingaid_api_key = auth.get_settings(1)
    if openai_api_key == False:
        return {'status':False, 'msg':"Please enter an openAI API Key"}
    if prowritingaid_api_key == False:
        return {'status':False, 'msg':"Please enter a prowritingaid API Key"}
    request_payload = {
        "prompt": {
            "essay": essay,
            "openaiapikey": openai_api_key,
            "prowritingaidapikey": prowritingaid_api_key,
            "approach": "Creative",
            "context": True,
            "randomness": 5,
            "tone": "newspaper",
            "difficulty": "easy to understand, very common",
            "additional_adjectives": "concise and precise, to the point",
            "model": "GPT-3",
        },
        "user": {"username": auth.get_settings(2), "password": auth.get_settings(3)},
    }

    # Send a POST request to the /rephrase_essay endpoint
    response = requests.post(f"{base_url}/rephrase_essay", json=request_payload)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        rephrased_essay = response.json()
        rephrased_essay = rephrased_essay['rephrased_essay']
        return {'status':True, 'msg':rephrased_essay}
    elif response.status_code == 401:
        # Invalid API key
        return {'status':False, 'msg':"Invalid API key"}
        
    else:
        # Request failed
        error_message = response.json()

        return {'status':False, 'msg':f"Failed to rephrase essay\n {error_message['detail'][0]['msg']}"}

if __name__ == "__main__":
    essay = "Tz."
    print(rephrase_2(essay))
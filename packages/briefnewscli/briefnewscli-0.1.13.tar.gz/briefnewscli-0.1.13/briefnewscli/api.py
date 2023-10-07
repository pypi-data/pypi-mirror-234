# api.py API integration functions
import requests
import os
from decouple import Config, RepositoryEnv

# Specify the full path to the .env file
#DOTENV_FILE = os.environ.get("DOTENV_FILE", "../.env")
#env_config = Config(RepositoryEnv('../.env'))
#env_config = Config('../.env')

# Accessing variables from the .env file
#api_key = env_config.get('NYT_API_KEY', default='')
#base_url = env_config.get('NYT_API_TopStories_URL', default='')
api_key = "Y55UQABsAloXXpDVtA1GfdU82Ed2sIz2"
base_url = "https://api.nytimes.com/svc/topstories/v2/home.json"

def fetch_top_stories():
    
    # Request parameters
    params = {
        "api-key": api_key
    }

    try:
        # Make the GET request to the API
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and return the list of top stories
            top_stories = data.get("results", [])
            return top_stories
        else:
            # Handle errors (e.g., print an error message)
            print(f"Error: Unable to fetch top stories. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Handle exceptions (e.g., network issues)
        print(f"An error occurred: {str(e)}")
        return None

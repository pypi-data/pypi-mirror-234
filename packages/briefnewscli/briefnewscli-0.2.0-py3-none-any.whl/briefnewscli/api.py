# api.py API integration functions
import requests
from decouple import config, UndefinedValueError

try:
    # Accessing variables from the .env file
    api_key = config('NYT_API_KEY')
    base_url = "https://api.nytimes.com/svc/topstories/v2/home.json"
except UndefinedValueError:
    # Handle the case where the environment variable is not defined
    print("NYT_API_KEY environment variable is not defined.")

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

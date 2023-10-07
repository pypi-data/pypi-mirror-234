from decouple import config

# Load configuration based on the DEPLOYMENT_ENV environment variable
DEPLOYMENT_ENV = config("DEPLOYMENT_ENV")

if DEPLOYMENT_ENV == "development":
    # Load development environment configuration from the .env file
    print("***Development Env***")
    NYTimes_API_KEY = config("NYTimes_API_KEY")
    NYTimes_API_SECRET = config("NYTimes_API_SECRET")
    NYTimes_API_TopStories_URL = "https://api.nytimes.com/svc/topstories/v2/home.json"
elif DEPLOYMENT_ENV == "production":
    # Load production environment configuration
    NYTimes_API_KEY = config("NYTimes_API_KEY")
    NYTimes_API_SECRET = config("NYTimes_API_SECRET")
    NYTimes_API_TopStories_URL = "https://api.nytimes.com/svc/topstories/v2/home.json"
else:
    raise ValueError("Invalid DEPLOYMENT_ENV value. Use 'development' or 'production'.")
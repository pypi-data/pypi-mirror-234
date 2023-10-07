# cli.py Typer-based CLI entry point
import typer
from decouple import config
from .api import fetch_top_stories 
from transformers import pipeline, AutoTokenizer

# Specify the path to the .env file (adjust the path as needed)
config = Config()
config.read('/.env')

app = typer.Typer()

@app.command()
def dummy(arg1: str, arg2: int):
    """
    My CLI command description.
    """
    typer.echo(f"Argument 1: {arg1}")
    typer.echo(f"Argument 2: {arg2}")

@app.command()
def top_stories():
    """
    Fetch and display top stories from the New York Times API.
    """
    # Accessing variables from the .env file
    api_key = config.get('NYTimes_API_KEY', default='')

    # Check if the NYTimes_API_KEY is available
    if not api_key:
        typer.echo("Error: New York Times API key is missing. Please set it in your config.py file.")
        return

    # Fetch top stories
    top_stories_data = fetch_top_stories()

    if top_stories_data:
        typer.echo("Top Stories:")
        for i, story in enumerate(top_stories_data, start=1):
            typer.echo(f"{i}. {story['title']}")
    else:
        typer.echo("Failed to fetch top stories. Check your API key and network connection.")

@app.command()
def brief():
    """
    Summarize news articles fetched from NYT Top Stories API.
    """
    typer.echo("Fetching top stories from New York Times...")
    # Fetch top stories
    top_stories_data = fetch_top_stories()

    if top_stories_data:

        num_news_processed = len(top_stories_data)
        typer.echo(f"Analyzing {num_news_processed} news articles...")
        combined_content = ""
        for story in top_stories_data:
            # Extract the abstract (or use a different field as needed)
            article_text = story.get("abstract", "")
            combined_content += article_text + "\n"

        typer.echo("Loading AI engine...")
        # Set the cache directory to the path defined in the Docker container
        cache_dir = "/root/.cache/huggingface/transformers"

        # Specify the model name and revision
        model_name = "facebook/bart-large-cnn"  # Replace with the desired model name
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        
        # Initialize the Huggingface summarization pipeline with model and revision
        summarizer = pipeline("summarization", model=model_name, tokenizer=tokenizer)

        # Summarize the article
        typer.echo(f"Using AI engine to summarizing {num_news_processed} news articles...")
        summarized_text = summarizer(combined_content, max_length=350, min_length=120, do_sample=False)
        
        typer.echo("\n***Here it is your brief for today:***\n")
        typer.echo(summarized_text[0]['summary_text'])
    else:
        typer.echo("Failed to fetch top stories for summarization. Check your API key and network connection.")



@app.callback()
def main(ctx: typer.Context):
    """
    Non-commercial use. A CLI based on Python and Typer. 
    Connects to trusted news sources like the New York Times APIs, fetch today's news, 
    and then uses Hugging Face AI tools to summarize the news in a simple paragraph.
    """

if __name__ == "__main__":
    app()
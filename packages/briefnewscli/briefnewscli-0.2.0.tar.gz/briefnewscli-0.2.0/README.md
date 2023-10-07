# briefnewsCLI
Non-commercial use. briefnewsCLI is a Python command-line tool for fetching and summarizing news articles from various sources. It simplifies the process of staying informed by providing quick access to summarized news articles by AI in your terminal.

## Features

- Fetch and display top news stories.
- Summarize news articles for quick insights.
- Customizable summarization options.
- Easy-to-use and interactive command-line interface.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install briefnewsCLI via pip. Ensure you have Python 3.7 or higher installed.

```bash
pip install briefnewscli
```

## Configuration

To use briefnewsCLI, you need to configure the following environment variables:

- `NYT_API_KEY`: Your New York Times API key for authentication.

Please make sure to set these environment variables in your local environment before using briefnewsCLI.


## Usage

After installation, you can use briefnewsCLI by running the `brief-news` command in your terminal:

```bash
briefnewscli headlines
```

To summarize today's top stories, use:

```bash
briefnewscli brief
```

For more details and options, refer to the Commands section below.

## Commands

`headlines`
Fetch and display the top news stories from various sources.

```bash
briefnewscli headlines
```

`brief`
Summarize news articles for quick insights. Customize summarization options as needed.

```bash
briefnewscli brief
```
For additional commands and options, run `briefnewscli --help`.

## Contributing
Contributions to BriefNewsCLI are welcome! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License
This project is licensed under the Creative Commons Legal Code.
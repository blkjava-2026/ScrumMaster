# ScrumMaster Discord Bot

An AI-powered Discord bot that answers Agile and Scrum questions with expert guidance. The bot uses OpenAI's API to provide professional, concise responses from a Scrum Master perspective.

## Features

- **Scrum Expert Responses**: Answers questions about Agile/Scrum practices, roles, events, and artifacts
- **Professional Tone**: Delivers clear, confident explanations with actionable next steps
- **Discord Integration**: Seamlessly handles Discord commands and messages
- **Smart Message Chunking**: Automatically splits responses to respect Discord's 2000-character limit
- **Configurable AI Model**: Uses gpt-4o-mini by default; easily configurable via environment variables

## Commands

- `$hello` - Get a greeting and command help
- `$question <your question>` - Ask the ScrumMaster about Agile/Scrum topics

## Setup

### Requirements

- Python 3.8+
- Discord Bot Token
- OpenAI API Key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ScrumMaster
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your credentials:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o-mini  # optional, defaults to gpt-4o-mini
   ```

4. Run the bot:
   ```bash
   python Bot.py
   ```

## Environment Variables

- `DISCORD_TOKEN` (required): Your Discord bot token
- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): The OpenAI model to use (default: `gpt-4o-mini`)

## Adding the Bot to Your Discord Server

1. Create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Copy your bot token and add it to `.env`
3. Generate an invite link with these scopes: `bot` and permissions: `Send Messages`, `Read Messages`
4. Use the invite link to add the bot to your server

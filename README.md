# Ripper Bot

A Discord bot that extracts text from images using OCR, processes it with AI, and creates formatted text files.

## Description

Ripper Bot is a powerful Discord utility that can process image attachments from Discord messages, apply OCR (Optical Character Recognition) to extract text content, enhance the text using AI formatting via Google's Gemini API, and return the processed content as downloadable text files.

## Features

- OCR Image Processing: Extract text from PNG, JPG, and JPEG images
- AI-Enhanced Text Formatting: Utilizes Google's Gemini API to improve text formatting and readability
- PDF Generation: Creates formatted PDF documents from extracted text
- Discord Slash Commands: Easy to use with Discord's integrated command system
- Role-Based Permissions: Commands require moderator permissions for security

## Usage

The bot provides slash commands for interaction:

1. `/rip` slash command extracts text from images in a specified message.

```sh
/rip message_id:<message ID> filename:<optional output filename>
```

- `message_id`: The ID of the Discord message containing images
- `filename`: (Optional) Custom name for the output files (default: "output")

2. `/jack` slash command converts text files to EPUB format.

```sh
/jack message_id:<message ID>
```

- `message_id`: The ID of the Discord message containing a .txt file.

## Installation

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Tesseract OCR installed on your system
- Discord Bot Token
- Google Gemini API Key

### Setup

1. Clone the repository:

```sh
git clone https://github.com/bakayu/ripper-bot.git
cd ripper-bot
```

2. Install dependencies using Poetry:

```sh
poetry install
```

3. Install Tesseract OCR:

For Ubuntu/Debian:

```sh
sudo apt update
sudo apt install tesseract-ocr
```

For other platforms, visit the Tesseract documentation
Create an environment file:

5. Edit the .env file with your credentials:

```sh
DISCORD_TOKEN = "your-discord-bot-token"
GEMINI_API_KEY = "your-gemini-api-key"
```

6. Make sure the NotoSans font is installed or update the path in [pdf_builder.py](./main/utils/pdf_builder.py)

### Running as a Service with PM2

PM2 is used to manage the bot as a persistent service:

1. Install PM2 if not already installed:

```sh
npm install -g pm2
```

2. Make the run script executable:

```sh
chmox +x run.sh
```

3. Start the bot with PM2:

```sh
pm2 start ecosystem.config.js
```

4. View logs:

```sh
pm2 logs rbot
```

5. Setup PM2 to start on system boot:

```sh
pm2 startup
pm2 save
```

6. Other useful PM2 commands:

```sh
pm2 stop rbot       # stop the bot
pm2 restart rbot    # restart the bot
pm2 status          # check status of the bot
```

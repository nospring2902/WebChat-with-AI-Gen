

# AI-Powered Web Chat Application

## Introduction

This project is a web chat application that integrates the Gemini Flash 1.5 AI model. The application offers multilingual chat translation, chat summaries, and word explanations, making communication seamless and accessible for users in English, Japanese, and Vietnamese.

## Features

- **Automatic Chat Translation:** Real-time translation of chat messages in English, Japanese, and Vietnamese.
- **Chat Summary:** Automatically generates a summary of the chat conversation.
- **Word Explanation:** Provides detailed explanations of words in the chat, enhancing understanding and language learning.

## Demo

You can try out the web chat application [https://techbridgeofasap.pythonanywhere.com/](#).

## Installation

### Prerequisites

- Python 3.x
- Django 4.x
- Other dependencies as listed in `requirements.txt`

### Steps to Install

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python manage.py migrate
    ```

4. Run the development server:
    ```bash
    python manage.py runserver
    ```

5. Access the application in your browser at `http://localhost:8000`.

## Usage

1. **Login/Register:** Users can register or log in using their credentials.
2. **Start Chatting:** Select a language and start chatting. Messages will be automatically translated based on the selected language.
3. **Chat Summary:** Click on the button to generate a summary of the ongoing conversation.
4. **Word Explanation:** Hover over on message to see its explanation.


## Contributing

We welcome contributions to enhance the features and performance of this application. Please feel free to submit a pull request or open an issue.


---


# Quotes Recommendation Chatbot (Rasa 3.x)

This is a Rasa 3.x conversational AI chatbot that provides users with various types of quotes based on their mood or request.

## Architecture Overview
The bot handles simple, single-turn interactions using **Rules**. There are NO complex dialogue paths (stories) currently needed, keeping the bot fast and predictable.

### Capabilities (Intents)
- `greet`: The bot greets the user and asks what quote they want.
- `motivation_quote`: The bot triggers a custom action to return a motivational quote.
- `love_quote`: The bot triggers a custom action to return a love quote.
- `success_quote`: The bot triggers a custom action to return a success quote.
- `funny_quote`: The bot triggers a custom action to return a funny quote.
- `thank_you`: The bot says "You're welcome."
- `goodbye`: The bot says goodbye.
- `nlu_fallback`: If the bot doesn't understand the user, it gracefully explains its capabilities.

### Custom Actions
The actual quotes are returned by a Python Action Server (`actions/actions.py`). This allows the quotes to be dynamic, randomized, or eventually fetched from an external API.

## Installation

1. Prepare your Python environment (Python 3.8 - 3.10 recommended).
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies (assuming you have a requirements file or just `pip install rasa`):
   ```bash
   pip install rasa
   ```

## Running the Chatbot with UI

You need three terminal windows open simultaneously:

**Terminal 1 (Action Server):**
```bash
source venv/bin/activate
rasa run actions
```

**Terminal 2 (Rasa API Server):**
```bash
source venv/bin/activate
rasa run --enable-api
```

**Terminal 3 (Streamlit UI):**
First, ensure the UI dependencies are installed:
```bash
pip install -r ui/requirements_ui.txt
```
Then run the UI:
```bash
streamlit run ui/chat_ui.py
```

## Example Conversation
```
User: Hello there
Bot: Hello! What type of quote do you need today?

User: Make me laugh!
Bot: I am not lazy, I am on energy saving mode.

User: Thank you
Bot: You're welcome!

User: Bye
Bot: Goodbye! Have a great day.
```

## Testing
To test that your latest updates haven't broken the conversational flows:
```bash
source venv/bin/activate
rasa test
```

## Project Structure
- `data/nlu.yml`: Contains the training data for what users might say.
- `data/rules.yml`: Contains the 1-to-1 mapping of intents to custom actions/responses.
- `actions/actions.py`: The Python code that selects and returns the actual quotes.
- `domain.yml`: The "universe" of the bot (all intents, actions, and text responses).
- `endpoints.yml`: Configuration connecting the Rasa bot to the action server.
- `tests/test_stories.yml`: The automated test conversations.

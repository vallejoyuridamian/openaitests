# OpenAI Voice Assistant

This is a simple voice assistant application built using Python and various libraries. It listens for a wake word, allows you to ask questions using voice or text input, and responds with answers from OpenAI's GPT-3.5-turbo model.

## Features
- Voice recognition to detect the wake word and commands.
- Text input to query ChatGPT.
- Text-to-speech for responses.
- Customizable parameters for personalization.

### Prerequisites
- Python 3.7 or higher
- OpenAI API Key
- Required Python libraries:
  - openai
  - customtkinter
  - gtts
  - pygame
  - speech_recognition

For this to work, you need an OpenAI api key and you need to set it as an environment variable (OPENAI_API_KEY='your-api-key')

### Customization

You can change the parameters in the script to customize the behavior and appearance:

```python
role = "You are a helpful assistant"
label_text = "ChatGPT Assistant"
button_text = "Ask"
button_speak_text = "Speak"
wake_word = "Assistant"
lang_audio_in = "en-US"
lang_audio_out = "en"
greeting = "Hello, how can I help you?"
chat_gpt_model = "gpt-3.5-turbo"
```

Feel free to modify these variables to choose the language, context, and other settings that suit your needs.

## License

You can use it as you please, make money from it, whatever, I don't care. I would be happy to know that it was useful to someone.

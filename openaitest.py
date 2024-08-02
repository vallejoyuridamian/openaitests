import openai
import customtkinter as ctk
from gtts import gTTS
import pygame
from io import BytesIO
import speech_recognition as sr
import threading

# Feel free to change these paramters to customize it
role = "Sos un chatgpt uruguayo"
label_text = "ChatGPT uruguayo"
button_text = "Pregunte nomás"
button_speak_text = "Speak"
wake_word = "Compa"
lang_audio_in = "es-US"
lang_audio_out = "es"
greeting = "Mande patrón"
chat_gpt_model = "gpt-3.5-turbo"

chat_log = [{"role": "system", "content": role}]
class MyGUI:
    def __init__(self):
        self.root = ctk.CTk()

        self.root._set_appearance_mode("dark")
        self.root.geometry("1000x600")

        self.label = ctk.CTkLabel(self.root, text=label_text, bg_color="transparent")
        self.label.pack(padx=10, pady=10)

        self.textbox = ctk.CTkTextbox(self.root, width=600)
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.button = ctk.CTkButton(self.root, text=button_text, command = self.querychatgpt)
        self.button.pack(padx=10, pady=10)

        self.button_speak = ctk.CTkButton(self.root, text=button_speak_text, command=self.speak)
        self.button_speak.pack(padx=10, pady=10)

        self.anstextbox = ctk.CTkTextbox(self.root, width=600)
        self.anstextbox.pack(padx=10, pady=10)

        pygame.mixer.init()

        self.recognizer = sr.Recognizer()

        self.listening_thread = None
        self.continuous_listening = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.start_continuous_listening()
        self.root.mainloop()

    def listen_for_wake_word(self):
        while self.continuous_listening:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = self.recognizer.listen(source, timeout=5)

            try:
                text = self.recognizer.recognize_google(audio, language=lang_audio_in)
                print("Heard:", text)

                if wake_word.lower() in text.lower():
                    print("Wake word detected. Listening for your command...")
                    self.play_text_to_speech(greeting)
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    self.continuous_listening = False
                    self.speak()
                    break

            except sr.UnknownValueError:
                print("No speech detected")
            except sr.RequestError as e:
                print(f"Error in speech recognition; {e}")

    def start_continuous_listening(self):
        self.continuous_listening = True
        self.listening_thread = threading.Thread(target=self.listen_for_wake_word)
        self.listening_thread.start()

    def stop_continuous_listening(self):
        self.continuous_listening = False

    def speak(self):
        self.stop_continuous_listening()

        with sr.Microphone() as source:
            print("Speak now...")
            audio = self.recognizer.listen(source, timeout=2)

        try:
            text = self.recognizer.recognize_google(audio, language=lang_audio_in)
            self.textbox.delete('1.0', ctk.END)
            self.textbox.insert("0.0", text)
            self.querychatgpt()
            self.start_continuous_listening()

        except sr.UnknownValueError:
            print("No speech detected")
            self.start_continuous_listening()
        except sr.RequestError as e:
           print(f"Error in speech recognition; {e}")

    def querychatgpt(self):
        client = openai.OpenAI()
        promt = self.textbox.get('1.0', ctk.END)
        self.anstextbox.delete('1.0', ctk.END)
        chat_log.append({"role": "user", "content": promt})
        response = client.chat.completions.create(
            model=chat_gpt_model,
            messages=chat_log,
            temperature=0.5,
            max_tokens=200,
            top_p=1
        )
        answer = response.choices[0].message.content
        chat_log.append({"role": "assistant", "content": answer})
        self.anstextbox.insert("0.0", answer)

        self.play_text_to_speech(answer)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def play_text_to_speech(self, text):

        tts = gTTS(text=text, lang=lang_audio_out, tld='us')
        speech_data = BytesIO()
        tts.write_to_fp(speech_data)
        speech_data.seek(0)

        pygame.mixer.music.load(speech_data)
        pygame.mixer.music.play()

    def shortcut(self, event):
        if event.keysym == "Return":
            self.querychatgpt()

    def on_closing(self):
        self.root.destroy()

MyGUI()
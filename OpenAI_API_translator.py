import os
import re
import threading
import openai
from tkinter import Tk, ttk, Text, Button, Label, StringVar, END, OptionMenu, messagebox
import tkinter.ttk as ttk

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
client = OpenAI(api_key=SECRET_KEY)

def split_text(input_text, limit=4096):
    sentences = re.split(r'(?<=[.!?])\s+', input_text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < limit:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def translate_text(chunks, target_lang="en", progress_bar=None):
    translations = []
    total_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Translate this text to {target_lang}: {chunk}"}
                ],
                max_tokens=1024
            )
            translation = response.choices[0].message.content.strip()
            translations.append(translation)
        except AttributeError as e:
            print(f"Failed to extract text from response: {e}")
            print(f"Response object: {response}")
            translations.append("[Translation error]")
        # Update the progress bar
        if progress_bar:
            progress_bar['value'] = 100 * (i + 1) / total_chunks
            root.update_idletasks()  # Force update of GUI
    return translations



def handle_translation():
    status_label.config(text="Processing...")
    input_text = text_input.get("1.0", END).strip()
    if not input_text:
        messagebox.showerror("Error", "Please enter some text.")
        status_label.config(text="")
        return
    target_lang = language_var.get().lower()
    progress_bar['value'] = 0  # Reset progress bar
    try:
        chunks = split_text(input_text)
        translations = translate_text(chunks, target_lang=target_lang, progress_bar=progress_bar)
        text_output.delete("1.0", END)
        text_output.insert("1.0", " ".join(translations))
        status_label.config(text="Translation complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="")
    progress_bar['value'] = 0  # Reset progress bar at the end


def run_translation():
    threading.Thread(target=handle_translation).start()

root = Tk()
root.title("Text Translator")

text_input = Text(root, height=10, width=50)
text_input.pack(pady=20)


language_var = StringVar(root)
language_var.set("English")  # default value
languages = ["Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian", "Burmese", "Catalan", "Cebuano", "Chinese", "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Finnish", "French", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole", "Hausa", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish", "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Nepali", "Norwegian", "Odia", "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Samoan", "Scottish Gaelic", "Serbian", "Shona", "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tongan", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"]
language_dropdown = OptionMenu(root, language_var, *languages)
language_dropdown.pack()

translate_button = Button(root, text="Translate Text", command=run_translation)
translate_button.pack(pady=10)

text_output = Text(root, height=10, width=50)
text_output.pack(pady=20)

status_label = Label(root, text="")
status_label.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
progress_bar.pack(pady=20)


root.mainloop()

This is a very simple little app that takes an input of pasted text and uses the openAI API to translate it into the language you choose from the dropdown list.
**You will need an OpenAI API account with sufficient funds. In the same directory as the app, create a file with the filename .env that includes this single line: SECRET_KEY = "YOUR_KEY_HERE". Replace YOUR_KEY_HERE with your OpenAI API secret key. You can find out how to obtain your key here: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key
A progress bar lets you know how the translation is progressing.
The translated text appears in the bottom window. You can copy and paste it from there, but you can't directly save the text within the app.
I find that it takes about 10 minutes to translate a book-length chunk of text, and it costs significantly less than $1.

I find this little app super useful for producing quick and dirty translations of academic articles written in languages other than English, but I'm sure there are lots of other possible uses too.

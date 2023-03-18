<span style="color: gray">
<h1>Voice chatbot application ChatGPT</h1>
</span>

Evolving chatbot program using OpenAI's GPT-4 API

<span style="color: gray">
<h2>Installation</h2>
</span>

As a development project, 'installation' consists of pulling down the source code and installing the required dependencies. That is best done within a Python virtual
environment, so as to not possibly conflicting with other Python packages already on one's system globally. This is the recommended practice for any such
project.

Use at your risk. ;) And if you do dare ;), and encounter any issue/bug/suggestion, feel free to open an issue. I'd appreciate the feedback.

1) Clone this repository, and change to the new directory. (You will need to have git and LFS installed.)

```
git clone https://github.com/karencfisher/ChatGPT-chatbot.git
cd ChatGPT-chatbot
```

2) Create a Python virtual environment and activate it, e.g., 

```
python -m venv chat_env
chat_env\scripts\activate
```

3) Install dependencies using the requirements.txt file, e.g.,

```
pip -r requirements.txt
```

4) If you do not already have an account to use the OpenAI API, you will need to do so. You 
will initially have $18 credit for usage, which is good for 3 months. If you have used the
free credits or they have expired after 3 months (which ever happens first), you will need to 
set up a paid account. 

Also, GPT-4 is in limited beta, so one needs to get on the waitlist and, well, wait. It only
took me a couple of days, but I might have received priority as I have been working on these
projects.

https://openai.com/api/

5) Create a secret key to access the API, and copy it to paste in the next step

https://beta.openai.com/account/api-keys

6) Create an .env file in the same directory, and in it include the line:

```
SECRET_KEY = '<your secret key>'
```

<span style="color: gray">
<h2>Configuration</h2>
</span>

There are four configuration files:

gpt4_config.json:

Parameters for the language model.

```
{"model": "gpt-4",
 "temperature": 0.1,
 "top_p": 1,
 "n": 1,
 "presence_penalty": 0,
 "frequency_penalty": 0,
 "max_tokens": 64}
 ```

vosk_config.json: settings for vosk speech recognition. These have technical details like bit rate and buffer sizes, and likely
won't need to be change often. But they are exposed for the brave.

```
{"model": "vosk-model-small-en-us-0.15",
"chunk": 4096,
"channels": 1,
"rate": 16000}
```

voice.json: here is where you may be able to select the voice to be used. Currently, it uses 
a voice provided by Windows 10. On other platforms one needs to find the voice they
prefer: see the pyttsx3 documentation linked above.

```
{"voice": "Microsoft Zira Desktop - English (United States)", 
 "rate": 130}
 ```

<span style="color: gray">
<h2>Use</h2>
</span>

Run

```
python GPT4Chat.py
```

The program will initialize the speech rocognition and synthesis modules, and GPT-4 will greet you. Talk with GPT-4. Say "goodbye" to exit.
A transcription of your conversation will be in the log files, labeled by date and time.

If you prefer not to talk, there is an option to specify a 'novoice' command line argument. Conversation will then be via text on the
terminal.

```
python GPT4Chat.py novoice
```



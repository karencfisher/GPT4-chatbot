<span style="color: gray">
<h1>Voice chatbot application ChatGPT</h1>
</span>

Evolving chatbot program using OpenAI's ChatGPT API (gpt-3.5-turbo)

<span style="color: gray">
<h2>Installation</h2>
</span>

As a development project, 'installation' consists of pulling down the source code and installing the required dependencies. That is best done within a Python virtual
environment, so as to not possibly conflicting with other Python packages already on one's system globally. This is the recommended practice for any such
project.

Use at your risk. ;) And if you do dare ;), and encounter any issue/bug/suggestion, feel free to open an issue. I'd appreciate the feedback.

1) Clone this repository, and change to the new directory. (You will need to have git and LFS installed.)

```
git clone https://github.com/karencfisher/simple-chat.git
cd simple-chat
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
set up a paid account. Text generation, for the largest GPT-3 model DaVinci-0003,
costs $0.02/thousand tokens (about 750 words on average). (Using ChatGPT will only set you
back $0.002/thousand tokens, one tenth the cost of using the best GPT-3 model.)

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

chatgpt_config.json:


vosk_config.json: settings for vosk speech recognition. These have technical details like bit rate and buffer sizes, and likely
won't need to be change often. But they are exposed for the brave.

voice.json: here is where you may be able to select the voice to be used. Currently, it uses 
a voice provided by Windows 10. On other platforms one needs to find the voice they
prefer: see the pyttsx3 documentation linked above.

<span style="color: gray">
<h2>Maintaining context</h2>
</span>

In order to maintain some degree of conitnuity, we will prompt the model with a
rolling conversation, in this form:

PRETEXT
CONTEXT

<span style="color: gray">
PRETEXT:
</span>

The <span style="color: gray">PRETEXT</span> defines a role or character for the conversational agent, or other
wise define it's purpose. It is defined in a text file in the working directory with the file name of 'pretext.txt' ('chat_pretext.txt' for ChatGPT). If one wants to omit a pretext (using the AI essentially out of the box), the file can simply be omitted.

The <span style="color: gray">CONTEXT</span> then is the rolling, recent conversation. 

The two portions of text are concatenated becoming the next prompt to the model.
<b>The total combination of pretext and context cannot exceed 2048 tokens, which is the input limit for
GPT-3</b>. When that limit is reached, the earlier portions of the context are truncated.<br>


<span style="color: gray">
<h2>Use</h2>
</span>

Run

```
python ChatGPT.py
```

The program will initialize the speech rocognition and synthesis modules, and ChatGPT will greet you. Talk with ChatGPT. Say "goodbye" to exit.
A transcription of your conversation will be in the log files, labeled by date and time.


<span style="color: gray">
<h2>Logs</h2>
</span>

The program also records transcriptions of the conversation in a log file. It is named by the date and time
of the ocnversation, and is stored in the logs directory.

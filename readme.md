<span style="color: gray">
<h1>Simple voice chat with GPT-3 or ChatGPT</h1>
</span>

Maybe the simplest voice chat with GPT-3 one can build? This is a project to build a voice interface for GPT-3, which can be used as a chatbot or for other purposes. Using SpeechRecognition to convert speech to text (using the Google speech recongition engine), passing the text to GPT-3 via the OpenAI API, and then converting the resulting text to speech using Coqui TTS and simple audio. The use case is defined by providing a prompt as a "pretext," which merely needs to be saved in a text file. 

<b>Update:</b> Changed both speech recognition engine to Vosk, and text to speech to pyttsx3. These are more efficient, resulting in less latency! Vosk performs
speech recognition, for example, locally rather than incurring an additional API call to the cloud (such as Google Speech Recognition services). Pyttsx3 seems
faster as well. On Windows it uses the SAPI for speech synthesis. For other platforms, you may need to install another synthesizer such as eSpeak. See the pyttstx3
documentation for details.

https://pyttsx3.readthedocs.io/en/latest/

<b>Update 3/1/2023</b> Now OpenAI has released an API for ChatGPT (today, in fact!), we've now added an application
to use it. The same pretext file is used as the initial prompting for the system. The configuration
file for ChatGPT is chatgpt_config.json, and the system prompt is in a separate text file (chat_pretext.txt).
The application to run is ChatGPT.py


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

gpt3_config.json: where you can set the specific engine, temperature, and max_tokens. Changing the temperature will change the
randomness or variation in of the model's responses. The lower the temperature, the less 'creative' it will be in its responses, 
and it may be more repetitive. The higher, the more 'creative' it may be.

chatgpt_config.json:
similar configuration for ChatGPT, except for not specifying the model being used. You can also
personalize your chatbot by telling it your name, e.g.,

```
"user": "karen"
```

The chatbot will then address you by name.

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

<span style="color: gray">
PRETEXT:
</span>

```
The following is a conversation with an AI assistant. The assistant is helpful, creative, 
clever, and very friendly. The assistant's name is Susan.
```

<span style="color: gray">
CONTEXT:
</span>

```
[human] Hello Susan.  
[AI] Hello, what can I do for you today?  
[human] Why don't you tell us who you are?  
[AI] I am Susan, an AI virtual assistant, so I'm always here to help you. No matter where you are, I'm here to answer your questions.  
[human] okay what is the meaning of life?  
[AI] The meaning of life is a complex question that has no single answer. Everyone has their own opinion on what life is all about. Some believe that life is about finding purpose and creating a life of meaning, while others believe that life is simply about experiencing joy and living in the moment. Ultimately, it's up to you to decide what the meaning of life is for you.
[human] Tell me more about it?
```

The <span style="color: gray">PRETEXT</span> defines a role or character for the conversational agent, or other
wise define it's purpose. It is defined in a text file in the working directory with the file name of 'pretext.txt' ('chat_pretext.txt' for ChatGPT). If one wants to omit a pretext (using the AI essentially out of the box), the file can simply be omitted.

The <span style="color: gray">CONTEXT</span> then is the rolling, recent conversation. 

The two portions of text are concatenated becoming the next prompt to the model.
<b>The total combination of pretext and context cannot exceed 2048 tokens, which is the input limit for
GPT-3</b>. When that limit is reached, the earlier portions of the context are truncated.<br>

<span style="color: gray">
<h2>Different tasks</h2>
</span>

There is no need to have the model only behave as an AI assistant or chatbot. You can, for example, also have it perform language translation. (Don't
expect a native accent -- its French pronunciation is horrible!)

```
[AI] Bonjour
[human] throw something and french
[AI] Lancer quelque chose
[human] your accent is really bad
[AI] Votre accent est vraiment mauvais
[human] goodbye
[AI] Au revoir
```

One can also
experiment with other sorts of prompt engineering: for example, maybe one wants a surly chatbot, with a cynical outlook on life. The pretext file can
also include few-shot learning, giving the model a few examples of how it should respond. One of the amazing abilities of these LLMs is there ability
to perform few-shot learning on new tasks.
        
<span style="color: gray">
<h2>Use</h2>
</span>

Run

```
python gpt_chat.py
```

Or, for the ChatGPT application, run

```
python ChatGPT.py
```

The program will initialize the speech rocognition and synthesis modules, and GPT-3 will greet you. Talk with GPT-3. Say "goodbye" to exit.
A transcription of your conversation will be in the log files, labeled by date and time.


<span style="color: gray">
<h2>Logs</h2>
</span>

The program also records transcriptions of the conversation in a log file. It is named by the date and time
of the ocnversation, and is stored in the logs directory.

<span style="color: gray">
<h1>Voice chatbot application using GPT-4</h1>
</span>

Evolving chatbot program now updated to use OpenAI's GPT-4 API. 

Currently, we are working on extracting user information from conversation,
which then expands the user profile. This way the language model will have some information from previous sessions, providing some degree
of long term memory. GPT-4 is prompted to extract that information and include it in snippets of JSON, key/value pairs. The software then
strips those out from the response, and updates the profile information (currently as a Python dictionary). It is then serialized as JSON
and the user profile file is updated.

The application uses a combination of Python procedures and prompt engineering. This way we task the LLM with performing routine operations
without explicitly coding them. For example, the model is instructed to extract information about the user that arises in conversation, including
that information as key/value snippets of JSON. The application pulls JSON formatted key/value pairs, passes through the rest of the LLM's
responses to the user, and then prompts the model to also merge the changes using further prompts rather than hard coding the process.

<span style="color: gray">
<h2>Installation</h2>
</span>

As a development project, 'installation' consists of pulling down the source code and installing the required dependencies. That is best done within a Python virtual
environment, so as to not possibly conflict with other Python packages already on one's system globally. This is the recommended practice for any such
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
pip install -r requirements.txt
```

4) If you do not already have an account to use the OpenAI API, you will need to do so. You 
will initially have $5 credit for usage, which is good for 3 months. If you have used the
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

(Replacing <your secret key> with your actual key.)

<span style="color: gray">
<h2>Configuration</h2>
</span>

There are four configuration files:

**gpt4_config.json:** Parameters for the language model.

```
{"model": "gpt-4",
 "temperature": 0.1,
 "top_p": 1,
 "n": 1,
 "presence_penalty": 0,
 "frequency_penalty": 0,
 "max_tokens": 64}
 ```

**vosk_config.json:** settings for vosk speech recognition. These have technical details like bit rate and buffer sizes, and likely
won't need to be changed often. But they are exposed for the brave.

```
{"model": "vosk-model-small-en-us-0.15",
"chunk": 4096,
"channels": 1,
"rate": 16000}
```

**voice.json:** here is where you may be able to select the voice to be used. Currently, it uses 
a voice provided by Windows 10. On other platforms one needs to find the voice they
prefer: see the pyttsx3 documentation linked above.

```
{"voice": "Microsoft Zira Desktop - English (United States)", 
 "rate": 130}
 ```
 
 **chat_user_profile.json:** This is the user profile. This is how the chatbot is can know the user. It is in JSON format. For example:

```
{"name": "Karen",
 "Location": "Moab",
 "Occupation": "Software Engineer"}
```
 
 The chatbot is programmed to then also expand the user profile with new information gleaned from the user's
 prompts. For example, once told about the user's dog, a terrier named Max, the model is instructed to extract
 that information into a machine readable form (a JSON snippet). The program strips that information from the
 model's response and it is stored, passing through the rest of the model's response to the user. At then end of
 the session it tasks GPT-4 to merge the new information to the user profile, so as to provide a limited form 
 of long term memory. 
 
 ```
{"name": "Karen",
 "Location": "Moab",
 "Occupation": "Software Engineer",
 "has_dog": "yes",
 "dogs_name" "Max",
 "dog_breed": "terrier"}
```

 During future chat's GPT-4 may, for example, refer to the information, such as enquiring about your dog's
 well being by name. (How cool is that?)
 
**gpt4-system_prompt.txt:** This is the prompt engineering for the model. It can define parameters for the model,
such as its role, persona, tone, and so forth, as well as instructing it for specific tasks, such as extracting
new user information. User information is extracted as key/value pairs which the application pulls from the model's
responses and chached to merge at the conclusion of the session.

At run time, the user profile is appended to the text in this file, and the complete prompt is then submitted to the model 
as the 'system message.' (GPT-4 is more robust working with the system message than as was the case with ChatGPT,
which often ignored it.)

Example of the system prompt (minus the user profile):

```
You are a friendly chatbot, named Susan, who likes to discuss many topics.
You are helpful with your friends, enquiring as to their well being, always kind and caring.
You like to learn new things about them as well.
Your responses are informal and brief, as in a casual social conversation.

Extract any new persistent user profile information from user prompts and generate key/value pairs. 
Output the key/value pairs at the beginning of your responses. Persistent information are ones such as 
names, ages, favorite foods, hobbies, job, etc. Information that will remain true from session 
to session. For example:

User: My dog's name is Ralf
Assistant: {"dogs_name": "Ralf"} Thank you for telling me about Ralf. I will remember their name.

User: I started a new job as an AI engineer.
Assistant: {"occupation": "AI Engineer"} That is awesome, I am happy that you have reached on of your goals!

If an existing fact no longer exists, generate a key/value pairs to indicate that change also. This may
affect multiple key/value pairs which apply to the change. For example:

User: I had to give my dog Ralf away. It was too much to have two pets. I am sad though.
Assistant: {"dogs_name": "None", "dogs_breed": "None", "dogs_age": "None"} I am really sorry you had to make that choice.

Please follow these instructions accurately for the entirety of the conversation.
```

It uses context learning, inclduing one shot learning in this example (giving the model a single
example to understand the task it is being asked of. This is a new, upcoming paradigm for programming,
AKA "AI Whispering." As much teaching as programming!

**gpt4_merge_instructions.txt:** During the session, the application gathers any key/value pairs extracted
during the conversation. At the end of the session the application then prompts GPT-4 to merge thoses into
the user profile. This file contains the system prompt with instructions for the merging. E.g.:

```
Merge the changes provided to the user profile, and only respond with the 
final updated profile JSON.

If there is an existing key for an item, consider how to update it.

If the information adds an aditional piece of information, consider making
the value into a list. For example,

Existing profile contains: {"pet": "cat"}
Change includes: {"pet", "dog"}
Merge as: "{"pets": ["cat", "dog"]}

If it is instead updating a singular fact, it should be just updated. A 
"singular fact" is something of which there is only a single value.
For example:

Existing profile contains: {"age": 64}
Change includes: {"age": 65}
Merge as : {"age": 65}
As one will only have one current age.

If the new value for an existing key is "None", the key/value should be deleted:
For example:

Existing profile contains: {"dogs_name": "Max"}
Change includes: {"dogs_name", "None"}
Merge as: delete the key/value pair
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

There is also a debug mode, which will display and log newly extract key/value pairs (and other debug information as the project continues).

```
python GPT4Chat.py debug
```

The two command line arguments can also be combined.


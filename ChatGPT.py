'''
GPT Chat

The loop is basically

speech -> text -> prompt -> completion by GPT-3 -> response -> speech

Until the user says simply "goodbye", at which point the model is allowed
to reply, and then the program exits.

'''
import os
import sys
import re
import json
import logging
from datetime import datetime
import openai
from dotenv import load_dotenv

from ChatGPTContext import Context
from vosk_recognizer import SpeechRecognize
from tts import Text2Speech


class ChatGPT:
    def __init__(self, logger):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')

        # get configuration
        with open('chatgpt_config.json', 'r') as FP:
            self.config = json.load(FP)

        # intialize speech recognition
        self.recog = SpeechRecognize()

        # Initialize TTS
        self.tts = Text2Speech()

        # get system prompt
        with open('chat_system_prompt.txt', 'r') as PRETEXT:
            sys_prompt = PRETEXT.read()

        # get pretext and profile
        with open('chat_instructions.txt', 'r') as PRETEXT:
            self.instructions = PRETEXT.read()

        with open('chat_user_profile.json', 'r') as PROFILE:
            self.__profile = json.load(PROFILE)

        # set up context
        self.context = Context(response_tokens=self.config['max_tokens'], 
                               pretext=sys_prompt,
                               profile=self.__profile)

        self.logger = logger
        self.logger.info("*Begin log*\n")

    def loop(self, voice=True):
        '''
        The main loop

        Loops until the user says simply "goodbye" and model has responded
        to that prompt.
        '''
        text = ''
        iteration = 0
        while True:
            # send prompt to GPT-3
            prompt = self.context.get_prompt()
            ai_text, n_tokens = self.__prompt_gpt(prompt)
            ai_text = self.__filterResponse(ai_text)

            # speak and log response
            if iteration == 1:
                self.logger.info(f'[Hidden] {ai_text}')
                print(f'\n{ai_text}')
            else:
                if voice:
                    self.tts.speak(ai_text)
                else:
                    print(f'{ai_text}')
                self.logger.info(f'[AI] {ai_text.strip()}')
                self.context.add(role='assistant',
                                text=ai_text, 
                                n_tokens=n_tokens)

            # See if user said goodbye
            if text == 'goodbye':
                break

            if iteration == 0:
                self.context.add(role='user', text=self.instructions)
            else:
                # Listen for user input
                if voice:
                    text = self.recog.speech_to_text()
                else:
                    text = input('>> ')
                # update context and get prompt
                self.logger.info(f'[Human] {text}')
                self.context.add(role='user', text=text)
            iteration += 1

        self.logger.info('\n*End log*')

        # update profile
        with open('chat_user_profile.json', 'w') as PROFILE:
            json.dump(self.__profile, PROFILE)
        print('\rExiting...')

    def __filterResponse(self, text):
        # extract kv_pair if found
        pattern = re.compile(r'{"\w+":\s*"[^"]+"}')
        match = pattern.search(text)
        if match:
            kv_pair = match.group()
            self.logger.info(f"Key/value pair extracted: {kv_pair}")
            print(f'Key/value pair extracted: {kv_pair}')
            
            # Add the key/value pair to data structure
            kv = json.loads(kv_pair)
            key, value = list(kv.items())[0]
            self.__profile[key] = value
        return re.sub(pattern, '', text).strip()

    def __prompt_gpt(self, prompt):
        '''
        Prompt GPT-3

        Input: prompt - string
        Returns: text from the model
        '''
        print('\rWaiting...     ', end='')
        openai.api_key = self.secret_key
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=prompt,
            max_tokens=self.config['max_tokens'],
            temperature=self.config['temperature'],
            top_p=self.config['top_p'],
            n=self.config['n'],
            presence_penalty=self.config['presence_penalty'],
            frequency_penalty=self.config['frequency_penalty']
        )
        text = response.choices[0].message.content
        n_tokens = response.usage.completion_tokens
        return text, n_tokens


def main():
    if len(sys.argv) > 1:
        voice = sys.argv[1] != 'novoice'
    else:
        voice = True

    # initialize logging
    now = datetime.now()
    logfile = f'chatgptlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = ChatGPT(logger)
    gpt_chat.loop(voice=voice)


if __name__ == '__main__':
    main()

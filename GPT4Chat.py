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

from context import Context
from vosk_recognizer import SpeechRecognize
from tts import Text2Speech


class ChatGPT:
    def __init__(self, logger):
        # fetch API key from environment
        load_dotenv()
        self.secret_key = os.getenv('SECRET_KEY')
        self.memories = []

        # get configuration
        with open('gpt4_config.json', 'r') as FP:
            self.config = json.load(FP)

        # intialize speech recognition
        self.recog = SpeechRecognize()

        # Initialize TTS
        self.tts = Text2Speech()

        # get system prompt
        with open('gpt4_system_prompt.txt', 'r') as PRETEXT:
            sys_prompt = PRETEXT.read()

        # get profile
        with open('chat_user_profile.json', 'r') as PROFILE:
            self.__profile_JSON = PROFILE.read()
        self.__profile = json.loads(self.__profile_JSON)
        sys_prompt += '\nUser Profile:\n' + self.__profile_JSON

        self.context = Context(num_response_tokens=self.config['max_tokens'], 
                               pretext=sys_prompt,
                               max_context_tokens=8192)

        # start log
        self.logger = logger
        self.logger.info("*Begin log*\n")

    def loop(self, voice=True):
        '''
        The main loop

        Loops until the user says simply "goodbye" and model has responded
        to that prompt.
        '''
        text = ''
        while True:
            # send prompt to GPT-4
            prompt = self.context.get_prompt()
            ai_text, n_tokens = self.__prompt_gpt(prompt)
            ai_text_filter = self.filterResponse(ai_text)

            # speak and log response
            if voice:
                self.tts.speak(ai_text_filter)
            else:
                print(f'\r{ai_text_filter}')
            self.logger.info(f'[AI] {ai_text_filter}')

            # update context. If first two iterations, store as pretext
            # (pinned messages). 
            self.context.add(role='assistant',
                            text=ai_text,
                            n_tokens=n_tokens)

            # See if user said goodbye
            if text == 'goodbye':
                break

            # Listen for user input
            if voice:
                text = self.recog.speech_to_text()
            else:
                text = input('>> ')
            # update context and get prompt
            self.logger.info(f'[Human] {text}')
            self.context.add(role='user', text=text)

        self.logger.info(f'Extracted info: {self.memories}')
        self.logger.info('\n*End log*')

        # update profile
        self.update_profile(self.memories)
        print('\rExiting...')

    def update_profile(self, memories):
        for memory in memories:
            memory_dict = json.loads(memory)
            for key in memory_dict.keys():
                if  key == 'context':
                    continue
                value = memory_dict[key]
                try:
                    if self.__profile.get(key) is not None:
                        if not isinstance(self.__profile[key], list):
                            self.__profile[key] = [self.__profile[key]]
                        self.__profile[key].append(value)
                    else:
                        if isinstance(value, str):
                            if not isinstance(value, list):
                                value = value.split(', ') if ',' in value else value
                        self.__profile[key] = value
                except:
                    self.logger.info(f'Error storing memory {memory}')
                    continue
        with open('chat_user_profile.json', 'w') as PROFILE:
            json.dump(self.__profile, PROFILE)

    def filterResponse(self, text):
        # extract kv_pair if found
        pattern = re.compile(r'{(?:[^{}]|((?:{[^{}]*})+))*}')
        match = pattern.search(text)
        if match:
            kv_pairs = match.group()
            self.logger.info(f"Key/value pairs extracted: {kv_pairs}")
            print(f"{kv_pairs}")
            
            # Add the key/value pair to data structure (for now just
            # accumulate them)
            self.memories.append(kv_pairs)
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
            model=self.config['model'],
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
    logfile = f'gpt4chatlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
    logpath = os.path.join('logs', logfile)
    logging.basicConfig(filename=logpath, 
                        level=logging.INFO, 
                        format='%(message)s')
    logger = logging.getLogger()

    # Inistantiate GPTChat and run loop
    print('Initializing...', end='')
    gpt_chat = ChatGPT(logger)
    gpt_chat.loop(voice=False)


if __name__ == '__main__':
    main()
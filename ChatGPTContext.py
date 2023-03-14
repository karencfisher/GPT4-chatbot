'''
Maintain context buffer for ChatGPT.

There are two sections:

PRETEXT: a description of the chatbot
CONTEXT: the current conversation

The maximum length of the buffer is 4096 tokens. We will deduct the
length of the pretext, and the maximum tokens for a response. When
queried for the current context, will will return messages from
the most recent until fitting within the difference.

'''
import tiktoken as tt


class Context:
    def __init__(self, pretext, profile, response_tokens=128, max_tokens=4096):
        self.__context = []
        self.__max_tokens = max_tokens
        self.__response_tokens = response_tokens

        # get system prompt (pretext)
        self.__encoder = tt.get_encoding('p50k_base')
        num_pretext_tokens = len(self.__encoder.encode(pretext))
        self.__pretext = {'role': 'system', 'content': pretext}
        user_profile, num_intro_tokens = self.update_prompt(profile)
        self.__intro = {'role': 'user', 'content': user_profile}
        self.__max_context = max_tokens - (num_pretext_tokens + num_intro_tokens)

    def update_prompt(self, profile):
        # Unpack dictionary to text version of profile
        items = [f'{key}: {value}' for key, value in profile.items()]
        profile_txt = '\n'.join(items)
        profile_txt = f'User profile:\n{profile_txt}\n\nHello'
        
        # get count of tokens
        num_tokens = len(self.__encoder.encode(profile_txt))

        return profile_txt, num_tokens

    def get_prompt(self):
        '''
        Manage the context capacity as well as returning the 
        combined pretext and context
        '''
        # encode the context, and truncate early portion as needed
        # to keep within limit
        n_tokens = 0
        context = []
        for indx in range(len(self.__context) - 1, -1, -1):
            n_tokens += self.__context[indx]['n_tokens']
            if n_tokens >= self.__max_context:
                break
            context.append(self.__context[indx]['message'])
        context.append(self.__intro)
        context.append(self.__pretext)
        # return concatenated pretext and context
        return context[::-1]

    def add(self, role, text, n_tokens=None):
        '''
        Add token count, role, and content to the context

        Input: new text
        '''
        if len(text) > 0:
            if n_tokens is None:
                n_tokens = len(self.__encoder.encode(text))
            message = {'n_tokens': n_tokens, 'message': {'role': role, 'content': text}}
            self.__context.append(message)


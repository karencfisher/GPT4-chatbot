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
    def __init__(self, response_tokens, max_tokens=4096, pretext=''):
        self.__context = []
        if len(pretext) > 0:
            self.__pretext = {'role': 'system', 'content': pretext}
            
        # Store pretext and it's length in tokens
        self.__encoder = tt.get_encoding('p50k_base')
        pretext_enc = self.__encoder.encode(pretext)

        # Store maximum number of tokens in the context
        self.__max_context = max_tokens - len(pretext_enc) - response_tokens

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


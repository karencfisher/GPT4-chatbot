from GPT4Chat import GPT4Chat
import logging
from datetime import datetime
import os
from pprint import pprint
import json


now = datetime.now()
logfile = f'chatgptlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
logpath = os.path.join('logs', logfile)
logging.basicConfig(filename=logpath, 
                    level=logging.INFO, 
                    format='%(message)s')
logger = logging.getLogger()
c = GPT4Chat(logger)

cases = ['{"hobby": "beer making"} Wow, that is really interesting.',
         '{"location": "Seattle"} Seattle is a beautiful and diverse city.']
for j in cases:
    text = c.filterResponse(j)
    print(text)
print(c.memories)

print('Before:')
with open('chat_user_profile.json', 'r') as PROFILE:
    profile = json.load(PROFILE)
pprint(profile)

c.update_profile()
print('\nAfter:')
with open('chat_user_profile.json', 'r') as PROFILE:
    profile = json.load(PROFILE)
pprint(profile)

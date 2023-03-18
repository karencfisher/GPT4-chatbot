from GPT4Chat import ChatGPT
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
c = ChatGPT(logger)

cases = ['{"name": "Karen"} And some text after.', 
         '{"fruits": ["apple", "orange"]} some other stuff.',
         '{"pet_age": {"Nyima": 11, "Max": 1}} well that is very cool.']
for j in cases:
    text = c.filterResponse(j)
    print(text)
print(c.memories)

print('Before:')
with open('chat_user_profile.json', 'r') as PROFILE:
    profile = json.load(PROFILE)
pprint(profile)

m = ['{"mood": "relaxed", "activity": "chilling out with cat", "weather": "sunny"}', '{"pet_name": "Nyima"}', '{"pet_breed": "ginger"}', '{"pet_favorite_treats": "turkey and ham"}', '{"has_dog": true}', '{"pet_name": "Max", "pet_breed": "chihuahua"}', '{"pet_age": {"Nyima": 11, "Max": 1}}', '{"pet_relationship": "Nyima is weirded out by Max being a smaller dog"}', '{"about_me": "I am a friendly chatbot named Susan. I am designed to have casual social conversations with people and discuss a variety of topics. I enjoy learning about people\'s interests, hobbies, and pets. My goal is to be helpful and provide a positive experience for those who interact with me."}']

c.update_profile(m)
print('\nAfter:')
with open('chat_user_profile.json', 'r') as PROFILE:
    profile = json.load(PROFILE)
pprint(profile)

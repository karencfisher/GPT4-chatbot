from ChatGPT import ChatGPT
import logging
from datetime import datetime
import os


now = datetime.now()
logfile = f'chatgptlog-{now.strftime("%m.%d.%Y-%H.%M.%S")}.log'
logpath = os.path.join('logs', logfile)
logging.basicConfig(filename=logpath, 
                    level=logging.INFO, 
                    format='%(message)s')
logger = logging.getLogger()

m = '{"art_style": "abstract", "hobby": "painting"}', '{"cat_name": "Nyima"}', '{"career_goal": "getting a job in AI field"}', '{"other_pet": "dog"}', '{"cat_age": "11 years old"}', '{"weather": "sunny", "activity": "chilling with cat"}', '{"dog_behavior": "scared of Nyima"}', '{"education": "completed certificate in AI from NC State University"}', '{"dog_breed": "chihuahua", "dog_name": "Max"}', '{"interests": "AI, art"}', '{"dog_tenure": "1 month"}'
c = ChatGPT(logger)
c.update_profile(m)

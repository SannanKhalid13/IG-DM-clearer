import httpx
import time
import os
from dotenv import load_dotenv

load_dotenv()
thread_id=os.getenv('thread_id')
cursor_id=os.getenv('cursor_id')
user_id=os.getenv('user_id')

class acc:
    def __init__(self):  
        self.session = httpx.Client(
        headers={
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': os.getenv("cookie"),
        'referer': os.getenv("referer"),
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': os.getenv('sec-ch-ua'),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': os.getenv('sec-ch-ua-platform'),
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': os.getenv('user-agent'),
        'viewport-width': os.getenv('viewport-width'),
        'x-asbd-id': os.getenv('x-asbd-id'),
        'x-csrftoken': os.getenv('x-csrftoken'),
        'x-ig-app-id': os.getenv('x-ig-app-id'),
        'x-ig-www-claim': os.getenv('x-ig-www-claim'),
        'x-requested-with': os.getenv('x-requested-with')'
        },timeout=30)

    def get_msg_ids(self):
        url=f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
        #url=f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/?cursor={cursor_id}"
        req=self.session.get(url)
        print(req.status_code)
        f=open('ig_message_ids.txt','a')
        for items in req.json()['thread']['items']:
            if items['user_id']=='4042198693':
                print(items['item_id'])
                f.write(items['item_id']+'\n')
        # next=req.json()['thread']['oldest_cursor']
        next=req.json()['thread']['items'][-1]['item_id']
        while True:
            print("prev cursor id : ",next)
            # url=f"https://www.instagram.com/api/v1/direct_v2/threads/340282366841710300949128456283095387202/?cursor={next}"
            url=f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/?cursor={next}"
            req=self.session.get(url)
            # next=req.json()['thread']['next_cursor']
            next=req.json()['thread']['items'][-1]['item_id']

            for items in req.json()['thread']['items']:
                if items['user_id']==user_id:
                    f.write(items['item_id']+'\n')

    def del_messages(self,msgs):
        for msg_id in msgs:
            time.sleep(1.7)
            url=f"https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/items/{msg_id}/delete/"
            req=self.session.post(url)
            print(req.status_code)
            if req.status_code==429:
                print("Rate Limited. Sleeping for 2 minutes")
                time.sleep(120)


if __name__=="__main__":
    session=acc()
    choice=input("1.Get messages\n2. Del messages\n")
    if choice=="1":
        session.get_msg_ids()
    elif choice=="2":
        with open("ig_message_ids.txt") as f:
            msgs = f.read().splitlines()
        session.del_messages(msgs)

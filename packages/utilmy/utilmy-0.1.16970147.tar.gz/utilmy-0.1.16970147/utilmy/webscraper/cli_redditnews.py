"""

Fetch secret from here:
https://www.reddit.com/prefs/apps/


pip install praw fire utilmy


export reddit_client=''
export reddit_client_secret='meYGqgbj1ya1BDKLNtoXu8lIkTGAYg'
export reddit_ua='daily'
export reddit_subreddit='MachineLearning,OpenAI,ChatGPT,OpenAIDev,learnmachinelearning'


cd utilmy/webscrapper/

python cli_redditnews.py run --query 'icml 2023, neurips 2023'  --dirout ztnp/reddit/



"""
import fire, os, praw, pandas as pd
from utilmy import (date_now, pd_to_file, os_makedirs, log)


def run(query:str='icml 2023, ', dirout:str="ztmp/", subreddits=None, reddit_limit=10, reddit_sort='top', verbose=1):

    ### from https://www.reddit.com/prefs/apps/
    client_id     = os.environ.get("reddit_client_id")
    client_secret = os.environ.get("reddit_client_secret")
    user_agent    = os.environ.get("reddit_ua",  "daily")   ### Same from Secret page
    reddit = praw.Reddit(client_id = client_id,#my client id
                     client_secret = client_secret,  #your client secret
                     user_agent    = user_agent #user agent name
                     )

    if subreddits is None :
        subreddits = os.environ.get('reddit_subreddit', 'MachineLearning,OpenAI,ChatGPT,OpenAIDev,learnmachinelearning' ) 
        subreddits = subreddits.split(",")

    if isinstance(query, str):
        query = query.split(",")

    ymd = date_now(fmt='%Y%m%d', returnval='str')    

    log("########## Start Scrapping")
    dfall = pd.DataFrame() 
    for s in subreddits:
        subreddit = reddit.subreddit(s) 
        log('fetching:', s)

        for item in query:
            ddict = {
            "title" : [], "score" : [], "id" : [], "url" : [], "comms_num": [], "created" : [], "body" : []
            }
            
            for submi in subreddit.search(query,sort = reddit_sort,limit = reddit_limit):
                ddict["title"].append(submi.title)
                ddict["score"].append(submi.score)
                ddict["id"].append(submi.id)
                ddict["url"].append(submi.url)
                ddict["comms_num"].append(submi.num_comments)
                ddict["created"].append(submi.created)
                ddict["body"].append(submi.selftext)

            dfres = pd.DataFrame(ddict)
            log( f'{item}: N article: ', len(dfres))
            dfall = pd.concat([dfall,dfres], axis=0,ignore_index=True)

    pd_to_file(dfall, dirout + f"/subreddit_{ymd}.csv"), sep="\t")
    return

if __name__ == "__main__":
  fire.Fire()


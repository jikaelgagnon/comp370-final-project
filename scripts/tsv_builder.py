import pandas as pd
import json
import os

def get_merged_dfs(folder):
    dfs = []
    for file in os.listdir(folder):
        filename = os.path.join(folder, os.fsdecode(file))
        if not filename.endswith(".json"):
            continue
        with open(filename) as f:
            json_file = json.load(f)
            data = json_file['articles']
            df = pd.DataFrame(data)
            df = df[df['title'] != '[Removed]'] # filter out removed articles
            df['source'] = df['source'].map(lambda x: x['name'])
            df['topic'] = ''
            df['positive/negative'] = ''
            df = df.drop(['urlToImage','content'], axis=1)
            dfs.append(df)
    return pd.concat(dfs)
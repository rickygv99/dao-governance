import pandas as pd

df = pd.read_csv(r'./csv/pooltogether/pooltogether_ens.csv')
df = df.sort_values(by=['proposalID.id'], ascending= True)

def shorten_string(s):
    if len(s) > 1:
        s = s[:-2] 
    return s

df['single_vote'] = df['single_vote'].astype(str).map(lambda x: shorten_string(x))

df.to_csv("./csv/pooltogether/pooltogether_ens.csv", index=False)


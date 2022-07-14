import pandas as pd
from web3.auto.infura import w3
from ens import ENS

ns = ENS.fromWeb3(w3)
df = pd.read_csv(r'./csv/compoundf.csv')
# pd.options.display.max_columns = len(df.columns)

addresses = df['voters.id'].unique()
print(len(addresses))

df['name'] = df['voters.id']

print('starting conversion...')
for address in addresses:
    df.loc[df['voters.id'] == address, 'name'] = ns.name(address)

df.to_csv("./compound_ens.csv")
print('done')



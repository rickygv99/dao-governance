import pandas as pd
import numpy as np
from web3.auto.infura import w3
from ens import ENS

"""
To Do:
    add way to export infura key
"""

def get_voters(name, result):
    print("generating voters table")
    voters = pd.json_normalize(result,record_path=["voters", "votes"], meta=[['voters', 'id']])
    cols_to_move = ['proposalID.id', 'voters.id']
    voters = voters[cols_to_move + [col for col in voters.columns if col not in cols_to_move]]
    voters = voters.rename(columns={"proposalID.id": "proposal", "voters.id": "voter"})
    voters['proposal'] = voters['proposal'].astype(int)
    if name == "Compound":
        voters['single_vote'] = np.array(voters['single_vote'], dtype=np.float64)
        voters['single_vote'] = voters['single_vote'] / 10**18

    voters = voters.sort_values(by=['proposal'], ascending=True)
    return voters

def get_voting_rate(result):
    # return voting_rate
    pass

def add_ens(voters):
    ns = ENS.fromWeb3(w3)
    addresses = voters['voter'].unique()

    print("Number of unique addresses: ", len(addresses))
    voters['name'] = voters['voter']
    
    print('starting conversion...')
    for address in addresses:
        voters.loc[voters['voter'] == address, 'name'] = ns.name(address)
    
    return voters


def trim(name, voters):
    # return voters
    pass




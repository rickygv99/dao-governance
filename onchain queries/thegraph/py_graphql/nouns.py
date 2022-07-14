from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import os  

os.makedirs('./csv', exist_ok=True)  

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/28876/multigovernance/v0.0.3")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
        proposals(first: 1000) {
            id
            blocktime
            votes {
              voter{
                id
              }
              single_vote
            }
        }
        singleVotes(first: 1000) {
            id
            voter {
              id
            }
            single_vote
            proposalID {
              id
            }
            support
        }
        voters(first: 1000, where:zx) {
            id
            votes{
                proposalID{
                    id
                }
                support
                single_vote
            }
        }
        implementations{
            id
            blocktime
            newImplementation
        }
    } 
    """
)

# Execute the query on the transport
result = client.execute(query)

pd.set_option('display.max_colwidth', None)

voter_list = pd.json_normalize(result['voters'])
voter_list.to_csv('./csv/nouns_addresses.csv')

df_voters = pd.json_normalize(result,record_path=["voters", "votes"], meta=[['voters', 'id']])

cols_to_move = ['voters.id', 'proposalID.id']
df_voters = df_voters[ cols_to_move + [col for col in df_voters.columns if col not in cols_to_move ] ]

df_voters.to_csv('./csv/nounsf.csv')

df_voters['id_proposal'] = df_voters[["voters.id", "proposalID.id"]].apply(tuple,axis=1)
df_voters['support_votes'] = df_voters[["support", "single_vote"]].apply(tuple,axis=1)
df_voters = df_voters.drop(columns=['voters.id', 'proposalID.id', 'support', 'single_vote'])

df_voters.to_csv('./csv/nouns.csv')  

proposal_result = result['proposals']
implementation_result = result['implementations']
tmp = {}
for proposal in proposal_result:
    proposal_id = proposal['id']
    max_vote = 0
    # tmp[proposal_id]['blocktime'] = proposal['blocktime']
    for vote in proposal['votes']:
        max_vote += int(vote['single_vote'])
    voting_rate = max_vote / 10**25
    tmp[proposal_id] = voting_rate
# 
df_voting_rates = pd.json_normalize(tmp)
 
# with open('propsals.pickle', 'wb') as f:
#    pickle.dump(df_voting_rates, f)


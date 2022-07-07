from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pickle
import pandas as pd
from flatten_json import flatten
# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/28876/governance/v0.2.5")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
        proposals{
            id
            blocktime
            votes {
              voter{
                id
              }
              single_vote
            }
        }
        singleVotes(first: 5, where: {support: 10}) {
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
        voters(first: 1000) {
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


# for voter in voters:
#     n_voter = pd.json_normalize(voter['votes'])
#     print(n_voter)
#     print(n_voter.sort_values("proposalID.id"))
#     break
pd.set_option('display.max_colwidth', None)
df_voters = pd.json_normalize(result,record_path=["voters", "votes"], meta=[['voters', 'id']])

with open('compound_matrix.pickle', 'wb') as f:
    pickle.dump(df_voters, f)

# print(df)
# print(len(result['voters']))

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
 
with open('propsals.pickle', 'wb') as f:
    pickle.dump(df_voting_rates, f)
# 
# with open('implementations.pickle', 'wb') as f:
#     pickle.dump(implementation_result, f)
# 

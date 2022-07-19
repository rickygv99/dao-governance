from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import datetime
import pandas as pd
import os  

os.makedirs('./csv', exist_ok=True)  

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/28876/multigovernance/v0.2.1")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
        proposals(first: 1000) {
            id
            blocktime
            forvotes
            againstvotes
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
        voters {
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

# Voting Rates
proposal_result = result['proposals']
df_voting_rates = pd.json_normalize(proposal_result)

forvotes, againstvotes, vote_rate = [], [], []
for proposal in proposal_result:
    forvote = int(proposal["forvotes"])
    againstvote = int(proposal['againstvotes'])
    forvotes.append(forvote)
    againstvotes.append(againstvotes)
    vote_rate.append(forvote + againstvote)

print(forvotes)

df_voting_rates['blocktime'] = df_voting_rates['blocktime'].map(lambda time: datetime.datetime.fromtimestamp(int(time)))
df_voting_rates['vote_rate'] = vote_rate
# df_voting_rates['forvotes'] = forvotes
# df_voting_rates['againstvotes'] = againstvotes
df_voting_rates = df_voting_rates.drop(columns=['forvotes', 'againstvotes'])
df_voting_rates['id'] = df_voting_rates['id'].astype(int)
df_voting_rates = df_voting_rates.sort_values(by=['id'], ascending= True)
df_voting_rates.to_csv('./csv/nouns_voting_rates.csv')

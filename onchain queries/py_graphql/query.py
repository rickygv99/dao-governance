from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pickle

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/28876/governance/v0.2.3")

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
              voter
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
proposal_result = result['proposals']
implementation_result = result['implementations']

tmp = {}
for proposal in proposal_result:
    proposal_id = proposal['id']
    max_vote = 0
    tmp[proposal_id] = {}
    tmp[proposal_id]['blocktime'] = proposal['blocktime']
    for vote in proposal['votes']:
        max_vote += int(vote['single_vote'])
    voting_rate = max_vote / 10**23
    tmp[proposal_id]['vote_rate'] = voting_rate

print(tmp)

print(implementation_result)

with open('propsals.pickle', 'wb') as f:
    pickle.dump(tmp, f)

with open('implementations.pickle', 'wb') as f:
    pickle.dump(implementation_result, f)


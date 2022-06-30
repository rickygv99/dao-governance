from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/28876/governance/v0.2")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    {
        proposals(first: 100)
        {
            id
            votes {
              voter
              single_vote
            }
        }
    } 
    """
)

# Execute the query on the transport
result = client.execute(query)['proposals']
tmp = {}
for proposal in result:
    proposal_id = proposal['id']
    max_vote = 0
    for vote in proposal['votes']:
        max_vote += int(vote['single_vote'])
    voting_rate = max_vote / 10**23
    tmp[proposal_id] = int(voting_rate)

print(tmp)

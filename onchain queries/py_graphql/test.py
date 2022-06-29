from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.studio.thegraph.com/query/28876/governance/v0.0.7")

# Create the query string and variables required for the request.
query = """
    {
      proposals(first: 5) {
        id
        proposalID
        votes
        voter
      }
    }
"""
variables = {"countryCode": "CA"}

# Synchronous request
data = client.execute(query=query)
print(data)

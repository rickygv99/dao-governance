import React from 'react';
import { render } from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {
    ApolloClient,
    InMemoryCache,
    ApolloProvider,
    useQuery,
    gql
} from "@apollo/client"

const client = new ApolloClient({
  uri: 'https://api.studio.thegraph.com/query/28876/governance/v0.0.7',
  cache: new InMemoryCache()
});



client
  .query({
    query: gql`
     {
      proposals(first: 5) {
        id
        proposalID
        votes
        voter
      }
    }
    `
  })
    .then(result => console.log(result));

function App() {
  return (
    <div>
      <h2>My first Apollo app 🚀</h2>
    </div>
  );
}

render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

function drawCharts() {
  let spaces = [
    "ens.eth",
    "uniswap",
    "aave.eth",
    "nouns.eth",
    "pooltogether.eth",
    "yam.eth",
    "sushigov.eth",
    "olympusdao.eth",
    "gitcoindao.eth",
  ];

  (async () => {
    let daos = [["Name", "Average voting rate"]];
    let voteOverTimeData = [["Time (in days)", "30", "60", "90", "120", "150"]];
    for (let i = 0; i < spaces.length; i++) {
      const fetchFollowersData = async (args) => {
        const res = await fetch("https://hub.snapshot.org/graphql", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: `
              query Spaces($space: String!) {
                spaces(where: {id: $space}) {
                  id
                  name
                  followersCount
                }
              }
            `,
            variables: {
              space: spaces[i],
            },
          }),
        });

        const body = await res.json();
        return body.data.spaces[0];
      };

      const fetchProposals = async (args) => {
        const res = await fetch("https://hub.snapshot.org/graphql", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: `
              query Proposals($space: String!) {
                proposals(first: 2147483646, skip: 0, where: {created_gte: 1640995200, state: "closed", space: $space}) {
                  id
                  title
                  votes
                }
              }
            `,
            variables: {
              space: spaces[i],
            },
          }),
        });

        const body = await res.json();
        return body.data.proposals;
      };
      
      let followersData = await fetchFollowersData();
      let followersCount = followersData.followersCount;
      let name = followersData.name;
      
      let voteCountsOverTime = [name];
      let startTime = 1640995200; // January 1, 2022 in Unix time (seconds)
      let period = 2592000; // 30 days in seconds
      for (let j = 0; j < 5; j++) {
        let fetchProposalsForVoting = async (args) => {
          let res = await fetch("https://hub.snapshot.org/graphql", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              query: `
                query Proposals($space: String!, $created_gte: Int!, $created_lte: Int!) {
                  proposals(first: 2147483646, skip: 0, where: {created_gte: $created_gte, created_lte: $created_lte, state: "closed", space: $space}) {
                    id,
                    votes
                  }
                }
              `,
              variables: {
                space: spaces[i],
                created_gte: startTime + j * period,
                created_lte: startTime + (j + 1) * period - 1,
              },
            }),
          });

          let body = await res.json();
          return body.data.proposals;
        }
        
        let proposals = await fetchProposalsForVoting();
        let sum = 0;
        for (let j = 0; j < proposals.length; j++) {
          sum += proposals[j].votes;
        }
        let voteRate = 100 * sum / (proposals.length * followersCount);
        voteCountsOverTime.push(voteRate);
      }
      voteOverTimeData.push(voteCountsOverTime)

      let proposals = await fetchProposals();

      let sum = 0;
      for (let j = 0; j < proposals.length; j++) {
        let p = 100 * proposals[j].votes / followersCount;
        sum = sum + p;
      }
      let avg = sum / proposals.length;

      daos.push([
        name,
        avg,
      ]);
    }

    var data_bar = google.visualization.arrayToDataTable(daos);
    var options_bar = {
      title: "Average Voting Rate by DAOs (All-Time)",
      width: 800,
      height: 800,
      hAxis: {
        title: "Average voting rate (%)",
        minValue: 0
      },
      legend: {position: "none"},
    };
    var chart_bar = new google.visualization.BarChart(document.getElementById('chart_div_bar'));
    chart_bar.draw(data_bar, options_bar);
    
    // Transpose data
    // https://stackoverflow.com/questions/17428587/transposing-a-2d-array-in-javascript
    voteOverTimeData = voteOverTimeData[0].map((col, i) => voteOverTimeData.map(row => row[i]));
    
    var data_line = google.visualization.arrayToDataTable(voteOverTimeData);
    var options_line = {
      title: "DAO Voting Rates Over Time",
      width: 800,
      height: 800,
      hAxis: {
        title: "Time (in days)",
        minValue: 0
      },
      vAxis: {
        "title": "Average voting rate (%)"
      },
      legend: {position: "bottom"},
      curveType: 'function',
    };
    var chart_line = new google.visualization.LineChart(document.getElementById('chart_div_line'));
    chart_line.draw(data_line, options_line);
  })();
}

// Load the Visualization API and the corechart package.
google.charts.load("current", { packages: ["corechart", "bar"] });

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawCharts);

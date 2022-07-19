import os
import pandas as pd
from query import make_query
from utils import get_voters, trim, add_ens

os.makedirs('./csvs/voters', exist_ok=True)  

with open('metadata.txt') as f:
    lines = f.readlines()
    metadata = [] 

    for line in lines:
        line = line.strip() 
        if line:
            metadata.append((item.strip() for item in line.split(',')))

# Generate voter data
for data in metadata:
    name, api, params = data
    
    print(f"Generating vote data for {name}...")
    result = make_query(api)
    voters = get_voters(name, result)
    voters = add_ens(voters)
    voters.to_csv(f"./csvs/voters/{name}_voters.csv")
    print(f"Finished generating for {name}...")

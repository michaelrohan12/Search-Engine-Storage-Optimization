import json
import sys
import os
import regex as re
from pathlib import Path
import pandas as pd
from itertools import combinations,islice

queries = pd.DataFrame()

def generate_queries(json_file):
    
    data = json.load(json_file)
    keyword_list = data.keys()
    values_set = set()
    for keyword in keyword_list:
        if (type(data[keyword]) is dict):
            values_set.add(keyword)
            keyword2_list = data[keyword].keys()
            for keyword_2 in keyword2_list:
                values_set.add(keyword + ' ' + keyword_2)
        else:
            values_set.add(keyword)
    
    query_keywords = list(values_set)
    
    final_queries = []
    for i in range(1,6):
        [final_queries.append(" ".join(keyword)) for keyword in islice(combinations((query_keywords),i),500)]
    
    result = Path(json_file.name)
            
    target_name = re.sub('_DS.json','',result.name)
    labels = [target_name for i in range(len(final_queries))]
    val = {'queries':final_queries, 'files': labels}
    query = pd.DataFrame(val, index=None)
    
    global queries
    queries = pd.concat([queries,query], ignore_index=True)
    
    return result.name
        # queries.head()


def main():
    print("Starting to create queries for each inverted index ds...\n")
    path = sys.path[0] + '\\inverted-index-ds'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = generate_queries(json_file)
            print(name + " has queries successfully created")
            
    global queries
    queries.to_csv(f'./queries.csv', index=False)
    print("Finished generating queries!!\n")

if __name__ == '__main__':
    main()
import sys
import os
import json
from pybloom import BloomFilter
import regex as re
from pathlib import Path
import tempfile
import itertools 

# class BloomFilter(object):
#     def __init__(self, capacity, error_rate=0.001):
#         if not(0 < error_rate < 1):
#             raise ValueError("Bloom filter must have an error_rate between 0 and 1")
#         if not capacity > 0:
#             raise ValueError("Bloom filter must have capacity greater than 0")
            
def create_bloom_filter(json_file):
    data = json.load(json_file)
    
    keywords_list = data.keys()
    
    count = 0
    key_items = []
    
    for keyword in keywords_list:
        if (type(data[keyword]) is dict):
            count += 1
            key_items.append(keyword)
            keyword2_list = data[keyword].keys()
            for keyword_2 in keyword2_list:
                key_items.append(keyword_2)
                count += 1
        else:
            key_items.append(keyword)
            
    key_items = [*set(key_items)]
            
    data_filter = BloomFilter(capacity=len(key_items), error_rate=0.001)
    
    for i in range(len(key_items)):
        data_filter.add(key_items[i])
    
    # print(len(key_items))
    
    result = Path(json_file.name)
    
    name = re.sub('_DS.json','_Filter',result.name)
    
    path = sys.path[0] + '\\Bloom-Filters\\' 
    
    tempfile._get_candidate_names = lambda: itertools.repeat(name) 
    
    f = tempfile.NamedTemporaryFile(prefix='',suffix = '', dir=path, delete=False) 
    data_filter.tofile(f)        
    return name
        
    # print("Canon" in data_filter)
    




def main():
    print("Starting to create bloom filters for each inverted index ds...\n")
    
    path = sys.path[0] + '\\inverted-index-ds'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = create_bloom_filter(json_file)
            print(name + " has been successfully created")
            
    print("\nBloom Filters of each inverted index ds have been successfully created")


if __name__ == "__main__":
    main()
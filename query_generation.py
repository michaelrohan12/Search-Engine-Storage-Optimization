import json
import pandas as pd

#function to detect whether string contains digits
def contains_digit(s):
    num = 0
    digit = False
    for i in s:
        if i.isdigit():
            digit = True
            num += 1
    if(num > 0):
        return num
    else:
        return False



def generate_queries():
    file_names = ['CameraLens.json','Laptop.json','LaptopPeriferals.json','Mobile.json','Refrigerator.json','Tablet.json','TV.json','WashingMachine.json','WearableSmartDevice.json']
    queries = pd.DataFrame()
    for file in file_names:
        with open(f'./data/{file}') as fp:
            json_files = json.load(fp)
        keys_set = set()
        values_set = set()
        for json_file in json_files:
            keys = list(json_file.keys())
            values = list(json_file.values())
            if len(keys) == len(values):
                for i in range(len(keys)):
                    if(keys[i].strip().startswith('id') == True):
                        continue
                    if(contains_digit(values[i]) > 3 and len(values[i]) < 30 or len(values[i]) <= 5):
                        values_set.add(keys[i].strip()+'-'+values[i])
                        continue
                    if values[i] == 'Yes' or values[i] == 'No' or len(values[i]) >= 30 or len(values[i]) <=3:
                        if len(keys[i].strip()) <= 3:
                            continue
                        values_set.add(keys[i].strip())
                    else:
                        if len(values[i].strip()) <= 3:
                            continue
                        values_set.add(values[i].strip())
        labels = [f'{file}' for i in range(len(values_set))]
        val = {'queries':list(values_set), 'files': labels}
        query = pd.DataFrame(val, index=None)
        queries = queries.append(query, ignore_index=True)
        # queries.head()

    queries.to_csv(f'./queries.csv', index=False)


def main():
    generate_queries()

if __name__ == '__main__':
    main()
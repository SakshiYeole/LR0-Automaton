import pandas as pd
from tabulate import tabulate

def convertData(data, header_symbols):
    dict = {}
    
    for item in data:
        for s in header_symbols:
            key = s
            value = 'NULL'
            if key in item:
                value = str(item[s])
                
            if key in dict:
                dict[key].append(value)
            else:
                dict[key] = [value]
    return dict
    
def visualizeTable(map, header_symbols):
    data = convertData(map, header_symbols)
    df = pd.DataFrame(data)

    table = tabulate(df, headers='keys', tablefmt='grid')
    print(table)

def visualizeTableToFile(map, path, header_symbols):
    data = convertData(map, header_symbols)
    df = pd.DataFrame(data)
    table = tabulate(df, headers='keys', tablefmt='grid')
    with open(path, 'w') as file:
        file.write(table)

def main():
    # Sample data for the table
    dict = {
        'Name': ['John', 'Alice', 'Bob'],
        'Age': [30, 25, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    data = [{'Name': 'John', 'Age': 30, 'City': 'NewYork'}, {'Name': 'Alice', 'Age': 25, 'City': 'Los Angeles'}, {'Name': 'Bob', 'Age': 35, 'City': 'Chicago'}]

    path = 'ParsingTable.txt'
    visualizeTableToFile(data, path)
    visualizeTable(data)
    # print(dict)

if __name__ == "__main__":
    main()
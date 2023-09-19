import pandas as pd
from tabulate import tabulate
import os

def visualizeTable(data, path):
    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Display the table
    table = tabulate(df, headers='keys', tablefmt='grid')

    # Print the table
    print(table)

    # Write the table to a text file
    with open(path, 'w') as file:
        file.write(table)

    # print("Table written to 'table.txt'")
    
def main():
    # Sample data for the table
    data = {
        'Name': ['John', 'Alice', 'Bob'],
        'Age': [30, 25, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    # path = os.path.join()
    path = 'ParsingTable.txt'
    visualizeTable(data, path)

if __name__ == "__main__":
    main()
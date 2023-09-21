import pandas as pd
from tabulate import tabulate
import os
import sys


import settings
# sys.exit(-1)
path = os.getcwd()
# print(path)
# sys.exit(-1)
sys.path.append(path + '\..\LR0Grammar')
import LR0automaton

def convertData(parseTable):
    t = LR0automaton.LR0Grammar()
    data = {}
    header_symbols = []
    header_symbols = t.getTerminalSymbols()         # ACTION
    header_symbols.extend(t.getNonTerminalSymbols())    #GOTO

    for str in header_symbols:
        data[str] = []
        for i in t.getStateIndexing():
            data[str].append(parseTable[i][str])

    return data

def visualizeTable(map):
    # Create a DataFrame from the data
    data = convertData(map)
    df = pd.DataFrame(data)

    table = tabulate(df, headers='keys', tablefmt='grid')
    print(table)

def visualizeTableToFile(map, path):
    # Create a DataFrame from the data
    data = convertData(map)
    # data = map
    df = pd.DataFrame(data)
    table = tabulate(df, headers='keys', tablefmt='grid')
    with open(path, 'w') as file:
        file.write(table)

def main():
    # Sample data for the table
    # data = {
    #     'Name': ['John', 'Alice', 'Bob'],
    #     'Age': [30, 25, 35],
    #     'City': ['New York', 'Los Angeles', 'Chicago']
    # }
    # data = [{'a':'b'}, {'c':'d'}]
    # path = 'ParsingTable.txt'
    # visualizeTableToFile(data, path)
    # t = LR0automaton.LR0Grammar()
    # t.setFirstSymbol("E")
    # t.addNonterminalSymbol("E")
    # t.addNonterminalSymbol("T")
    # t.addNonterminalSymbol("F")

    # t.addTerminalSymbol("+")
    # t.addTerminalSymbol("*")
    # t.addTerminalSymbol("(")
    # t.addTerminalSymbol(")")
    # t.addTerminalSymbol("F")

    # t.addRule("E' -> E")
    # t.addRule("E -> E + T | T")
    # t.addRule("T -> T * F | F")
    # t.addRule("F -> ( E ) | id")

    # # t.printGrammar()

    
    # t.compute_transitions()
    # t.computeIndexingOfStates()
    # t.printIndexingOfStates()
    # # t.printTransitions()
    # t.computeParsingTable()
    
    # for i in t.getStateIndexing:
    #         print(i)
    pass

if __name__ == "__main__":
    main()
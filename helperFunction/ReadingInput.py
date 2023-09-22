import sys
import os
path = os.getcwd()
sys.path.append(path + '\..\LR0Grammar')
from LR0Grammar import LR0automaton

class ReadingInput:
    def readInputFromFile(path):
        with open(path, 'r') as file:
            grammar = LR0automaton.LR0Grammar()
            startSymbol = file.readline().strip()
            grammar.setFirstSymbol(startSymbol)

            nonTerminalString = file.readline().strip()
            nonTeminals = nonTerminalString.split()
            grammar.addAllNonTerminalSymbolFromIterator(nonTeminals)

            terminalString = file.readline().strip()
            terminals = terminalString.split()
            grammar.addAllTerminalSymbolFromIterator(terminals)

            for line in file:
                input_line = line.strip()
                input_line = input_line.replace('Îµ', "ε")
                if not input_line:
                    continue
                grammar.addRule(input_line)

        return grammar
    
def main():
    pass

if __name__ == "__main__":
    main()
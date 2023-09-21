import sys
sys.path.append('E:\Acads\Semester 7\CD\Lab\lab6\LR0Grammar\model')
from LR0Grammar.model import Grammar

class ReadingInput:
    def readInputFromFile(path):
        with open(path, 'r') as file:
            grammar = Grammar.Grammar()
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
                if not input_line:
                    continue
                grammar.addRule(input_line)

        return grammar
    
def main():
    pass

if __name__ == "__main__":
    main()
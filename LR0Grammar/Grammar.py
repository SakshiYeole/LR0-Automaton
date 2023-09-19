from model import productionRule as pr

import os

class Grammar:                   
    epsilon = '\u03B5'
    end_of_line = "$"
    firstSymbol = ""

    def __init__(self) -> None:         #Tested
        self.production_rule = []           #list of ProductionRule
        self.terminal_symbols = []
        self.non_terminal_symbols = []
        self.terminal_symbols.append(self.end_of_line)
        self.firstSet = {}
        self.followSet = {}   

    def __str__(self) -> str:           # Tested
        s = ""
        for i in self.production_rule:
            s += i.__str__()
        return s

    def getFirstSymbol(self):           # Tested
        return self.firstSymbol
    
    def setFirstSymbol(self, firstSymbol):      # Tested
        self.firstSymbol = firstSymbol

    def getProductionRules(self):           # Tested
        return self.production_rule
    
    def getProductionRulesBasedOnNonTerminal(self, symbol):     # Tested
        rule = pr.ProductionRule(symbol)
        if rule in self.production_rule:
            index = self.production_rule.index(rule)
            return self.production_rule[index]
        else:
            return None

    def addRuleList(self, LHS, RHS):           # Tested
        alreadyExistingRule = self.getProductionRulesBasedOnNonTerminal(LHS)

        if alreadyExistingRule is None:
            newProductionRule = pr.ProductionRule(LHS)
            newProductionRule.addRHSall(RHS)
            self.production_rule.append(newProductionRule)
        else:
            alreadyExistingRule.addRHS(RHS)

    def addRule(self, input):               # Tested
        rulesplit = input.split("->")
        left_side = rulesplit[0]
        left_side = left_side.strip()
        right_side = rulesplit[1].split("|")

        rightfinal = []
        for right in right_side:
            right = right.strip()
            symbols = right.split(" ")
            rightfinal.append(symbols)
        self.addRuleList(left_side, rightfinal)

    def getTerminalSymbols(self):           # Tested
        return self.terminal_symbols
    
    def getNonTerminalSymbols(self):        # Tested
        return self.non_terminal_symbols
    
    def addAllTerminalSymbolFromIterator(self, iterator):       # Tested
        for symbol in iterator:
            self.addTerminalSymbol(symbol)

    def addAllNonTerminalSymbolFromIterator(self, iterator):    # Tested
        for symbol in iterator:
            self.addNonterminalSymbol(symbol)
        
    def addTerminalSymbol(self, str):            # Tested
        if str not in self.terminal_symbols:              
            self.terminal_symbols.append(str)

    def addNonterminalSymbol(self, str):                # Tested
        self.non_terminal_symbols.append(str)
    
    def isTerminalSymbol(self, str):            # Tested
        if str not in self.terminal_symbols:
            return False
        return True
    
    def isNonterminalSymbol(self, str):         # Tested
        if str not in self.non_terminal_symbols:
            return False
        return True
    
    def findNewName(self, LHS):             # Tested
        new_name = LHS + "'"
        notunique = True
        while(notunique):
            notunique  = False
            for r in self.production_rule:
                if r.__eq__(pr.ProductionRule(new_name)):
                    new_name += "'"
                    notunique = True
        
        # self.non_terminal_symbols.append(new_name)
        return new_name
    
    def printGrammar(self):             # Tested
        print("Set of terminal symbols: {}".format(str(self.terminal_symbols)))
        print("Set of non_terminal symbols: {}".format(str(self.non_terminal_symbols)))
        print("Rules of Grammar: ")
        for i in self.production_rule:
            print(i)

    def printGrammarWithToFile(self, pathToDirectory, note):
        pathToFile = os.path.join(pathToDirectory, note.replace(" ", "") + ".txt")

        with open(pathToFile, 'w', encoding='utf-8') as writer:
            writer.write(note + "\n")
            writer.write("Set of Terminal Symbols: " + str(self.terminal_symbols) + "\n")
            writer.write("Set of Non-Terminal Symbols: " + str(self.non_terminal_symbols) + "\n")
            writer.write("Rules in the given Grammar: \n")

            for productionRule in self.production_rule:
                writer.write(str(productionRule) + "\n")
    
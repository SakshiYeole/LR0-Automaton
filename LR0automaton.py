# the final output DFA must be a list of states, where each item in list a dictionary
# 1st key is the items matched to dictionary of production rules(each prodcution rule is a dict with items as strings and key as teh LHS of prodcution rule) in that state.
# 2nd key is transition matched to dictionary of transitions from that state to some other state on the key element
# states = [
#     {'items': ['S -> .E', 'E -> .E + T', 'E -> .T', 'T -> .T*F', 'T -> .F'], 'transitions': {'E': 1}},        # 0
#     {'items': ['S -> E.'], 'transitions': {}},              # 1
#     {'items': ['E -> .E+T', 'E -> .T'], 'transitions': {'E': 3, 'T': 2}}, #2
#     {'items': ['E -> E.+T'], 'transitions': {'T': 4}},      # 3
#     {'items': ['E -> E+.T'], 'transitions': {'T': 5}},      # 4
#     {'items': ['T -> .T*F', 'T -> .F'], 'transitions': {'T': 6, 'F': 7}},   # 5
#     {'items': ['T -> T.*F'], 'transitions': {'F': 8}},         # 6
#     {'items': ['F -> .(E)', 'F -> .id'], 'transitions': {'E': 9, 'id': 10}},    # 7
#     {'items': ['F -> (E.)'], 'transitions': {}},            # 8
#     {'items': ['E -> E+.T.'], 'transitions': {}},    # 9
#     {'items': ['T -> T.*F.'], 'transitions': {}},           # 10
# ]

import os
import sys
import copy
from pathlib import Path
from enum import Enum
import shutil
import subprocess

class ProductionRule:           #Tested

    def __init__(self, LHS):
        self.LHS = LHS
        self.RHS = []
    
    def __str__(self):
        return  f"{self.LHS} -> {self.RHS} "
    
    def addRHS(self, RHS):
        self.RHS.append(RHS)
    
    def addRHSall(self,RHSall):
        for i in RHSall:
            self.addRHS(i)
    
    def getLHS(self):
        return self.LHS
    
    def getRHS(self):
        return self.RHS
    
    def setnewRHS(self, RHS):
        self.RHS.clear()
        self.addRHSall(RHS)

    def printProductionRule(self):
        print(f"{self.LHS} -> ")
        s = ""
        for right in self.RHS:
            s = s + " " + right + " |"
        s.replace(s[len(s)-1], "")
        print(s)

    def __eq__(self, other):
        if other == None:
            return False
        return self.LHS == other.LHS

class itemType:
        new_item = "new_item"
        derived_item = "derived_item"

class Item:
    dotMarker = '\u2022'
    # isreduction, 

    def __init__(self, LHS, RHS, item_type):
        self.LHS = LHS
        self.RHS = copy.deepcopy(RHS)
        if item_type == itemType.new_item:
            self.RHS.insert(0, self.dotMarker)

    def isReductionItem(self):
        return self.RHS.index(self.dotMarker)==(len(self.RHS)-1)
    
    def getSymbolNextToDotMarker(self):
        if self.isReductionItem():
            return None
        indexOfDotMarker = self.RHS.index(self.dotMarker)
        return self.RHS[indexOfDotMarker + 1]
    
    def movingDotMarkerInItemAndReturn(self):
        if self.isReductionItem():
            print("Is a Reduction Item")
            return None
        newRHS = copy.deepcopy(self.RHS)
        indexOfDotMarker = self.RHS.index(self.dotMarker)
        self.RHS.remove(self.dotMarker)
        self.RHS.insert(indexOfDotMarker + 1, self.dotMarker)
        return Item(self.LHS, newRHS, self.itemType.derived_item)
    
    def closure(self, production_rules):
        closure_item = {self}
        addedNew = True
        while addedNew:
            addedNew = False
            toAdd = set()
            for currItem in closure_item:
                nextSymbolOfDotMarker = currItem.getSymbolNextToDotMarker()
                indexInProductionRule = next((i for i, rule in enumerate(production_rules) if rule.LHS == nextSymbolOfDotMarker), -1)
                if indexInProductionRule < 0:
                    continue
                production_rule = production_rules[indexInProductionRule]
                LHSOfproductionRule = production_rule.LHS
                for RHSOfProductionRule in production_rule.RHS:
                    itemForParticularRUle = Item(LHSOfproductionRule, RHSOfProductionRule, itemType.new_item)
                    if itemForParticularRUle not in closure_item:
                        addedNew = True
                        toAdd.add(itemForParticularRUle)
            
            if toAdd:
                closure_item.update(toAdd)
        return closure_item

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, Item):
            return False
        return self.LHS == other.LHS and self.RHS == other.RHS
    
    def __str__(self):
        return  f"{self.LHS} -> {self.RHS} "
    
    def __hash__(self) -> int:
        return hash((self.LHS, tuple(self.RHS)))

class State:
    epsilon = '\u03B5'
    dotMarker = '\u2022'

    def __init__(self, non_closure_items, production_rules):
        self.items = set(non_closure_items)

        closure_items = set()
        for curr_item in self.items:
            curr_closure_items = curr_item.closure(production_rules)
            closure_items.update(curr_closure_items)
        
        self.items.update(closure_items)    

    def getItems(self):
        return copy.deepcopy(self.items)
    
    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, State):
            return False
        return self.items == other.items
    
    def __hash__(self) -> int:
        return hash(tuple(self.items))
    
    def __str__(self) -> str:
        stateStr = "State: \n"
        for item in self.items:
            stateStr += str(item) + "\n"
        return stateStr
    
class DFA:

    def __init__(self) -> None:
        self.states = []
        self.listOfStateNo = []
        self.startState = 0
        self.acceptingStateNo = None

    def __str__(self) -> str:
        s = ""
        for i in self.states:
            s += i.__str__()
        return s
    
    def getListOfStateNo(self):
        return self.listOfStateNo
    
    def getAcceptingStateNo(self):
        return self.acceptingStateNo
    
    def getStateItemsBasedOnStateNo(self, stateno):
        state = State(stateno)
        if state in self.states:
            index = self.states.index(state)
            return self.states[index]
        else:
            return None
        
    def addState(self, input):
        pass

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
        rule = ProductionRule(symbol)
        if rule in self.production_rule:
            index = self.production_rule.index(rule)
            return self.production_rule[index]
        else:
            return None

    def addRuleList(self, LHS, RHS):           # Tested
        alreadyExistingRule = self.getProductionRulesBasedOnNonTerminal(LHS)

        if alreadyExistingRule is None:
            newProductionRule = ProductionRule(LHS)
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
                if r.__eq__(ProductionRule(new_name)):
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
    

class ReadingInput:
    def readInputFromFile(path):
        with open(path, 'r') as file:
            grammar = Grammar()
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

    dotMarker = '\u2022'

    # Testing
    t = Grammar()
    # t.setFirstSymbol("S")
    # t.addNonterminalSymbol("S")
    # t.addNonterminalSymbol("L")
    # t.addNonterminalSymbol("L'")
    # t.addTerminalSymbol("(")
    # t.addTerminalSymbol(")")
    # t.addTerminalSymbol("a")
    t.addRule("E' -> E")
    t.addRule("E -> E + T | T")
    t.addRule("T -> T * F | F")
    t.addRule("F -> ( E ) | id")
    t.printGrammar()

    right = []
    right.append("(")
    right.append(dotMarker)
    right.append("E")
    right.append(")")
    i = Item("F", right, itemType.derived_item)
    print(f"Item: {i}")

    # closure = set()
    # closure = i.closure(t.getProductionRules())
    # for i in  closure:
    #     print(i)

    inititemset = set()
    inititemset.add(i)

    s1 = State(inititemset, t.getProductionRules())
    print(s1)
    s2 = State(inititemset, t.getProductionRules())
    print(s2)

    print(s1==s2)

    states = set()
    states.add(s1)
    states.add(s2)
    print(f"states size: {len(states)}")

if __name__ == "__main__":
    main()